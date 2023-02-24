#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

PI = 3.1415926535897

class movement :

    def __init__(self):
        rospy.init_node('move_robot_node', anonymous=False)
        self.pub_move = rospy.Publisher("/cmd_vel",Twist,queue_size=10)
        self.move = Twist()

    def publish_vel(self):
        self.pub_move.publish(self.move)

    def move_forward(self):        
        self.move.linear.x=1
        self.move.angular.z=0.0

    def move_backward(self):      
        self.move.linear.x=-2
        self.move.angular.z=0.0

    def stop(self):        
        self.move.linear.x=0
        self.move.angular.z=0.0

    def rotate(self, dir):
        speed = 50
        angle = 60
        if dir==True:
            clockwise = True #True or false
        else:
            clockwise = False

        #Converting from angles to radians
        angular_speed = speed*2*PI/360
        relative_angle = angle*2*PI/360

        #We wont use linear components
        self.move.linear.x=0
        self.move.linear.y=0
        self.move.linear.z=0
        self.move.angular.x = 0
        self.move.angular.y = 0

        # Checking if our movement is CW or CCW
        if clockwise:
            self.move.angular.z = -abs(angular_speed)
            print self.move.angular.z
        else:
            self.move.angular.z = abs(angular_speed)
        # Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_angle = 0

        while(current_angle < relative_angle):
            self.pub_move.publish(self.move)
            t1 = rospy.Time.now().to_sec()
            current_angle = angular_speed*(t1-t0)
        #Forcing our robot to stop
        self.move.angular.z = 0
        # self.pub_move.publish(move)
        # rospy.spin()   


if __name__ == "__main__":

    mov = movement()
    rate = rospy.Rate(1)

    while not rospy.is_shutdown() :

        movement = raw_input('Enter desired movement: ')

        if movement == 'forward':
            mov.move_forward()

        if movement == 'backward':
            mov.move_backward()

        if movement == 'stop':
            mov.stop()

        if movement == 'r':
            mov.rotate(True)
            
        if movement == 'l':
            mov.rotate(False)

        mov.publish_vel()
        rate.sleep()
