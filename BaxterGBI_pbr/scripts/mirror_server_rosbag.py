#!/usr/bin/env python

"""
ROS node used to allow the user to control the baxter via mirroring using the data provided by the kinect (Rosbag for testing).
"""

import argparse
import sys

import struct
import rospy

import baxter_interface
from BaxterGBI_pbr.msg import *
from baxter_interface import CHECK_VERSION, Limb
from BaxterGBI_pbr.srv import *
from BaxterGBI_pbr import ik_tracking, ReturnValue

import tf

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)


global init_pose_hand, init_orient_hand, init_pose_baxter, init_orient_baxter, first_data
first_data = 0
init_pose_hand = []
init_orient_hand = []
init_pose_baxter = []
init_orient_baxter = []

   
global steps, file_output
steps = -1 

def mirror_callback(data):
    """
    Callback function associated with the topic 'mirror_end_effector'.
    Whenever a data is written in the topic, this function is called and obtain from ik_tracking function the joints values to assign and
    move the end effector to the goal.
    
    @type data.pose.pose.position: float[]
    @param data.pose.pose.position: position we want to achieve.
    @type data.pose.pose.orientation: float[]
    @param data.pose.pose.orientation: orientation we want to achieve (Quaternion).
    """
    
    
    
    global arm, limb, init_pose_hand, init_orient_hand, init_pose_baxter, init_orient_baxter, first_data
    global steps
    
    
    steps = (steps+1)%5
    
    if first_data == 0:
        first_data = 1  
        
        #Acquire initial position/orientation of the human hand (The first value published)
        init_pose_hand.append(data.pose.pose.position.x)
        init_pose_hand.append(data.pose.pose.position.y)
        init_pose_hand.append(data.pose.pose.position.z)
        init_orient_hand.append(data.pose.pose.orientation.x)
        init_orient_hand.append(data.pose.pose.orientation.y)
        init_orient_hand.append(data.pose.pose.orientation.z)
        init_orient_hand.append(data.pose.pose.orientation.w)
        
        
        resp = arm.endpoint_pose()
        #Acquire initial position/orientation of the baxter
        init_pose_baxter = resp['position']
        init_orient_baxter = resp['orientation']
        #rospy.loginfo("Pose: "+ str(init_pose_baxter))
        #rospy.loginfo("Orient: "+str(init_orient_baxter))
        rospy.loginfo("First Data achieved -> Used as initial state")
    elif steps == 0:
        #Evaluate the relative movement of the hand
        pos = []
        pos.append(init_pose_baxter[0] - (data.pose.pose.position.x - init_pose_hand[0]))
        pos.append(init_pose_baxter[1] + (data.pose.pose.position.y - init_pose_hand[1]))
        pos.append(init_pose_baxter[2] + (data.pose.pose.position.z - init_pose_hand[2]))
        
        
        orient = []
        
        #quaternion = tf.transformations.quaternion_from_euler(-3.127816, 0.000416, -1.900463)
        #type(pose) = geometry_msgs.msg.Pose
        #orient.append(quaternion[0])
        #orient.append(quaternion[1])
        #orient.append(quaternion[2])
        #orient.append(quaternion[3])
        
        orient.append(init_orient_baxter[0] + (data.pose.pose.orientation.x - init_orient_hand[0]))
        orient.append(init_orient_baxter[1] + (data.pose.pose.orientation.y - init_orient_hand[1]))
        orient.append(init_orient_baxter[2] + (data.pose.pose.orientation.z - init_orient_hand[2]))
        orient.append(init_orient_baxter[3] + (data.pose.pose.orientation.w - init_orient_hand[3]))
        
        rospy.loginfo("Start q: "+str(arm.joint_angles()))
        
        
        try:
            joint_solution = ik_tracking(limb,pos,orient)   #joint_solution is an object type ReturnValue
            
            if joint_solution.isError == 1:
                rospy.logwarn("Cannot reach the goal")
            else:
                # set arm joint positions to solution
                arm.move_to_joint_positions(joint_solution.limb_joints)
                
                global file_output
                resp = arm.endpoint_pose()
                file_output.write(str(resp['position'].x)+","+str(resp['position'].y)+","+str(resp['position'].z)+"\n")
        except rospy.ServiceException, e:
            rospy.logerr("Error during Inverse Kinematic problem")
       
  
def mirror_server():
    """
    Main of the node. Takes the information from the topic and move the baxter end effector based on those values.
    """
    
    rospy.loginfo("Initializing node... ")
    rospy.init_node('mirror_server')
    rospy.loginfo("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled
    rospy.loginfo("Enabling robot... ")
    rs.enable()
    
    rospy.loginfo("Mirror Server executed -> mirror service available.")
    
    global file_output
    file_output = open("baxter_data.csv","w+")
    
    global arm, limb
    if len(sys.argv) == 2 and (sys.argv[1] == "left" or sys.argv[1] == "right"):
        arm = Limb(sys.argv[1])
        limb = sys.argv[1]
    else:
        print("Insert as 1st param left or right")
        return
        
    rospy.Subscriber("odometry/baxter/kinect_right_hand", mirror_bag, mirror_callback)
    
    def clean_shutdown():
        rospy.loginfo("\nExiting example...")
        if not init_state:
            rospy.loginfo("Disabling robot...")
            rs.disable()
        file_output.close()
    rospy.on_shutdown(clean_shutdown)

    rospy.spin()

if __name__ == "__main__":
    mirror_server()