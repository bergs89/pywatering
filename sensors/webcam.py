import time
import os


def get_picture(picture_path):
    command = 'fswebcam -r 640x480 --jpeg --save ' + picture_path
    os.system(command)  # uses Fswebcam to take picture


def get_picture_indefinetely(picture_path):
    while True:  # do forever
        get_picture(picture_path)
        time.sleep(1800)


if __name__ == "__main__":
    get_picture_indefinetely('/home/pi/test_picture.jpg')
