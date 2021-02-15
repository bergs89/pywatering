bus = smbus.SMBus(1)

data = [0xC4,0x83]
bus.write_i2c_block_data(0x48, 0x01, data)
data = bus.read_i2c_block_data(0x48, 0x00, 2)
raw_adc = data[0] * 256 + data[1]
if raw_adc > 32767:
	raw_adc -= 65535
# Output data to screen
print "Digital Value of Analog Input on Channel-0: %d" %raw_adc

data = [0xD4,0x83]
bus.write_i2c_block_data(0x48, 0x01, data)
# ADS1115 address, 0x48(72)
# Read data back from 0x00(00), 2 bytes
# raw_adc MSB, raw_adc LSB
data = bus.read_i2c_block_data(0x48, 0x00, 2)
# Convert the data
raw_adc = data[0] * 256 + data[1]
if raw_adc > 32767:
	raw_adc -= 65535
# Output data to screen
print "Digital Value of Analog Input on Channel-1: %d" %raw_adc

# ADS1115 address, 0x48(72)
# Select configuration register, 0x01(01)
#		0xE483(58499)	AINP = AIN2 and AINN = GND, +/- 2.048V
#				Continuous conversion mode, 128SPS
data = [0xE4,0x83]
bus.write_i2c_block_data(0x48, 0x01, data)
# ADS1115 address, 0x48(72)
# Read data back from 0x00(00), 2 bytes
# raw_adc MSB, raw_adc LSB
data = bus.read_i2c_block_data(0x48, 0x00, 2)
# Convert the data
raw_adc = data[0] * 256 + data[1]

if raw_adc > 32767:
	raw_adc -= 65535

# Output data to screen
print "Digital Value of Analog Input on Channel-2: %d" %raw_adc

# ADS1115 address, 0x48(72)
# Select configuration register, 0x01(01)
#		0xF483(62595)	AINP = AIN3 and AINN = GND, +/- 2.048V
#				Continuous conversion mode, 128SPS
data = [0xF4,0x83]
bus.write_i2c_block_data(0x48, 0x01, data)
# ADS1115 address, 0x48(72)
# Read data back from 0x00(00), 2 bytes
# raw_adc MSB, raw_adc LSB
data = bus.read_i2c_block_data(0x48, 0x00, 2)
# Convert the data
raw_adc = data[0] * 256 + data[1]
if raw_adc > 32767:
	raw_adc -= 65535

# Output data to screen
print "Digital Value of Analog Input on Channel-3: %d" %raw_adc