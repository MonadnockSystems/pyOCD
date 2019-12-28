# pyOCD debugger
# Copyright (c) 2018-2019 Arm Limited
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from ...core import exceptions
from .. import common
import usb.core
import usb.util
import logging
import six
import threading
from collections import namedtuple
import platform
import errno
from binascii import hexlify

LOG = logging.getLogger(__name__)

TRACE = LOG.getChild("trace")
TRACE.setLevel(logging.CRITICAL)

JLinkInfo = namedtuple('JLinkInfo', 'version_name out_ep in_ep swv_ep')

USB_CLASS_VENDOR_SPECIFIC = 0xff

class JLinkUSBInterface(object):
    """!@brief Provides low-level USB enumeration and transfers for STLinkV2/3 devices."""

    ## Command packet size.
    CMD_SIZE = 16
    
    ## ST's USB vendor ID
    USB_VID = 0x1366

    @classmethod
    def _usb_match(cls, dev):
        try:
            # Check VID/PID.
            isJLink = (dev.idVendor == cls.USB_VID) 
            
            # Try accessing the current config, which will cause a permission error on Linux. Better
            # to error out here than later when building the device description. For Windows we
            # don't need to worry about device permissions, but reading descriptors requires special
            # handling due to the libusb bug described in __init__().
            if isJLink and platform.system() != "Windows":
                dev.get_active_configuration()
            
            return isJLink
        except usb.core.USBError as error:
            if error.errno == errno.EACCES and platform.system() == "Linux" \
                and common.should_show_libusb_device_error((dev.idVendor, dev.idProduct)):
                # We've already checked that this is JLink via VID, so we
                # can use a warning log level to let the user know it's almost certainly
                # a permissions issue.
                LOG.warning("%s while trying to get the JLink USB device configuration "
                   "(VID=%04x PID=%04x). This can probably be remedied with a udev rule. "
                   "See <https://github.com/mbedmicro/pyOCD/tree/master/udev> for help.",
                   error, dev.idVendor, dev.idProduct)
            return False
        except (IndexError, NotImplementedError, ValueError) as error:
            return False

    @classmethod
    def get_all_connected_devices(cls):
        try:
            devices = usb.core.find(find_all=True, custom_match=cls._usb_match)
        except usb.core.NoBackendError:
            common.show_no_libusb_warning()
            return []
    
        intfList = []
        for dev in devices:
            try:
                intf = cls(dev)
                intfList.append(intf)
            except (ValueError, usb.core.USBError, IndexError, NotImplementedError) as error:
                # Ignore errors that can be raised by libusb, just don't add the device to the list.
                pass
    
        return intfList

    def __init__(self, dev):
        self._dev = dev
        self._interface_num = None
        assert dev.idVendor == self.USB_VID
        self._ep_out = None
        self._ep_in = None
        self._ep_swv = None
        self._max_packet_size = 64
        self._closed = True

        # Open the device temporarily to read the descriptor strings. The Windows libusb
        # (version 1.0.22 at the time of this writing) appears to have a bug where it can fail to
        # properly close a device automatically opened for reading descriptors. The bug manifests
        # as every other call to get_all_connected_devices() returning no available probes,
        # caused by a getting a permissions error ("The device has no langid" ValueError) when
        # attempting to read descriptor strings. If we manually call dispose_resources() after
        # reading the strings, everything is ok. This workaround doesn't cause any issues with
        # Linux or macOS.
        try:
            self._vendor_name = self._dev.manufacturer
            self._product_name = self._dev.product
            self._serial_number = str(int(self._dev.serial_number))
        finally:
            usb.util.dispose_resources(self._dev)
    
    def open(self):
        assert self._closed
        
        # Debug interface is always interface 0, alt setting 0.
        config = self._dev.get_active_configuration()
        
        def _match_jlink_interface(interface):
            interface_name = usb.util.get_string(interface.device, interface.iInterface)
            # Now check the interface class to distinguish v1 from v2.
            if interface.bInterfaceClass != USB_CLASS_VENDOR_SPECIFIC:
                return False

            # Must have 2 endpoints.
            if interface.bNumEndpoints != 2:
                return False
            return True
        interface = usb.util.find_descriptor(config, custom_match=_match_jlink_interface)
        self._interface_num = interface.bInterfaceNumber
        
        # Look up endpoint objects.
        for endpoint in interface:
            if endpoint.bEndpointAddress & usb.util.ENDPOINT_IN:
                self._ep_in = endpoint
            else:
                self._ep_out = endpoint

        # Detach kernel driver
        try:
            if self._dev.is_kernel_driver_active(self._interface_num):
                self._dev.detach_kernel_driver(self._interface_num)
        except NotImplementedError as e:
            # Some implementations don't don't have kernel attach/detach
            pass

        # Explicitly claim the interface
        usb.util.claim_interface(self._dev, self._interface_num)
                
        if not self._ep_out:
            raise exceptions.ProbeError("Unable to find OUT endpoint")
        if not self._ep_in:
            raise exceptions.ProbeError("Unable to find IN endpoint")

        self._max_packet_size = self._ep_in.wMaxPacketSize
        
        self._flush_rx()
        self._closed = False
    
    def close(self):
        assert not self._closed
        self._closed = True
        usb.util.release_interface(self._dev, self._interface_num)
        usb.util.dispose_resources(self._dev)
        self._ep_out = None
        self._ep_in = None

    @property
    def serial_number(self):
        return self._serial_number

    @property
    def vendor_name(self):
        return self._vendor_name

    @property
    def product_name(self):
        return self._product_name

    @property
    def version_name(self):
        return self._info.version_name

    @property
    def max_packet_size(self):
        return self._max_packet_size

    def _flush_rx(self):
        # Flush the RX buffers by reading until timeout exception
        try:
            while True:
                self._ep_in.read(self._max_packet_size, 1)
        except usb.core.USBError:
            # USB timeout expected
            pass

    def _read(self, size, timeout=1000):
        # Minimum read size is the maximum packet size.
        read_size = max(size, self._max_packet_size)
        data = self._ep_in.read(read_size, timeout)
        return bytearray(data)[:size]

    def transfer(self, cmd, writeData=None, readSize=None, timeout=1000):
        try:
            # Command phase.
            TRACE.debug("  USB CMD> %s" % ' '.join(['%02x' % i for i in cmd]))
            count = self._ep_out.write(cmd, timeout)
            assert count == len(cmd)
            
            # Optional data out phase.
            if writeData is not None:
                TRACE.debug("  USB OUT> %s" % ' '.join(['%02x' % i for i in writeData]))
                count = self._ep_out.write(writeData, timeout)
                assert count == len(writeData)
            
            # Optional data in phase.
            if readSize is not None:
                TRACE.debug("  USB IN < (%d bytes)" % readSize)
                data = self._read(readSize)
                TRACE.debug("  USB IN < %s" % ' '.join(['%02x' % i for i in data]))
                return data
        except usb.core.USBError as exc:
            six.raise_from(exceptions.ProbeError("USB Error: %s" % exc), exc)
        return None

    def read_swv(self, size, timeout=1000):
        return bytearray(self._ep_swv.read(size, timeout))
    
    def __repr__(self):
        return "<{} @ {:#x} vid={:#06x} pid={:#06x} sn={} version={}>".format(
            self.__class__.__name__, id(self),
            self._dev.idVendor, self._dev.idProduct, self.serial_number,
            self.version)
