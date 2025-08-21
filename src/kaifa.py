#
# Thanks to https://github.com/tirolerstefan/kaifa/blob/master/kaifareader.py
# for this really great work. This is basically a refactoring of this work
# to my needs...
#


import re
import binascii
from Cryptodome.Cipher import AES
from datetime import datetime

# TINETZ Supplier specific values
frame1_start_bytes_hex = '68fafa68'
frame1_start_bytes = b'\x68\xfa\xfa\x68'  # 68 FA FA 68
frame2_end_bytes = b'\x16'

frame2_start_bytes_hex = '68727268'
frame2_start_bytes = b'\x68\x72\x72\x68'  # 68 72 72 68
ic_start_byte = 23
enc_data_start_byte = 27



class DataType:
    NullData = 0x00
    Boolean = 0x03
    BitString = 0x04
    DoubleLong = 0x05
    DoubleLongUnsigned = 0x06
    OctetString = 0x09
    VisibleString = 0x0A
    Utf8String = 0x0C
    BinaryCodedDecimal = 0x0D
    Integer = 0x0F
    Long = 0x10
    Unsigned = 0x11
    LongUnsigned = 0x12
    Long64 = 0x14
    Long64Unsigned = 0x15
    Enum = 0x16
    Float32 = 0x17
    Float64 = 0x18
    DateTime = 0x19
    Date = 0x1A
    Time = 0x1B
    Array = 0x01
    Structure = 0x02
    CompactArray = 0x13

class ObisCodes:
    def to_bytes(code):
        return bytes([int(a) for a in code.split(".")])

    VoltageL1 = to_bytes("01.0.32.7.0.255")
    VoltageL2 = to_bytes("01.0.52.7.0.255")
    VoltageL3 = to_bytes("01.0.72.7.0.255")
    CurrentL1 = to_bytes("1.0.31.7.0.255")
    CurrentL2 = to_bytes("1.0.51.7.0.255")
    CurrentL3 = to_bytes("1.0.71.7.0.255")
    RealPowerIn = to_bytes("1.0.1.7.0.255")
    RealPowerOut = to_bytes("1.0.2.7.0.255")
    RealEnergyIn = to_bytes("1.0.1.8.0.255")
    RealEnergyOut = to_bytes("1.0.2.8.0.255")
    ReactiveEnergyIn = to_bytes("1.0.3.8.0.255")
    ReactiveEnergyOut = to_bytes("1.0.4.8.0.255")



# with help of @micronano
# https://www.photovoltaikforum.com/thread/157476-stromz%C3%A4hler-kaifa-ma309-welches-mbus-usb-kabel/?postID=2341069#post2341069
class EnergyData:
    def __init__(self, frame1, frame2, key):
        key = binascii.unhexlify(key)  # convert to binary stream
        systitle = frame1[11:19]  # systitle at byte 12, length 8

        ic = frame1[ic_start_byte:ic_start_byte+4]   # invocation counter length 4
        iv = systitle + ic   # initialization vector
        data_frame1 = frame1[enc_data_start_byte:len(frame1) - 2]  # start at byte 26 or 27 (dep on supplier), excluding 2 bytes at end: checksum byte, end byte 0x16
        data_frame2 = frame2[9:len(frame2) - 2]   # start at byte 10, excluding 2 bytes at end: checksum byte, end byte 0x16

        data_encrypted = data_frame1 + data_frame2
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        self._data_decrypted = cipher.decrypt(data_encrypted)
        self._data_decrypted_hex = binascii.hexlify(self._data_decrypted)

        # Parse data
        self._parse_all()

        # Set all values
        self.data = {}
        self.data["datetime"] = datetime.strftime(datetime.now(), "%d %B %Y %X")
        self.data["energy_in"] = round(self.obis[ObisCodes.RealEnergyIn] / 1000.0, 2)
        self.data["energy_out"] = round(self.obis[ObisCodes.RealEnergyOut] / 1000.0, 2)
        self.data["power_in"] = round(self.obis[ObisCodes.RealPowerIn] / 1000.0, 2)
        self.data["power_out"] = round(self.obis[ObisCodes.RealPowerOut] / 1000.0, 2)
        self.data["reactive_energy_in"] = round(self.obis[ObisCodes.ReactiveEnergyIn] / 1000.0, 2)
        self.data["reactive_energy_out"] = round(self.obis[ObisCodes.ReactiveEnergyOut] / 1000.0, 2)
        self.data["voltage_l1"] = round(self.obis[ObisCodes.VoltageL1], 2)
        self.data["voltage_l2"] = round(self.obis[ObisCodes.VoltageL2], 2)
        self.data["voltage_l3"] = round(self.obis[ObisCodes.VoltageL3], 2)
        self.data["current_l1"] = round(self.obis[ObisCodes.CurrentL1], 2)
        self.data["current_l2"] = round(self.obis[ObisCodes.CurrentL2], 2)
        self.data["current_l3"] = round(self.obis[ObisCodes.CurrentL3], 2)


    def __str__(self):
        return f"""
DateTime: \t {self.data["datetime"]}

EnergyIn: \t {self.data["energy_in"]} kWh
ReacEnergyIn: \t {self.data["reactive_energy_in"]} kWh
PowerIn: \t {self.data["power_in"]} kW

EnergyOut: \t {self.data["energy_out"]} kWh
ReacEnergyOut: \t {self.data["reactive_energy_out"]} kWh
PowerOut: \t {self.data["power_out"]} kW

VoltageL1: \t {self.data["voltage_l1"]} V
VoltageL2: \t {self.data["voltage_l2"]} V
VoltageL3: \t {self.data["voltage_l3"]} V
CurrentL1: \t {self.data["current_l1"]} A
CurrentL2: \t {self.data["current_l2"]} A
CurrentL3: \t {self.data["current_l3"]} A
        """

    def _parse_all(self):
        decrypted = self._data_decrypted
        pos = 0
        total = len(decrypted)
        self.obis = {}
        while pos < total:
            if decrypted[pos] != DataType.OctetString:
                pos += 1
                continue
            if decrypted[pos + 1] != 6:
                pos += 1
                continue
            obis_code = decrypted[pos + 2 : pos + 2 + 6]
            data_type = decrypted[pos + 2 + 6]
            pos += 2 + 6 + 1

            if data_type == DataType.DoubleLongUnsigned:
                value = int.from_bytes(decrypted[pos : pos + 4], "big")
                scale = decrypted[pos + 4 + 3]
                if scale > 128: scale -= 256
                pos += 2 + 8
                self.obis[obis_code] = value*(10**scale)
            elif data_type == DataType.LongUnsigned:
                value = int.from_bytes(decrypted[pos : pos + 2], "big")
                scale = decrypted[pos + 2 + 3]
                if scale > 128: scale -= 256
                pos += 8
                self.obis[obis_code] = value*(10**scale)
            elif data_type == DataType.OctetString:
                octet_len = decrypted[pos]
                octet = decrypted[pos + 1 : pos + 1 + octet_len]
                pos += 1 + octet_len + 2
                self.obis[obis_code] = octet


def _get_frames(serial, serial_read_chunk_size=100):
    # "telegram fetching loop" (as long as we have found two full telegrams)
    # frame1 = first telegram (68fafa68), frame2 = second telegram (68727268
    stream = b''      # filled by serial device
    frame1 = b''      # parsed telegram1
    frame2 = b''      # parsed telegram2
    frame1_start_pos = -1          # pos of start bytes of telegram 1 (in stream)
    frame2_start_pos = -1          # pos of start bytes of telegram 2 (in stream)

    while True:
        # Read in chunks. Each chunk will wait as long as specified by
        # serial timeout. As the meters we tested send data every 5s the
        # timeout must be <5. Lower timeouts make us fail quicker.
        byte_chunk = serial.read(size=serial_read_chunk_size)
        stream += byte_chunk
        frame1_start_pos = stream.find(frame1_start_bytes)
        frame2_start_pos = stream.find(frame2_start_bytes)

        # fail as early as possible if we find the segment is not complete yet.
        if (
           (stream.find(frame1_start_bytes) < 0) or
           (stream.find(frame2_start_bytes) <= 0) or
           (stream[-1:] != frame2_end_bytes) or
           (len(byte_chunk) == serial_read_chunk_size)
           ):
            continue

        if (frame2_start_pos != -1):
            # frame2_start_pos could be smaller than frame1_start_pos
            if frame2_start_pos < frame1_start_pos:
                # start over with the stream from frame1 pos
                stream = stream[frame1_start_pos:len(stream)]
                continue

            # we have found at least two complete telegrams
            regex = binascii.unhexlify('28'+frame1_start_bytes_hex+'7c'+frame2_start_bytes_hex+'29')  # re = '(..|..)'
            l = re.split(regex, stream)
            l = list(filter(None, l))  # remove empty elements
            # l after split (here in following example in hex)
            # l = ['68fafa68', '53ff00...faecc16', '68727268', '53ff...3d16', '68fafa68', '53ff...d916', '68727268', '53ff.....']

            # take the first two matching telegrams
            for i, el in enumerate(l):
                if el == frame1_start_bytes:
                    frame1 = l[i] + l[i+1]
                    frame2 = l[i+2] + l[i+3]
                    break

            # check for weird result -> exit
            if (len(frame1) == 0) or (len(frame2) == 0):
                raise Exception("Unknown result")

            break

    return frame1, frame2


def read_energy_data(serial, key) -> EnergyData:
    frame1, frame2 = _get_frames(serial)
    return EnergyData(frame1, frame2, key)
