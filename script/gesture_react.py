#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from geometry_msgs.msg import Point
from std_msgs.msg import String
from jsk_recognition_msgs.msg import HumanSkeletonArray
from jsk_recognition_msgs.msg import HumanSkeleton

class Move_to_human():
    def __init__(self):
        self.msgs_pub = rospy.Publisher('chatter', String, queue_size = 10)
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
    # Task 1 if there are these 4 bones in self.bone_names, get the bone's coordinates in self.bones
    # Task 2 you should find whether the target bone is before or after arrow "->"
    # Task 3 compare the shoulder bone's coodinate with the wrist bone's coodinate
    def search_bone(self):
        target_shoulder_bones =  ['left shoulder', 'right shoulder']
        target_wrist_bones = ['left wrist', 'right wrist']
        shoulder_bone_coordinates = []
        wrist_bone_coordinates = []
        # print(len(self.bone_names))
        # print(len(self.bones))
        # print(self.bone_names)
        # print(self.bones)
        # for i, bone in enumerate(self.bones):
        #     bone_debug = bone
        #     bone_name = self.bone_names[i]
        #     rospy.loginfo(f"bone_raw {bone_debug}")
        #     rospy.loginfo(f"self.bone_names {bone_name}")
        # self.bone_names = []
        # self.bones = []

        if (len(self.bone_names)) < 1:
             rospy.loginfo("no bones")
        else:
            for i, bone_name in enumerate(self.bone_names):
                find_shoulder_bone_name = None
                shoulder_bone_coordinates = []
                find_wrist_bone_name = None
                wrist_bone_coordinates = []
                rospy.logerr(f"bone_name {bone_name}")
                #矢印を基準に分割
                if '->' in bone_name:
                    parts = bone_name.split('->')
                    start_bone_name = parts[0].strip()
                    end_bone_name = parts[1].strip()
                    
                    #ターゲットの骨を探索
                    # rospy.loginfo(f"bone_raw {self.bones[i]}") 
                    bone = self.bones[i]
                    # rospy.loginfo(f"bone{bone}")

                    if start_bone_name in target_wrist_bones:
                        find_wrist_bone_name = start_bone_name
                        wrist_bone_coordinates = bone.start_point
                    if end_bone_name in target_wrist_bones:
                        find_wrist_bone_name = end_bone_name
                        wrist_bone_coordinates = bone.end_point
                        
                    if start_bone_name in target_shoulder_bones:
                        find_shoulder_bone_name = start_bone_name
                        shoulder_bone_coordinates = bone.start_point
                    if end_bone_name in target_shoulder_bones:
                        find_shoulder_bone_name = end_bone_name
                        shoulder_bone_coordinates = bone.end_point
                    # rospy.loginfo(f"shoulder_bone_name{find_shoulder_bone_name}")
                    # rospy.loginfo(f"Target shoulder_bone coordinates: {shoulder_bone_coordinates.y}")
                    
                    rospy.logwarn(f"wrist_bone_name{find_wrist_bone_name}")
                    rospy.logwarn(f"Target wrist_bone coordinates: {wrist_bone_coordinates.y}")
            if wrist_bone_coordinates.y >shoulder_bone_coordinates.y:
                self.msgs_pub.publish("success!!")
                print("success")


    
    def timerCallback(self,event):
        try:
            self.search_bone()
        except Exception as e:
            pass
           # rospy.logerr(f"Error in timerCallback: {e}")


if __name__ == '__main__':
    rospy.init_node("Move_to_human")
    node = Move_to_human()
    rospy.spin()
