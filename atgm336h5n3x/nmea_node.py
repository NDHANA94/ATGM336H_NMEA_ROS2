#!/usr/bin/env python3
"""
    * Author: nipun.dhananjaya@gmail.com
    * Created: 25.05.2023
"""

from atgm336h5n3x.atgm336h_serial import ATGM336H_Serial
from rclpy.node import Node
import rclpy
from nmea_msgs.msg import Gpgga, Gpgsa, Gpgsv, GpgsvSatellite, Gprmc, Sentence
import serial
from time import time
import argparse
import numpy as np
from  std_msgs.msg import Int8MultiArray


"""
$GPGSA: GPS DOP and Active Satellites

$GPGSV: GPS Satellites in View

$GPTXT: General Purpose Text Transmission

$GNGLL: Geographic Position - Latitude/Longitude
     | $GNGLL | lat | lat dir | lon | lon gir | utc | data status | mode ind | *xx | [CR][LF] |

$GNGGA: Global Navigation Satellite System Fix Data

$GNRMC: Recommended Minimum Specific GPS/Transit Data

$GNVTG: Course Over Ground and Ground Speed

$GNZDA: Time and Date

$BDGSA: Beidou DOP and Active Satellites

$BDGSV: Beidou Satellites in View

"""

class GPS(Node):
    def __init__(self, atgm366h:ATGM336H_Serial, dev:str):
        super().__init__('gps_node')
        self.gpgga_pub = self.create_publisher(Gpgga, 'gps/gpgga', 10)
        self.gpgsa_pub = self.create_publisher(Gpgsa, 'gps/gpgsa', 10)
        self.gpgsv_pub = self.create_publisher(Gpgsv, 'gps/gpgsv', 10)
        # self.gpgsvSat_pub = self.create_publisher(GpgsvSatellite, 'gps/gpgsvSat', 10)
        self.gprmc_pub = self.create_publisher(Gprmc, 'gps/gprmc', 10)
        self.sentence_pub = self.create_publisher(Sentence, 'gps/sentence', 20)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback_gps)
        self.atgm = atgm366h
        self.atgm.connect(dev)

    def timer_callback_gps(self):
        if self.gpgga_pub.get_subscription_count() > 0:
            gpgga = Gpgga()
            data = self.atgm.read_data("$GNGGA") 
            if data != False and len(data) ==14:
                gpgga.header.stamp = self.get_clock().now().to_msg()
                gpgga.header.frame_id = 'gps'
                gpgga.utc_seconds = np.float64(data[0]) if data[0] != '' else np.nan
                gpgga.lat = np.float64(data[1]) if data[1] != '' else np.nan
                gpgga.lat_dir = data[2] 
                gpgga.lon = np.float64(data[3]) if data[3] != '' else np.nan
                gpgga.lon_dir = data[4] 
                if not data[5] == '': gpgga.gps_qual = int(data[5])
                if not data[6] == '': gpgga.num_sats = int(data[6])
                gpgga.hdop = float(data[7]) if data[7] != '' else np.nan
                gpgga.alt = float(data[8]) if data[8] != '' else np.nan
                gpgga.altitude_units = data[9]
                gpgga.undulation = float(data[10]) if data[10] != '' else np.nan
                gpgga.undulation_units = data[11]
                if not data[12] == '': gpgga.diff_age = int(data[12])
                gpgga.station_id = data[13]
                self.gpgga_pub.publish(gpgga)

        if self.gpgsa_pub.get_subscription_count() > 0:
            gpgsa = Gpgsa()
            data = self.atgm.read_data("$GPGSA")
            if data != False and len(data) == 17:
                gpgsa.header.stamp = self.get_clock().now().to_msg()
                gpgsa.header.frame_id = 'gps'

                # gpgsa.message_id = 
                gpgsa.auto_manual_mode = data[0]
                if not data[1] == '': gpgsa.fix_mode = int(data[1])
                sv_ids = []
                for d in data[2:14]:
                    if d != '': sv_ids.append(int(d))
                gpgsa.sv_ids = sv_ids
                gpgsa.pdop = float(data[14]) if data[14] != '' else np.nan
                gpgsa.hdop = float(data[15]) if data[15] != '' else np.nan
                gpgsa.vdop = float(data[16]) if data[16] != '' else np.nan
                self.gpgsa_pub.publish(gpgsa)

        if self.gpgsv_pub.get_subscription_count() > 0:
            gpgsv = Gpgsv()
            gpgsvSats = []
            gpgsv.header.stamp = self.get_clock().now().to_msg()
            gpgsv.header.frame_id = 'gps'
            data = self.atgm.read_data("$GPGSV")
            if data != False:
                sats_in_msg =  int((len(data) - 3)/4)

                # gpgsv.message_id = 
                if not data[0] == '': gpgsv.n_msgs = int(data[0]) 
                if not data[1] == '': gpgsv.msg_number = int(data[1])
                if not data[2] == '': gpgsv.n_satellites = int(data[2])    
                if sats_in_msg > 0:
                    sat1 = GpgsvSatellite()
                    if not data[3] == '': sat1.prn = int(data[3])
                    if not data[4] == '': sat1.elevation = int(data[4])
                    if not data[5] == '': sat1.azimuth = int(data[5])
                    if not data[6] == '': sat1.snr = int(data[6])
                    gpgsvSats.append(sat1)
                if sats_in_msg > 1:
                    sat2 = GpgsvSatellite()
                    if not data[7] == '': sat2.prn = int(data[7])
                    if not data[8] == '': sat2.elevation = int(data[8])
                    if not data[9] == '': sat2.azimuth = int(data[9])
                    if not data[10] == '': sat2.snr = int(data[10])
                    gpgsvSats.append(sat2)
                if sats_in_msg > 2:
                    sat3 = GpgsvSatellite()
                    if not data[11] == '': sat3.prn = int(data[11])
                    if not data[12] == '': sat3.elevation = int(data[12])
                    if not data[13] == '': sat3.azimuth = int(data[13])
                    if not data[14] == '': sat3.snr = int(data[14])
                    gpgsvSats.append(sat3)
                if sats_in_msg > 3:
                    sat4 = GpgsvSatellite()
                    if not data[15] == '': sat4.prn = int(data[15])
                    if not data[16] == '': sat4.elevation = int(data[16])
                    if not data[17] == '': sat4.azimuth = int(data[17])
                    if not data[18] == '': sat4.snr = int(data[18])
                    gpgsvSats.append(sat4)

                if sats_in_msg>0:
                    gpgsv.satellites = gpgsvSats
                self.gpgsv_pub.publish(gpgsv)

        if self.gprmc_pub.get_subscription_count() > 0:
            gprmc = Gprmc()
            gprmc.header.stamp = self.get_clock().now().to_msg()
            gprmc.header.frame_id = 'gps'
            data = self.atgm.read_data("$GNRMC")
            if data != False and len(data) == 12:
                # gprmc.message_id
                gprmc.utc_seconds = np.float64(data[0]) if data[0] != '' else np.nan
                gprmc.position_status = data[1] 
                gprmc.lat = np.float64(data[2]) if data[2] != '' else np.nan
                gprmc.lat_dir = data[3]
                gprmc.lon = np.float64(data[4]) if data[4] != '' else np.nan 
                gprmc.lon_dir = data[5]
                gprmc.speed = float(data[6]) if data[6] != '' else np.nan
                gprmc.track = float(data[7]) if data[7] != '' else np.nan
                gprmc.date = data[8]
                gprmc.mag_var = float(data[9]) if data[9] != '' else np.nan
                gprmc.mag_var_direction = data[10]
                gprmc.mode_indicator = data[11]
                
                self.gprmc_pub.publish(gprmc)

        if self.sentence_pub.get_subscription_count() > 0:
            sentence = Sentence()
            sentence.header.stamp = self.get_clock().now().to_msg()
            sentence.header.frame_id = 'gps'
            sentence.sentence = self.atgm.ser.readline().decode('ascii')
            self.sentence_pub.publish(sentence)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev')
    args_ = parser.parse_args()
    dev = args_.dev
    
    rclpy.init(args=args)
    atgm = ATGM336H_Serial()
    gps_publisher = GPS(atgm366h=atgm, dev=dev)
    rclpy.spin(gps_publisher)
    atgm.disconnect()
    gps_publisher.destroy_node()
    rclpy.shutdown()
   

    


if __name__ == '__main__':
    main()
