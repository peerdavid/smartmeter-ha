import argparse
import serial
import time

from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator
from gurux_dlms.GXDLMSTranslatorMessage import GXDLMSTranslatorMessage
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description='Integrate your smartmeter into HomeAssistant.')
parser.add_argument('--port', default="/dev/ttyUSB0", help='Port of M-BUS to USB adapter.')
parser.add_argument('--key', required=True, help='The key of your smartmeter. See also https://www.netz-noe.at/Download-(1)/Smart-Meter/218_9_SmartMeter_Kundenschnittstelle_lektoriert_14.aspx')

args = parser.parse_args()


def main():
    tr = GXDLMSTranslator()
    tr.blockCipherKey = GXByteBuffer(args.key)
    tr.comments = True
    ser = serial.Serial(
        port=args.port,
        baudrate=2400,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
    )

    while(True):
        try:
            data = ser.read(size=282).hex()
            print(len(data))
            time.sleep(1000)
        except:
            print("(Error) Could not read data from your smartmeter.")


if __name__ == "__main__":
    main()