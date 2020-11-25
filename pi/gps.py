import time
import L76X
import math


class Gps:
    def __init__(self):
        self.x = L76X.L76X()
        self.x.L76X_Set_Baudrate(9600)
        self.x.L76X_Send_Command(self.x.SET_NMEA_BAUDRATE_115200)
        time.sleep(2)
        self.x.L76X_Set_Baudrate(115200)
        self.x.L76X_Send_Command(self.x.SET_POS_FIX_400MS)
        # Set output message
        self.x.L76X_Send_Command(self.x.SET_NMEA_OUTPUT)
        self.x.L76X_Exit_BackupMode()

    def get_gps(self):
        self.x.L76X_Gat_GNRMC()
        if self.x.Status == 1:
            print('Already positioned')
        else:
            print('No positioning')
            return ""
        print('Time %d:' % self.x.Time_H)
        print('%d:' % self.x.Time_M)
        print('%d' % self.x.Time_S)
        print('Lon = %f' % self.x.Lon)
        print('Lat = %f' % self.x.Lat)
        self.x.L76X_Baidu_Coordinates(self.x.Lat,self.x.Lon)
        print('Baidu coordinate %f' % self.x.Lat_Baidu)
        print(',%f' % self.x.Lon_Baidu)
        res = 'Time %d:%d:%d. \n Lon = %f, Lat = %f \n Baidu coordinate %f, %f.'.format(self.x.Time_H, self.x.Time_M, self.x.Time_S, self.x.Lon, self.x.Lat, self.x.Lat_Baidu, self.x.Lon_Baidu)
        return res