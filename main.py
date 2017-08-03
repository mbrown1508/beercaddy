__author__ = 'Matthew'

import requests
from robot import Robot
import time
import serial
import traceback

import logging
logging.basicConfig(filename='../beercaddy.log', level=logging.DEBUG)


def read_serial_message():
    recieved_data = []

    byte = ser.read()

    if byte == b'\x3A':
        length = int.from_bytes(ser.read(), byteorder='big')
        command = int.from_bytes(ser.read(), byteorder='big')

        logging.debug('Message Length: {}'.format(length))
        logging.debug('Message Command: {}'.format(command))

        for _ in range(length):
            recieved_data.append(ser.read())

        checksum = ser.read()

    else:
        logging.debug('Received unexpected character - {}'.format(int.from_bytes(byte, byteorder='big')))
        return

    string_message = ''.join([x.decode('ascii') for x in recieved_data])

    if checksum != b'\x01':
        logging.debug('Checksum Failed - {} - {}'.format(command + string_message, checksum.decode('ascii')))
        return

    if command == 0:
        logging.debug('Log Message - ' + string_message)
    else:
        logging.debug('Command Not Found - ' + string_message)


if __name__ == '__main__':
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)

        while True:
            read_serial_message()

    except Exception:
        logging.warning(traceback.format_exc())
