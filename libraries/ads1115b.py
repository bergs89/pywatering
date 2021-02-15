# code is a rework of Guido Lutterbach ADS1115Runner
# http://smartypies.com/projects/ads1115-with-raspberrypi-and-python/ads1115runner/

import cmd, time, logging, smbus, RPi.GPIO as GPIO, numpy as np

# ADS1115 + hardware constants
I2C_BUS = 0
DEVICE_ADDRESS = 0x48
POINTER_CONVERSION = 0x0
POINTER_CONFIGURATION = 0x1
POINTER_LOW_THRESHOLD = 0x2
POINTER_HIGH_THRESHOLD = 0x3

RESET_ADDRESS = 0b0000000
RESET_COMMAND = 0b00000110

# Open I2C device
BUS = smbus.SMBus(I2C_BUS)
BUS.open(I2C_BUS)

ALERTPIN = 27


def swap2Bytes(c):
    '''Revert Byte order for Words (2 Bytes, 16 Bit).'''
    return (c >> 8 | c << 8) & 0xFFFF


def prepareLEconf(BEconf):
    '''Prepare LittleEndian Byte pattern from BigEndian configuration string, with separators.'''
    c = int(BEconf.replace('-', ''), base=2)
    return swap2Bytes(c)


def LEtoBE(c):
    '''Little Endian to BigEndian conversion for signed 2Byte integers (2 complement).'''
    c = swap2Bytes(c)
    if (c >= 2 ** 15):
        c = c - 2 ** 16
    return c


def BEtoLE(c):
    '''BigEndian to LittleEndian conversion for signed 2 Byte integers (2 complement).'''
    if (c < 0):
        c = 2 ** 16 + c
    return swap2Bytes(c)


def resetChip():
    BUS.write_byte(RESET_ADDRESS, RESET_COMMAND)
    return


# Use BCM GPIO references
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALERTPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  ## read mode, pull up resistor


class ADS1115(cmd.Cmd):
    intro = '''usage: type following commands
          1    - one-shot measurement mode, timed
          2    - one-shot measurement mode, alerted through GPIO
          3    - continuous measurment mode, alerted through GPIO
          4  low high  - continuous mode, alerted when value out of range [low, high]
          q (quit)
          just hitting enter quits any mode 1-4. Enter 'y' to continue in modes 1 and 2.'''
    prompt = 'Enter 1,2,3,4 or q >>'
    file = None

    #    __logfile = None

    def alerted(self, arg):
        data_raw = BUS.read_word_data(DEVICE_ADDRESS, POINTER_CONVERSION)
        print('alerted:' + str(LEtoBE(data_raw)))
        return

    def single_read(self, arg):
        '''One-shot, Read value from channel 0 with wait time'''
        resetChip()
        # compare with configuration settings from ADS115 datasheet
        # start single conversion - AIN2/GND - 4.096V - single shot - 8SPS - X
        # - X - X - disable comparator
        conf = prepareLEconf('1-110-001-1-000-0-0-0-11')
        BUS.write_word_data(DEVICE_ADDRESS, POINTER_CONFIGURATION, conf)
        # long enough to be safe that data acquisition (conversion) has completed
        # may be calculated from data rate + some extra time for safety.
        # check accuracy in any case.
        time.sleep(0.2)
        value_raw = BUS.read_word_data(DEVICE_ADDRESS, POINTER_CONVERSION)
        value = LEtoBE(value_raw)
        return value

    def continuous_read(self, timeout):
        '''One-shot, Read value from channel 0 with wait time'''
        resetChip()
        # compare with configuration settings from ADS115 datasheet
        # start single conversion - AIN2/GND - 4.096V - single shot - 8SPS - X
        # - X - X - disable comparator
        conf = prepareLEconf('1-110-001-1-000-0-0-0-11')
        values = []
        start_time = time.time()
        runtime = 0
        while True and runtime < timeout:
            BUS.write_word_data(DEVICE_ADDRESS, POINTER_CONFIGURATION, conf)
            # long enough to be safe that data acquisition (conversion) has completed
            # may be calculated from data rate + some extra time for safety.
            # check accuracy in any case.
            time.sleep(0.2)
            value_raw = BUS.read_word_data(DEVICE_ADDRESS, POINTER_CONVERSION)
            value = LEtoBE(value_raw)
            values.append(value)
            runtime = time.time() - start_time
        values_array = np.array(values)
        return values_array

    def do_q(self, arg):
        '''Quit.'''
        return True

    def default(self, line):
        print('undefined key')

    def shutdown(self):
        GPIO.cleanup()
        BUS.close()
        pass

if __name__ == "__main__":
    try:
        logging.basicConfig(
            level=logging.DEBUG,
            #format='%(name)-12s: %(levelname)-8s %(message)s')
            format='%(message)s')
        logger = logging.getLogger('ADS1115Runner')
        value = ADS1115().single_read(0)
	values = ADS1115().continuous_read(0.25)
        print(value)
	print(values)
    finally:
        ADS1115().shutdown()
