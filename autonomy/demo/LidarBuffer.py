import serial
import threading
import time
import math


class LidarBuffer:
    def __init__(self, serial):
        self.ser = serial
        self.listen_thread = threading.Thread(target=self.listen)
        self.running = False
        self.buffer = []

    def __del__(self):
        self.stop_listening()

    def start_listening(self):
        self.running = True
        self.listen_thread.start()

    def stop_listening(self):
        self.running = False

    def listen(self):
        while self.running:
            try:
                print('a')
                measurements = self.ser.readline().strip().decode()
                print('b')
                measurements = measurements.split()
                print(measurements)
                print('c')

                if measurements[0] == -1:
                    # lidar lite didn't read properly
                    continue

                dist = float(measurements[0]) / 100   # dist in cm, want m
                theta = math.radians(int(measurements[1]))
                phi = math.radians(int(measurements[2]))
                self.buffer.append((dist, theta, phi))
            except ValueError:
                # Something's gone wrong with lidar lite
                print('Lidar Lite error.')

    def get_buffer(self):
        '''
        Return buffer containing points that have been read since the last
        buffer read.

        Returns:
            buff: array of distance readings in metres with associated theta and phi.
                [(dist1, theta1, phi1), (dist2, theta2, phi2) etc.]
        '''
        buff = self.buffer
        self.buffer = []

        return buff


if __name__ == '__main__':
    l = LidarBuffer(serial.Serial('/dev/ttyUSB0', 115200))
    l.start_listening()
    time.sleep(5)
    print(l.get_buffer())
    l.stop_listening()
