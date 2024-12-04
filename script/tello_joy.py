#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist

class tello_joy():
    def __init__(self):
        ns = "/tello"
        self.joy_sub = rospy.Subscriber(ns + '/joy', Joy, self.joy_cb)
        self.joy = Joy()
        
        self.land_pub = rospy.Publisher(ns + '/land', Empty, queue_size=1)
        self.takeoff_pub = rospy.Publisher(ns + '/takeoff', Empty, queue_size=1)
        self.cmd_vel_pub = rospy.Publisher(ns + '/cmd_vel', Twist, queue_size=1)
        # self.cmd_vel_msg = Twist()
        self.takeoff_flag = False
        self.land_flag = False
        self.cmd_vel_flag = False
        self.gain = 1.0
        self.output = Twist()

    def joy_cb(self,msg):
        self.joy = msg
        if self.joy.buttons[0] == 1 and self.joy.axes[9] == -1.0:
            self.takeoff_flag = True
        if self.joy.buttons[2] == 1 and self.joy.axes[9] == 1.0:
            self.land_flag = True
        if self.joy.buttons[3] == 1 and self.cmd_vel_flag == False: #triangle
            rospy.loginfo("Enter Velocity Mode")
            self.cmd_vel_flag = True
            rospy.sleep(1.0)
        elif self.joy.buttons[1] == 1 and self.cmd_vel_flag == True: #triangle
            rospy.loginfo("Break Velocity Mode")
            self.cmd_vel_flag = False

    def joy_to_vel(self):
         self.output.linear.x = - self.joy.axes[0] * self.gain
         self.output.linear.y = self.joy.axes[1] * self.gain
         self.output.linear.z = self.joy.axes[5] * self.gain
         self.output.angular.z = - self.joy.axes[2]

    def main(self):
        rate = rospy.Rate(100) 
        while not rospy.is_shutdown():
            if self.takeoff_flag:
                rospy.loginfo("takeoff")
                self.takeoff_pub.publish(Empty())
                self.takeoff_flag = False

            if self.land_flag:
                rospy.loginfo("land")
                self.land_pub.publish(Empty())
                self.land_flag = False

            if self.cmd_vel_flag:
                self.joy_to_vel()
                rospy.loginfo(f"Publishing velocity: {self.output}")
                self.cmd_vel_pub.publish(self.output)

            rate.sleep()


if __name__ == '__main__':
    rospy.init_node("tello_joy")
    node = tello_joy()
    node.main()
