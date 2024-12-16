#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from geometry_msgs.msg import Point
from jsk_recognition_msgs.msg import HumanSkeletonArray
from jsk_recognition_msgs.msg import HumanSkeleton

class Move_to_human():
    def __init__(self):
        self.skeleton_sub = rospy.Subscriber('/edgetpu_human_pose_estimator/output/skeletons',HumanSkeletonArray, self.skeleton_cb)
        self.skeletons = HumanSkeletonArray()
        self.bone_names = []
        self.bones = []
        self.start = Point()
        self.end = Point()
        self.timer = rospy.Timer(rospy.Duration(0.05), self.timerCallback)

    def skeleton_cb(self,msg):
        self.skeletons = msg
        for skeleton in self.skeletons.skeletons:
            self.bone_names = skeleton.bone_names
            self.bones = skeleton.bones
            #rospy.loginfo(f"bone_name{self.bone_names}")


    # search "left wrist" or "right wrist" in self.bone_names
    # search "left shoulder" or "right shoulder" in self.bone_names
    # Task 1 if there are these 4 bones in self.bone_names, get the bone's coodinates in self.bones
    # Task 2 you should find whether the target bone is before or after arrow "->"
    # Task 3 compare the bone's coodinate
    def search_bone(self):
        target_bones =  ['left shoulder', 'right shoulder']
        for i, bone_name in enumerate(self.bone_names):
            for j,target_bone in enumerate(target_bones):
                if target_bone in bone_name:
                    rospy.loginfo(f"bone_name{bone_name}")
                    bone = self.bones[i]  
                    start = bone.start_point
                    end = bone.end_point

    def timerCallback(self,event):
        self.search_bone()

if __name__ == '__main__':
    rospy.init_node("Move_to_human")
    node = Move_to_human()
    rospy.spin()
