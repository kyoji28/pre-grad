#!/usr/bin/env python
import rospy

from std_msgs.msg import Empty
# from std_msgs.msg import Int8
# from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist
import sys, select, termios, tty

def getKey():
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
                key = sys.stdin.read(1)
        else:
                key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

if __name__=="__main__":
        settings = termios.tcgetattr(sys.stdin)
        rospy.init_node("keyboard_command")

        ns = "/tello"
        land_pub = rospy.Publisher(ns + '/land', Empty, queue_size=1)
        takeoff_pub = rospy.Publisher(ns + '/takeoff', Empty, queue_size=1)
        cmd_vel_pub = rospy.Publisher(ns + '/cmd_vel', Twist, queue_size=1)
        halt_pub = rospy.Publisher(ns + '/emergency', Empty, queue_size=1)
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.y = 0.0
        cmd_vel_msg.linear.x = 0.0

        #the way to write publisher in python
        # comm=Int8()
        # gain=UInt16()

        try:
                print("Control Tello with WASD keys for directional movement, H (up), B (down), T (takeoff), L (land), and X to stop.")
                while(True):
                        key = getKey()
                        # print("the key value is {}".format(ord(key)))
                        # Reset velocity message
                        cmd_vel_msg.linear.x = 0.0
                        cmd_vel_msg.linear.y = 0.0
                        cmd_vel_msg.linear.z = 0.0

                        # takeoff and landing
                        if key == 'l':
                                print("land!")
                                land_pub.publish(Empty())
                                #for hydra joints
                        elif key == 't':
                                print("takeoff!")
                                takeoff_pub.publish(Empty())

                        # move
                        elif key == 'w':
                                print("move forward")
                                cmd_vel_msg.linear.y = 0.3
                        elif key == 's':
                                print("move backward")
                                cmd_vel_msg.linear.y = -0.3
                        elif key == 'a':
                                print("move left")
                                cmd_vel_msg.linear.x = -0.3
                        elif key == 'd':
                                print("move right")
                                cmd_vel_msg.linear.x = 0.3

                        elif key == 'h':
                                print("move up")
                                cmd_vel_msg.linear.z = 0.3
                        elif key == 'b':
                                print("move down")
                                cmd_vel_msg.linear.z = -0.3
                        elif key == 'x':
                                print("stop")
                                cmd_vel_msg.linear.y = 0.0
                                cmd_vel_msg.linear.x = 0.0
                                cmd_vel_msg.linear.z = 0.0

                        # Let's write a script to move the tello in the yaw direction.
                        

                        elif key == '0':
                                print("halt")
                                halt_pub.publish(Empty())

                        elif key == '\x03':
                                break
                        cmd_vel_pub.publish(cmd_vel_msg)
                        rospy.sleep(0.01)
        except Exception as e:
                print(repr(e))
        finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

