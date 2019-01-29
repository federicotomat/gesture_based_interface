#!/usr/bin/env python

"""
Baxter Mirror Node -> provides the mirroring service.
"""

import argparse
import sys

import struct
import rospy


from BaxterGBI_pbr.msg import *
from baxter_interface import CHECK_VERSION
from BaxterGBI_pbr.srv import *
from ik_header import *
from pbr_header import *

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


global init_pose_hand, init_orient_hand, first_data, init_pose_baxter, init_orient_baxter
first_data = False
init_pose_hand = []
init_orient_hand = []
init_pose_baxter = []
init_orient_baxter = []

def mirror_callback(data):
    """
    Callback function associated with the topic 'mirror_end_effector'.
    Whenever a data is written in the topic, this function is called and obtain from ik_tracking function the joints values to assign and
    move the end effector to the goal.
    
    @type data.position: float[]
    @param data.position: position we want to achieve.
    @type data.quaternion: float[]
    @param data.quaternion: orientation we want to achieve (Quaternion).
    """
    #TODO -> make as parameter
    limb = "left"
    
    arm = Limb(limb)
    
    #TODO -> create a sevice "calibrate" for acquiring initial values
    global init_pose_hand, init_orient_hand, init_pose_baxter, init_orient_baxter, first_data
    if first_data == False:
        first_data = True
        #Acquire initial position/orientation of the human hand (The first value published)
        init_pose_hand.append(data.position[0])
        init_pose_hand.append(data.position[1])
        init_pose_hand.append(data.position[2])
        init_orient_hand.append(data.quaternion[0])
        init_orient_hand.append(data.quaternion[1])
        init_orient_hand.append(data.quaternion[2])
        init_orient_hand.append(data.quaternion[3])
        
        resp = arm.endpoint_pose()
        #Acquire initial position/orientation of the baxter
        init_pose_baxter = resp['position']
        init_orient_baxter = resp['orientation']
        print("Pose: "+ str(init_pose_baxter))
        print("Orient: "+str(init_orient_baxter))
        
        
    
    #Evaluate the relative movement of the hand
    pos = []
    pos.append(init_pose_baxter[0] + (data.position[0] - init_pose_hand[0]))
    pos.append(init_pose_baxter[1] + (data.position[1] - init_pose_hand[1]))
    pos.append(init_pose_baxter[2] + (data.position[2] - init_pose_hand[2]))
    
    
    orient = []
    
    #quaternion = tf.transformations.quaternion_from_euler(-3.127816, 0.000416, -1.900463)
    #type(pose) = geometry_msgs.msg.Pose
    #orient.append(quaternion[0])
    #orient.append(quaternion[1])
    #orient.append(quaternion[2])
    #orient.append(quaternion[3])
    
    orient.append(init_orient_baxter[0] + (data.quaternion[0] - init_orient_hand[0]))
    orient.append(init_orient_baxter[1] + (data.quaternion[1] - init_orient_hand[1]))
    orient.append(init_orient_baxter[2] + (data.quaternion[2] - init_orient_hand[2]))
    orient.append(init_orient_baxter[3] + (data.quaternion[3] - init_orient_hand[3]))
    
    print("Start q: "+str(arm.joint_angles()))
    
    
    try:
        # reformat the solution arrays into a dictionary
        joint_solution = ik_tracking(limb,pos,orient)   #joint_solution is an object type ReturnValue
        
        if joint_solution.isError == 1:
            print("Cannot reach the goal")
        else:
            # set arm joint positions to solution
            #arm = Limb(limb) #TODO -> remove (?) there is at the beginning of the funtion
            arm.move_to_joint_positions(joint_solution.limb_joints)
    except rospy.ServiceException, e:
        print("Ahahah speravi andasse bene!!")
   


def mirror_server():
    """
    Main of the node. Takes the information from the topic and move the baxter end effector based on those values.
    """
    
    print("Initializing node... ")
    rospy.init_node('mirror_server')
    print("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled
    print("Enabling robot... ")
    rs.enable()

    #Mirror service -> input on/off
    #service1 = rospy.Service('mirror', Mirror, mirror_handler)
    print "Mirror Server executed -> mirror service available."


    
    rospy.Subscriber("mirror_end_effector", mirror_end_effector, mirror_callback)
    
    def clean_shutdown():
        print("\nExiting example...")
        if not init_state:
            print("Disabling robot...")
            rs.disable()
    rospy.on_shutdown(clean_shutdown)

    rospy.spin()

if __name__ == "__main__":
    mirror_server()
