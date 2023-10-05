#!/usr/bin/env python
import rospy

from std_msgs.msg import Empty
from std_msgs.msg import Int8
from std_msgs.msg import UInt16
from std_msgs.msg import UInt8
import sys, select, termios, tty

def getKey():
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

if __name__=="__main__":
        settings = termios.tcgetattr(sys.stdin)
        rospy.init_node("keyboard_command")

        ns = "/tello"
        land_pub = rospy.Publisher(ns + '/land', Empty, queue_size=1)
        takeoff_pub = rospy.Publisher(ns + '/takeoff', Empty, queue_size=1)

        #the way to write publisher in python
        comm=Int8()
        gain=UInt16()
        try:
                while(True):
                        key = getKey()
                        # print("the key value is {}".format(ord(key)))
                        # takeoff and landing
                        if key == 'l':
                            print("land!")
                            land_pub.publish(Empty())
                            #for hydra joints
                        if key == 't':
                            print("takeoff!")
                            takeoff_pub.publish(Empty())
                        if key == '\x03':
                            break
                        rospy.sleep(0.001)
        except Exception as e:
                print(repr(e))
        finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

