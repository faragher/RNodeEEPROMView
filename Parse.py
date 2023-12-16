import os
import struct
from datetime import datetime
import hashlib


ADDR_PRODUCT = 0x00
ADDR_MODEL   =  0x01
ADDR_HW_REV  =  0x02
ADDR_SERIAL  =  0x03
ADDR_MADE	   = 0x07
ADDR_CHKSUM	 =  0x0B
ADDR_SIGNATURE = 0x1B
ADDR_INFO_LOCK = 0x9B

ADDR_CONF_SF  = 0x9C
ADDR_CONF_CR  = 0x9D
ADDR_CONF_TXP = 0x9E
ADDR_CONF_BW  = 0x9F
ADDR_CONF_FREQ = 0xA3
ADDR_CONF_OK  = 0xA7

#A8 - AF is missing. 
	
ADDR_CONF_BT  = 0xB0
ADDR_CONF_DSET = 0xB1
ADDR_CONF_DINT = 0xB2
ADDR_CONF_DADR = 0xB3

#B4 - C7 is missing

PRODUCT = {}
PRODUCT[0x03] = "RNode" # PRODUCT_RNODE  0x03
PRODUCT[0xF0] = "Homebrew"	#define PRODUCT_HMBRW  0xF0
PRODUCT[0xE0] = "TBeam"#define PRODUCT_TBEAM  0xE0
PRODUCT[0xB2] = "LilyGO 1.0"#define PRODUCT_T32_10 0xB2
PRODUCT[0xB0] = "LilyGO 2.0"#define PRODUCT_T32_20 0xB0
PRODUCT[0xB1] = "LilyGO 2.1"#define PRODUCT_T32_21 0xB1
PRODUCT[0xC0] = "Heltec V2"#define PRODUCT_H32_V2 0xC0

models = {
    0xA4: [410000000, 525000000, 14, "410 - 525 MHz", "rnode_firmware.hex"],
    0xA9: [820000000, 1020000000, 17, "820 - 1020 MHz", "rnode_firmware.hex"],
    0xA2: [410000000, 525000000, 17, "410 - 525 MHz", "rnode_firmware_ng21.zip"],
    0xA7: [820000000, 1020000000, 17, "820 - 1020 MHz", "rnode_firmware_ng21.zip"],
    0xA3: [410000000, 525000000, 17, "410 - 525 MHz", "rnode_firmware_ng20.zip"],
    0xA8: [820000000, 1020000000, 17, "820 - 1020 MHz", "rnode_firmware_ng20.zip"],
    0xB3: [420000000, 520000000, 17, "420 - 520 MHz", "rnode_firmware_lora32v20.zip"],
    0xB8: [850000000, 950000000, 17, "850 - 950 MHz", "rnode_firmware_lora32v20.zip"],
    0xB4: [420000000, 520000000, 17, "420 - 520 MHz", "rnode_firmware_lora32v21.zip"],
    0xB9: [850000000, 950000000, 17, "850 - 950 MHz", "rnode_firmware_lora32v21.zip"],
    0xBA: [420000000, 520000000, 17, "420 - 520 MHz", "rnode_firmware_lora32v10.zip"],
    0xBB: [850000000, 950000000, 17, "850 - 950 MHz", "rnode_firmware_lora32v10.zip"],
    0xC4: [420000000, 520000000, 17, "420 - 520 MHz", "rnode_firmware_heltec32v2.zip"],
    0xC9: [850000000, 950000000, 17, "850 - 950 MHz", "rnode_firmware_heltec32v2.zip"],
    0xE4: [420000000, 520000000, 17, "420 - 520 MHz", "rnode_firmware_tbeam.zip"],
    0xE9: [850000000, 950000000, 17, "850 - 950 MHz", "rnode_firmware_tbeam.zip"],
    0xFE: [100000000, 1100000000, 17, "(Band capabilities unknown)", None],
    0xFF: [100000000, 1100000000, 14, "(Band capabilities unknown)", None],
}
 

def dehex(b):
  buffer = ""
  for bb in b:
    buffer = buffer+str(hex(bb))[1:4]
  return buffer


EEPROM = ""
with open("Example.hex","rb") as payload:
  EEPROM = payload.read()
  
BUF = len(EEPROM)
print("Dump length: "+str(BUF)+" (expected 200)")
#print(hex(EEPROM[ADDR_PRODUCT]))
BUF = EEPROM[ADDR_PRODUCT]
if BUF in PRODUCT:
  print("Product: "+PRODUCT[BUF])
else:
  print("Product: UNKNOWN ("+str(hex(BUF))+")")
BUF = EEPROM[ADDR_MODEL]
print("Model: "+str(hex(BUF)))
if BUF in models:
  print(models[BUF][3]+" "+models[BUF][4])

BUF = EEPROM[ADDR_HW_REV]
print("HW Revision: "+str(hex(BUF)))
BUF = EEPROM[ADDR_SERIAL:ADDR_SERIAL+4]
print("Serial: "+str(BUF.hex()))
BUF = EEPROM[ADDR_MADE:ADDR_MADE+4]
timestamp = struct.unpack(">I",BUF)[0]
date = datetime.fromtimestamp(timestamp)
BUF = date.strftime("%d%b%Y, %H:%M:%S %z")
print("Made: "+str(BUF))
BUF = EEPROM[ADDR_CHKSUM:ADDR_CHKSUM+16]
print("Stored Checksum:    "+str(BUF.hex()))
BUF = EEPROM[0x00:0x0B]
BUF = hashlib.md5(BUF).digest()
print("Generated Checksum: "+str(BUF.hex()))
BUF = EEPROM[ADDR_SIGNATURE:ADDR_SIGNATURE+128]
print("Signature: "+str(BUF.hex()))

BUF = EEPROM[ADDR_INFO_LOCK]
print("Info Lock: "+str(hex(BUF)))

BUF = EEPROM[ADDR_CONF_SF]
print("SF: "+str(hex(BUF)))
BUF = EEPROM[ADDR_CONF_CR]
print("CR: "+str(hex(BUF)))
BUF = EEPROM[ADDR_CONF_TXP]
print("TXP: "+str(hex(BUF)))
BUF = EEPROM[ADDR_CONF_BW:ADDR_CONF_BW+4]
print("BW: "+str(BUF.hex()))
BUF = EEPROM[ADDR_CONF_FREQ:ADDR_CONF_FREQ+4]
print("Freq: "+str(BUF.hex()))
BUF = EEPROM[ADDR_CONF_OK]
print("OK: "+str(hex(BUF)))
	
BUF = EEPROM[ADDR_CONF_BT]
print("BT: "+str(hex(BUF)))
BUF = EEPROM[ADDR_CONF_DSET]
print("DSET: "+str(hex(BUF)))
BUF = EEPROM[ADDR_CONF_DINT]
print("DINT: "+str(hex(BUF)))
BUF = EEPROM[ADDR_CONF_DADR]
print("DADR: "+str(hex(BUF)))

