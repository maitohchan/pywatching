import smbus
import json
import os

from .date import Date


class Temperature(object):

    I2C_BUS_ADDRESS = 0x48
    CONFIGULATION_REGISTER_ADDRESS = 0x30
    TEMPERATURE_MSB_REGISTER_ADDRESS = 0x00
    # 16bit ONE-SHOT
    CONFIGULATION_REGISTER_VALUE = 0xa0

    def __init__(self, filename: str):
        self.__bus = smbus.SMBus(1)
        self.__filename = filename
        if os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump(dict(), f)


    def __get(self) -> float:
        bus.write_word_data(I2C_BUS_ADDRESS, CONFIGULATION_REGISTER_ADDRESS, CONFIGULATION_REGISTER_VALUE)
        wdata = bus.read_word_data(I2C_BUS_ADDRESS, TEMPERATURE_MSB_REGISTER_ADDRESS)
        data = (wdata & 0xff00) >> 8 | (wdata & 0xff) << 8
        return data/128.

    def __record(self):
        with open(self.__filename 'r') as f:
            data = json.load(f)
        
        data[Date().datetime()] = self.__get()
