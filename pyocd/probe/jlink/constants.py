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

class Commands:    
    """!
    @brief JLink commands.
    """
    
    # Get system information functions
    EMU_CMD_VERSION = 0x01
    EMU_CMD_GET_SPEEDS = 0xc0
    EMU_CMD_GET_MAX_MEM_BLOCK = 0xd4
    EMU_CMD_GET_CAPS = 0xe8
    EMU_CMD_GET_CAPS_EX = 0xed
    EMU_CMD_GET_HW_VERSION = 0xf0
    
    # Get state information functions
    EMU_CMD_GET_STATE = 0x07
    EMU_CMD_GET_HW_INFO = 0xc1
    EMU_CMD_GET_COUNTERS = 0xc2
    EMU_CMD_MEASURE_RTCK_REACT = 0xf6
    
    # JTAG & Hardware functions
    EMU_CMD_RESET_TRST = 0x02
    EMU_CMD_SET_SPEED = 0x05
    EMU_CMD_SELECT_IF = 0xc7
    EMU_CMD_SET_KS_POWER = 0x08
    EMU_CMD_HW_CLOCK = 0xc8
    EMU_CMD_HW_TMS0 = 0xc9
    EMU_CMD_HW_TMS1 = 0xca
    EMU_CMD_HW_DATA0 = 0xcb
    EMU_CMD_HW_DATA1 = 0xcc
    EMU_CMD_HW_JTAG = 0xcd
    EMU_CMD_HW_JTAG2 = 0xce
    EMU_CMD_HW_JTAG3 = 0xcf
    EMU_CMD_HW_JTAG_WRITE = 0xd5
    EMU_CMD_HW_JTAG_GET_RESULT = 0xd6
    EMU_CMD_HW_TRST0 = 0xde
    EMU_CMD_HW_TRST1 = 0xdf
    EMU_CMD_WRITE_DCC = 0xf1
    
    # Target functions
    EMU_CMD_RESET_TARGET = 0x03
    EMU_CMD_HW_RELEASE_RESET_STOP_EX = 0xd0
    EMU_CMD_HW_RELEASE_RESET_STOP_TIMED = 0xd1
    EMU_CMD_HW_RESET0 = 0xdc
    EMU_CMD_HW_RESET1 = 0xdd
    EMU_CMD_GET_CPU_CAPS = 0xe9
    EMU_CMD_EXEC_CPU_CMD = 0xea
    EMU_CMD_WRITE_MEM = 0xf4
    EMU_CMD_READ_MEM = 0xf5
    EMU_CMD_WRITE_MEM_ARM79 = 0xf7
    EMU_CMD_READ_MEM_ARM79 = 0xf8
    
    # Configuration functions
    EMU_CMD_READ_CONFIG = 0xf2
    EMU_CMD_WRITE_CONFIG = 0xf3
    

    # Capabilities returned by EMU_CMD_GET_CAPS.
    EMU_CAP_RESERVED = 1 << 0
    EMU_CAP_GET_HW_VERSION = 1 << 1
    EMU_CAP_WRITE_DCC = 1 << 2
    EMU_CAP_ADAPTIVE_CLOCKING = 1 << 3
    EMU_CAP_READ_CONFIG = 1 << 4
    EMU_CAP_WRITE_CONFIG = 1 << 5
    EMU_CAP_TRACE = 1 << 6
    EMU_CAP_WRITE_MEM = 1 << 7
    EMU_CAP_READ_MEM = 1 << 8
    EMU_CAP_SPEED_INFO = 1 << 9
    EMU_CAP_EXEC_CODE = 1 << 10
    EMU_CAP_GET_MAX_BLOCK_SIZE = 1 << 11
    EMU_CAP_GET_HW_INFO = 1 << 12
    EMU_CAP_SET_KS_POWER = 1 << 13
    EMU_CAP_RESET_STOP_TIMED = 1 << 14
    EMU_CAP_15 = 1 << 15
    EMU_CAP_MEASURE_RTCK_REACT = 1 < 16
    EMU_CAP_SELECT_IF = 1 << 17
    EMU_CAP_RW_MEM_ARM79 = 1 << 18
    EMU_CAP_GET_COUNTERS = 1 << 19
    EMU_CAP_READ_DCC = 1 << 20
    EMU_CAP_GET_CPU_CAPS = 1 << 21
    EMU_CAP_EXEC_CPU_CMD = 1 << 22
    EMU_CAP_SWO = 1 << 23
    EMU_CAP_WRITE_DCC_EX = 1 << 24
    EMU_CAP_UPDATE_FIRMWARE_EX = 1 << 25
    EMU_CAP_FILE_IO = 1 << 26
    EMU_CAP_REGISTER = 1 << 27
    EMU_CAP_INDICATORS = 1 << 28
    EMU_CAP_TEST_NET_SPEED = 1 << 29
    EMU_CAP_RAWTRACE = 1 << 30
    EMU_CAP_31 = 1 << 31
    
    # Responses to EMU_CMD_GET_HW_VERSION
    EMU_VERSION_HW_TYPE_JLINK = 0x00
    EMU_VERSION_HW_TYPE_JTRACE = 0x01
    EMU_VERSION_HW_TYPE_FLASHER = 0x02
    EMU_VERSION_HW_TYPE_JLINK_PRO = 0x03

    # Arguments for EMU_CMD_SET_SPEED
    EMU_CMD_SET_SPEED_ADAPTIVE = 0xffff

    # Subcommands and Interface definitions for EMU_CMD_SELECT_IF
    EMU_CMD_SELECT_IF_SUB_GET_AVAIL = 0xff
    EMU_CMD_SELECT_IF_SUB_GET_CURRENT = 0xfe
    EMU_CMD_SELECT_IF_SUB_SET_JTAG = 0x1
    EMU_CMD_SELECT_IF_SUB_SET_SWD = 0x2

    # Commands to exit other modes.
    DFU_EXIT = 0x07
    SWIM_EXIT = 0x01

    # JTAG commands.
    JTAG_READMEM_32BIT = 0x07
    JTAG_WRITEMEM_32BIT = 0x08
    JTAG_READMEM_8BIT = 0x0c
    JTAG_WRITEMEM_8BIT = 0x0d
    JTAG_EXIT = 0x21
    JTAG_ENTER2 = 0x30
    JTAG_GETLASTRWSTATUS2 = 0x3e # From V2J15
    JTAG_DRIVE_NRST = 0x3c
    SWV_START_TRACE_RECEPTION = 0x40
    SWV_STOP_TRACE_RECEPTION = 0x41
    SWV_GET_TRACE_NEW_RECORD_NB = 0x42
    SWD_SET_FREQ = 0x43 # From V2J20
    JTAG_SET_FREQ = 0x44 # From V2J24
    JTAG_READ_DAP_REG = 0x45 # From V2J24
    JTAG_WRITE_DAP_REG = 0x46 # From V2J24
    JTAG_READMEM_16BIT = 0x47 # From V2J26
    JTAG_WRITEMEM_16BIT = 0x48 # From V2J26
    JTAG_INIT_AP = 0x4b # From V2J28
    JTAG_CLOSE_AP_DBG = 0x4c # From V2J28
    SET_COM_FREQ = 0x61 # V3 only, replaces SWD/JTAG_SET_FREQ
    GET_COM_FREQ = 0x62 # V3 only
    
    # Parameters for JTAG_ENTER2.
    JTAG_ENTER_SWD = 0xa3
    JTAG_ENTER_JTAG_NO_CORE_RESET = 0xa3

    # Parameters for JTAG_DRIVE_NRST.
    JTAG_DRIVE_NRST_LOW = 0x00
    JTAG_DRIVE_NRST_HIGH = 0x01
    JTAG_DRIVE_NRST_PULSE = 0x02
    
    # Parameters for JTAG_INIT_AP and JTAG_CLOSE_AP_DBG.
    JTAG_AP_NO_CORE = 0x00
    JTAG_AP_CORTEXM_CORE = 0x01
    
    # Parameters for SET_COM_FREQ and GET_COM_FREQ.
    JTAG_STLINK_SWD_COM = 0x00
    JTAG_STLINK_JTAG_COM = 0x01
    
class Status(object):
    """!
    @brief STLink status codes and messages.
    """
    # Status codes.
    JTAG_OK = 0x80
    JTAG_UNKNOWN_ERROR = 0x01
    JTAG_SPI_ERROR = 0x02
    JTAG_DMA_ERROR = 0x03
    JTAG_UNKNOWN_JTAG_CHAIN = 0x04
    JTAG_NO_DEVICE_CONNECTED = 0x05
    JTAG_INTERNAL_ERROR = 0x06
    JTAG_CMD_WAIT = 0x07
    JTAG_CMD_ERROR = 0x08
    JTAG_GET_IDCODE_ERROR = 0x09
    JTAG_ALIGNMENT_ERROR = 0x0a
    JTAG_DBG_POWER_ERROR = 0x0b
    JTAG_WRITE_ERROR = 0x0c
    JTAG_WRITE_VERIF_ERROR = 0x0d
    JTAG_ALREADY_OPENED_IN_OTHER_MODE = 0x0e
    SWD_AP_WAIT = 0x10
    SWD_AP_FAULT = 0x11
    SWD_AP_ERROR = 0x12
    SWD_AP_PARITY_ERROR = 0x13
    SWD_DP_WAIT = 0x14
    SWD_DP_FAULT = 0x15
    SWD_DP_ERROR = 0x16
    SWD_DP_PARITY_ERROR = 0x17
    SWD_AP_WDATA_ERROR = 0x18
    SWD_AP_STICKY_ERROR = 0x19
    SWD_AP_STICKYORUN_ERROR = 0x1a
    SWV_NOT_AVAILABLE = 0x20
    JTAG_FREQ_NOT_SUPPORTED = 0x41
    JTAG_UNKNOWN_CMD = 0x42
    
    ## Map from status code to error message.
    MESSAGES = {
        JTAG_UNKNOWN_ERROR : "Unknown error",
        JTAG_SPI_ERROR : "SPI error",
        JTAG_DMA_ERROR : "DMA error",
        JTAG_UNKNOWN_JTAG_CHAIN : "Unknown JTAG chain",
        JTAG_NO_DEVICE_CONNECTED : "No device connected",
        JTAG_INTERNAL_ERROR : "Internal error",
        JTAG_CMD_WAIT : "Command wait",
        JTAG_CMD_ERROR : "Command error",
        JTAG_GET_IDCODE_ERROR : "Get IDCODE error",
        JTAG_ALIGNMENT_ERROR : "Alignment error",
        JTAG_DBG_POWER_ERROR : "Debug power error",
        JTAG_WRITE_ERROR : "Write error",
        JTAG_WRITE_VERIF_ERROR : "Write verification error",
        JTAG_ALREADY_OPENED_IN_OTHER_MODE : "Already opened in another mode",
        SWD_AP_WAIT : "AP wait",
        SWD_AP_FAULT : "AP fault",
        SWD_AP_ERROR : "AP error",
        SWD_AP_PARITY_ERROR : "AP parity error",
        SWD_DP_WAIT : "DP wait",
        SWD_DP_FAULT : "DP fault",
        SWD_DP_ERROR : "DP error",
        SWD_DP_PARITY_ERROR : "DP parity error",
        SWD_AP_WDATA_ERROR : "AP WDATA error",
        SWD_AP_STICKY_ERROR : "AP sticky error",
        SWD_AP_STICKYORUN_ERROR : "AP sticky overrun error",
        SWV_NOT_AVAILABLE : "SWV not available",
        JTAG_FREQ_NOT_SUPPORTED : "Frequency not supported",
        JTAG_UNKNOWN_CMD : "Unknown command",
    }
    
    @staticmethod
    def get_error_message(status):
        return "STLink error ({}): {}".format(status, Status.MESSAGES.get(status, "Unknown error"))

## Map from SWD frequency in Hertz to delay loop count.
SWD_FREQ_MAP = {
    4600000 :   0,
    1800000 :   1, # Default
    1200000 :   2,
    950000 :    3,
    650000 :    5,
    480000 :    7,
    400000 :    9,
    360000 :    10,
    240000 :    15,
    150000 :    25,
    125000 :    31,
    100000 :    40,
}

## Map from JTAG frequency in Hertz to frequency divider.
JTAG_FREQ_MAP = {
    18000000 :  2,
    9000000 :   4,
    4500000 :   8,
    2250000 :   16,
    1120000 :   32, # Default
    560000 :    64,
    280000 :    128,
    140000 :    256,
}

