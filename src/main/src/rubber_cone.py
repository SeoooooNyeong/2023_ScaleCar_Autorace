#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import rospy

from std_msgs.msg import Int32, String, Float32
from sensor_msgs.msg import Image 
from obstacle_detector.msg import Obstacles

class ClusterLidar :

    def __init__(self) :
        # subscriber: raw_obstacles를 받아 조향각을 구함
        rospy.Subscriber("/raw_obstacles", Obstacles, self.rubber_callback)
        # publisher: 조향각을 전달함
        self.rabacon_pub = rospy.Publisher("rubber_cone", Float32, queue_size = 5)
        self.angle = 0.0 


    def rubber_callback(self, _data):
        # 감지된 장애물을 왼쪽, 오른쪽으로 나누어 리스트에 저장함
        left_rabacon = []
        right_rabacon = []
        for i in _data.circles :
            if -1.7 < i.center.x < 0  :
                if 0 < i.center.y < 1 :    # 차량의 왼쪽 앞 장애물
                    left_rabacon.append(i)
                elif -1 < i.center.y < 0 : # 차량의 오른쪽 앞 장애물
                    right_rabacon.append(i)

        if len(left_rabacon) >= 1 and len(right_rabacon) >= 1:
            left_close_rabacon = sorted(left_rabacon, key = lambda x : -x.center.x)[0]
            right_close_rabacon = sorted(right_rabacon, key = lambda x : -x.center.x)[0]
            raba = (left_close_rabacon.center.y + right_close_rabacon.center.y)
            self.rabacon_pub.publish(raba)
        else :
            self.rabacon_pub.publish(1000.0)


def run():
    rospy.init_node("rubber_drive")
    cluster = ClusterLidar()
    rospy.spin()


if __name__ == '__main__':
    run()