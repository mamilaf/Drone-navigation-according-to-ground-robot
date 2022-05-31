
import math
from queue import PriorityQueue
import base64
import cv2 as cv
import numpy as np
import imutils as imutils
import time
from time import sleep
import rclpy
from rclpy.node import Node
import sys
from std_msgs.msg import Empty
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from geometry_msgs.msg import Twist
#define repeating parameters
i =0
ERROR = 0.2
SPEED = 0.2
ERROR_z = 0.00001

class CamSubscriber(Node):
	def __init__(self):
		super().__init__('image_face_listener')
		self.count_dist = 0
		self.cnt = 0
		self.init = 0
		self.area=0
		self.x = 0
		self.y = 0
		self.i = 0
		self.z= 0
		self.zi = 0
		self.zf = 0
		self.xi =0
		self.yi =0
		self.xf = 0
		self.yf = 0
		self.xd = 0
		self.yd = 0
		self.zd = 0
		self.xa = []
		self.ya = []
		self.onlyonce = 1
		self.got_points = 0
		self.final = 1
		self.stop = 0
		self.drone1_takeoff_pub = self.create_publisher(Empty, '/drone1/takeoff', 10)
		self.drone1_land_pub = self.create_publisher(Empty, '/drone1/land', 10)
		self.drone1_vel_pub = self.create_publisher(Twist, '/drone1/cmd_vel', 10)
		self.drone1_sub_odom = self.create_subscription(Odometry, '/odom', self.drone1_odom, 10)

		
		
	def drone1_odom(self, msg):
		msg2 = Twist()
		self.x = int(msg.pose.pose.position.x)
		self.y = int(msg.pose.pose.position.y)
		self.z = msg.pose.pose.orientation.x
		# get the coordinates saved for the start and end points
		graph_data = open('cordinates_tello.csv','r').read()
		lines = graph_data.split('\n')
		for line in lines[1:]:
			if len(line)>1:
				xi , yi, zi , xf, yf , zf = line.split(' ')
				self.zd = float(zf)
		# get the shortest path points
		graph_data = open('pathvalues.csv','r').read()
		lines = graph_data.split('\n')
		for line in lines[1:]:
			if len(line)>1:
				xdc , ydc = line.split(',')
				self.xa.append(xdc)
				self.ya.append(ydc)
		if self.i ==0:
			self.xd = int(self.xa[i])
			self.yd = int(self.ya[i])

		if self.path_achieved ==1:
			self.i += 1
			self.xd = int(self.xa[i])
			self.yd = int(self.ya[i])
			self.path_achieved = 0

		msg2 = Twist()

		
		msg2.linear.x = 0.0
		msg2.linear.y = 0.0
		msg2.angular.z = 0.0
		# check for orientation correction
		if self.z < self.zd - ERROR_z :
			msg2.angular.z = -SPEED
			msg2.linear.x = 0.0
			msg2.linear.y = 0.0
			

		elif self.z > self.zd + ERROR_z :
			msg2.angular.z = SPEED
			msg2.linear.x = 0.0
			msg2.linear.y = 0.0
			

		elif self.z > self.zd - ERROR_z and self.z < self.zd + ERROR_z:
			# print("z adjusted")
			#check for x coordinate correction

			if self.x < self.xd - ERROR :
				msg2.linear.x = SPEED
				msg2.linear.y = 0.0
				msg2.angular.z = 0.0
				

			elif self.x > self.xd + ERROR :
				msg2.linear.x = -SPEED
				msg2.linear.y = 0.0
				msg2.angular.z = 0.0
			
			elif self.x > self.xd - ERROR and self.x < self.xd + ERROR:
				

				#check for y coordinate correction
				if self.y < self.yd - ERROR :
					msg2.linear.y = SPEED
					msg2.linear.x = 0.0
					
					msg2.angular.z = 0.0

				elif self.y > self.yd + ERROR :
					msg2.linear.y = -SPEED
					msg2.linear.x = 0.0
					
					msg2.angular.z = 0.0

				elif self.y > self.yd - ERROR and self.y < self.yd + ERROR:
					self.path_achieved = 1
					
					

			
		msg2.angular.x = 0.0
		msg2.angular.y = 0.0
		msg2.linear.z = 0.0

		# publish
		self.drone1_vel_pub.publish(msg2)
	

	








	#takeoff function
	def takeoff_drone1(self):
		msg = Empty()
		for i in range(20):
			print("Taking off")
			self.drone1_takeoff_pub.publish(msg)
			time.sleep(0.1)
	#land function
	def land_drone1(self):
		msg = Empty()
		for i in range(5):
			self.drone1_land_pub.publish(msg)
			time.sleep(0.1)
	
####################################################################################################











def main():
    rclpy.init()
    print('points',  file=open('cordinates_tello.csv', 'w'))
    # print('pixels',  file=open('face_pixel_size_tello.csv', 'w'))
    image_face_listener = CamSubscriber()

    # Spin until ctrl + c
    rclpy.spin(image_face_listener)

    image_face_listener.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
