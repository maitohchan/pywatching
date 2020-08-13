import smbus
import json
import os

from pywatching.date import Date


class Temperature(object):
    """Temperature class to measure temperature with sensor.

    Args:
        filename (str): file name to record temperature
        outdir (str): output directory for tempeature file
    Attributes:
        bus (smbus.SMBus): I2C bus
    """

    I2C_BUS_ADDRESS = 0x48
    CONFIGULATION_REGISTER_ADDRESS = 0x30
    TEMPERATURE_MSB_REGISTER_ADDRESS = 0x00
    CONFIGULATION_REGISTER_ONESHOT_16BIT = 0xA0

    def __init__(self, outdir: str = "."):
        self.__bus = smbus.SMBus(1)
        self.__outdir = outdir

    def __get(self) -> float:
        """Get temperature from sensor.

        Returns:
            float: temperature
        """
        self.__bus.write_word_data(
            self.I2C_BUS_ADDRESS,
            self.CONFIGULATION_REGISTER_ADDRESS,
            self.CONFIGULATION_REGISTER_ONESHOT_16BIT,
        )
        wdata = self.__bus.read_word_data(
            self.I2C_BUS_ADDRESS, self.TEMPERATURE_MSB_REGISTER_ADDRESS
        )
        data = (wdata & 0xFF00) >> 8 | (wdata & 0xFF) << 8
        return data / 128.0

    def record(self):
        """Record temperature in file
        """
        filepath = os.path.join(
            self.__outdir, "temperature_" + Date().date.replace("/", "") + ".json"
        )

        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
        else:
            data = dict()

        data[Date().time] = self.__get()

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    t = Temperature()
    t.record()
