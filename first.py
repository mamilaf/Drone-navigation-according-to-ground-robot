#! /usr/bin/python
import base64
import cv2 as cv
import numpy as np
import imutils as imutils

import rclpy
from rclpy.node import Node
import sys
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class CamSubscriber(Node):
    def __init__(self):
        super().__init__('image_face_listener')
        self.cnt = 0
        self.init = 0
                            # initialize the variables to collect the coordinates
        self.x = 0
        self.y = 0
        self.xi =0
        self.yi =0
        self.xf = 0
        self.yf = 0
        self.onlyonce = 1
        self.got_points = 0
        self.jetbot_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)  # topic to publish velocity commands to the jetbot
        self.odom_request = self.create_subscription(Odometry, '/odom', self.jetbot_odom, 10)
    def jetbot_odom(self, msg):
        msg2 = Twist()
        #store the positioning data every loop
        self.x = int(msg.pose.pose.position.x)  
        self.y = int(msg.pose.pose.position.y)
        self.z = msg.pose.pose.orientation.x
        # initialising starting points
        if self.init == 0:
            self.xi = self.x
            self.yi = self.y
            self.zi = self.z

            self.init = 1

        #predefined path for the jetbot
        elif self.cnt <= 300: 
            msg2.linear.x = 0.5
            msg2.linear.y = 0.0
            self.jetbot_vel_pub.publish(msg2)
        elif self.cnt <= 380:
            msg2.linear.x =0.0
            msg2.linear.y = 0.0
            msg2.angular.z = 0.5
            self.jetbot_vel_pub.publish(msg2)
        elif self.cnt <= 600:
            msg2.linear.x =0.5
            msg2.linear.y = 0.0
            msg2.angular.z = 0.0
            self.jetbot_vel_pub.publish(msg2)
        else:
            msg2.linear.x =0.0
            msg2.linear.y = 0.0
            msg2.angular.z = 0.0
            self.jetbot_vel_pub.publish(msg2)
            self.xf = self.x
            self.yf = self.y
            self.zf = self.z
            self.got_points=1
        self.cnt +=1
        # save the start and end coordinates to csv
        if self.got_points == 1 and self.onlyonce == 1:
            self.onlyonce = 0
            print("entered")
            print(self.xi,self.yi,self.xf,self.yf)
            print(int(self.xi),int(self.yi),self.zi,int(self.xf),int(self.yf), self.zf,  file=open('cordinates_tello.csv','a'))
                    

        

        
        
     




 


def main():
    rclpy.init()
    print('points',  file=open('cordinates.csv', 'w'))
    image_face_listener = CamSubscriber()

    # Spin until ctrl + c
    rclpy.spin(image_face_listener)

    image_face_listener.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()