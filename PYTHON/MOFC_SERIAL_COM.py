# -*- coding: utf-8 -*-
"""
The RS-232 settings (baud rate, parity, stop bits, etc.)
Parity bit: None
Byte order: Little Endian
Speed: 115200 bit/s
RS-232 setup: Standard 8-bit RS-232 transmission
(Start bit = ‘0’, 8 data bits, Stop bit = ‘1’)


protocol setup
each message consist of 8 bytes

Byte0: Sych1  0x55
Byte1: Sync1  0xaa
Byte2: LenL   0x8
Byte3: LenH   0x0
Byte4: D0 (Spi-Addr R/W + 7 bits addr)
Byte5: D1 (D[23:16])
Byte6: D2 (D[15:8])
Byte7: D3 (D[7:0])


"""

#%%


import serial
import struct

import pandas as pd
import numpy as np

class RS232Device:
    def __init__(self, port):
        self.ser = serial.Serial(
            port=port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            write_timeout=1,
            timeout=1
        )

    def send_uint32(self, value: int):
        """
        Send uint32 using BIG-ENDIAN byte order
        """
        if not (0 <= value <= 0xFFFFFFFF):
            raise ValueError("Value must be uint32")

        frame = bytearray([
            0x55,       # Sync 1
            0xAA,       # Sync 2
            0x08,       # Length LSB
            0x00        # Length MSB
        ])

        # uint32 -> BIG endian (MSB first)
        frame.extend(struct.pack('>I', value))

        self.ser.write(frame)
        self.ser.flush()

    def receive_uint32(self) -> int:
        """
        Receive 8-byte frame and extract uint32 (BIG-ENDIAN)
        """
        data = self.ser.read(8)

        if len(data) != 8:
            raise TimeoutError("Incomplete frame")

        if data[0] != 0x55 or data[1] != 0xAA:
            raise ValueError("Invalid sync word")

        if data[2] != 0x08 or data[3] != 0x00:
            raise ValueError("Invalid length field")

        value = struct.unpack('>I', data[4:8])[0]
        return value

    def close(self):
        self.ser.close()



def SpiRegRead(Addr):
    SpiDev.send_uint32((0x80+Addr)<<24)
    RetVal = SpiDev.receive_uint32() 
    return(RetVal)

def SpiRegWrite(Addr,Data):
    SpiDev.send_uint32(0x80+Addr)
    RetVal = SpiDev.receive_uint32() 
    return(RetVal)


def read_xl_config_msg(xlsx_file, sheet_name, msg_col='W',msg_rows=(2,37)):
    HexValues = pd.read_excel(
        xlsx_file,
        sheet_name=sheet_name,
        usecols=msg_col,
        header=None,
        dtype=str
        ).iloc[msg_rows[0]:msg_rows[1], 0].to_list()

    CheckBox = pd.read_excel(
        xlsx_file,
        sheet_name=sheet_name,
        usecols="G",
        header=None
        ).iloc[23, 0]   # row 24 → index 23

    print(f'CheckBox:={CheckBox}')



    #HexValues = df.iloc[msg_rows[0]:msg_rows[1], 0].to_list()
    u32_array = np.array(
        [int(val, 16) for val in HexValues],
        dtype=np.uint32
        )

    CnfgMsgFields =['GlblCfg','BitCfg']
    for ch in range(8):
        CnfgMsgFields += [f'Ch{ch}CfgReg0',f'Ch{ch}CfgReg1',f'Ch{ch}CfgReg2',f'Ch{ch}CfgReg3']
    CnfgMsgFields +=['ChkSum']
    hex_addr = [hex(i) for i in range(0x6, 0x29)]

    df = pd.DataFrame(data = {
                          'HexAddr' :hex_addr,
                          'HexVal'  :HexValues,
                          'DecAddr'  :np.arange(0x6,0x29),
                          'DecVal': u32_array},index=CnfgMsgFields)





    return(df)

import time
if __name__ == "__main__":
    SpiDev = RS232Device(port="COM3")

    xlsx_file = "C:/Users/guyiz/Documents/Work/CDRP/MOFC//MOFC_GUI_TEST1.2.xlsx"
    sheet_name = "MOFC_ASSIGN"
    df =read_xl_config_msg(xlsx_file, sheet_name)
    for idx, row in df.iterrows():
        print(idx, row['DecAddr'] ,row['DecVal'])
        #SpiRegWrite(row['DecAddr'],row['DecVal'])

    SpiDev.close()
    for i in range (3):
        print(i)
        time.sleep(1)
#     dev = RS232Device(port="COM3")  # Linux: /dev/ttyUSB0

#     try:
#         tx_val = 0x12345678
#         dev.send_uint32(tx_val)
#         print(f"Sent: 0x{tx_val:08X}")

#         rx_val = dev.receive_uint32()
#         print(f"Received: 0x{rx_val:08X}")

#     finally:
#         dev.close()
# #SpiDev = RS232Device(port="COM3")
#%%

#%%
Sub SendCfgMsg()

    Dim pythonExe As String
    Dim scriptPath As String
    Dim cmd As String

    pythonExe = "C:\Users\guyiz\anaconda3\python.exe"
    scriptPath = "C:\Users\guyiz\Documents\Work\CDRP\MOFC\PYTHON\MOFC_SERIAL_COM.py"

    cmd = "cmd /k """ & pythonExe & " " & scriptPath & """"
    cmd = pythonExe & " " & scriptPath
    Shell cmd, vbNormalFocus



End Sub