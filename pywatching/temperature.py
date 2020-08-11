import smbus

bus = smbus.SMBus(1)

bus_addr = 0x48
config_reg_addr = 0x30
config_reg_val = 0xa0 # 16bit ONE-SHOT
temperature_msb_reg_addr = 0x00

bus.write_word_data(bus_addr, config_reg_addr, config_reg_val)
wdata = bus.read_word_data(bus_addr, temperature_msb_reg_addr)

data = (wdata & 0xff00) >> 8 | (wdata & 0xff) << 8

print(data/128.)
