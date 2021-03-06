import datetime
import time
import matplotlib.pyplot as plt

from sensors.libraries import bme280


def save_plot_as_pic(x, y, figname):
    plt.figure()
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.savefig(figname)
    plt.close('all')


def store_env_data_indefinetely():
    temperature_list = []
    pressure_list = []
    humidity_list = []
    time_list = []
    while True:
        temperature, pressure, humidity = bme280.readBME280All()
        temperature_list.append(temperature)
        pressure_list.append(pressure)
        humidity_list.append(humidity)
        time_list.append(datetime.datetime.now())
        save_plot_as_pic(time_list, temperature_list, 'data/temperature_plot.jpg')
        save_plot_as_pic(time_list, pressure_list, 'data/pressure_plot.jpg')
        save_plot_as_pic(time_list, humidity_list, 'data/humidity_plot.jpg')
        time.sleep(1)
        # time.sleep(3600)

if __name__=="__main__":
    store_env_data_indefinetely()
