#!/usr/bin/env python

"""
ROS node used to provide services for interacting with Baxter.
Services provided: playback, record, open/close gripper and reach goal position.
"""

import argparse
import sys

import rospy

from baxter_interface import Gripper

import os.path

from os import listdir
from BaxterGBI_pbr.msg import *
from baxter_interface import CHECK_VERSION
from BaxterGBI_pbr.srv import *
from BaxterGBI_pbr import *


"""
Global Variables used to manage all the services.
"""

global pb, playbacking, starting_pause, pause_state
global file_playback, line_executed #Information for recording after playback

line_executed = 0
pause_state = 0
starting_pause = 0
playbacking = False
pb = PlaybackObj()

def playback_handler(req):
    """
    Service used to activate the playback mode on the baxter.
    
    @type req.msg.filename: string
    @param req.msg.filename: name of the file you want to play.
    @type req.msg.loops: uint8
    @param req.msg.loops: number of times you want to play it.
    @type req.msg.scale_vel: float32
    @param req.msg.scale_vel: number to scale velocity of movement.
    
    @returns: 0 on success, 1 on errors
    """
    rospy.loginfo("Called!!!")

    
    #Check if the file exists
    file_path_string = "src/BaxterGBI_pbr/RecordedFile/"+req.msg.filename
    rospy.loginfo(file_path_string)
    if os.path.isfile(file_path_string) :
        global pb, playbacking, file_playback
        playbacking = True
        file_playback = file_path_string
        pb.map_file(file_path_string, req.msg.loops, req.msg.scale_vel)
        playbacking = False
        return 0
    else:
        rospy.logerr("The file doesn't exist!!")
        return 1


def record_start_handler(req):
    """
    Service used to start the recording mode on the baxter.
    
    @type req.filename: string
    @param req.filename: name of the recorderd file.
    @type req.mode: string
    @param req.mode: 'start' or 'stop'.
    @type req.record_rate: uint16
    @param req.record_rate: rate used for recording joints' data.
    
    @returns: 0 on success, 1 on errors
    """
    global pb, playbacking, pause_state, file_playback, line_executed
    
    if playbacking == True and pause_state == 1:
        playbacking = False
        pause_state = 0
        
        msg = modify_playback()
        msg.old_filename = file_playback
        msg.new_filename = "src/BaxterGBI_pbr/RecordedFile/"+req.filename
        msg.mode = "start"
        msg.line_number = line_executed
        msg.record_rate = req.record_rate
        
        #Stop the playbacking
        pb.stop = 1
        
        
        pub2.publish(msg)
        return 0
        
    elif playbacking == True:
        rospy.logwarn("Cannot record while playbacking")
        return 1
    else:
        rospy.loginfo("Called !!!")
         
        msg = record_status()
        
        msg.filename = "src/BaxterGBI_pbr/RecordedFile/"+req.filename
        msg.mode = "start"
        msg.record_rate = req.record_rate
        pub.publish(msg)
        return 0


def record_stop_handler(req):
    """
    Service used to stop the recording mode on the baxter.
    
    @type req.filename: string
    @param req.filename: (empty, not used).
    @type req.mode: string
    @param req.mode: 'start' or 'stop'.
    @type req.record_rate: uint16
    @param req.record_rate: rate used for recording joints' data (zero, not used).
    
    @returns: 0 on success, 1 on errors
    """
    
    rospy.loginfo("Called !!!")
    msg = record_status()
    msg.filename = " "
    msg.mode = "stop"
    msg.record_rate = 0
    
    pub.publish(msg)
    return 0


def gripper_handler(req):
    """
    Service used to open or close the gripper.
    
    @type req.limb: string
    @param req.limb: "left" or "right" arm.
    @type req.open: uint8
    @param req.open: value from 0 (close) to 100 (open).
    
    @returns: 0 on success, 1 on errors
    """

    global left_gripper, right_gripper
    
    if req.limb == "left":
        if req.open >= 0 and req.open <= 100:
            left_gripper.command_position(req.open)
    elif req.limb == "right":
        if req.open >= 0 and req.open <= 100:
            right_gripper.command_position(req.open)
    else:
        return 1 #Invalid choice
        
    return 0


def reach_goal_handler(req):
    """
    Service used to reach a specified goal.
    
    @type req.limb: string
    @param req.limb: "left" or "right" arm.
    @type req.position: float64[]
    @param req.position: position of the goal (x, y, z).
    @type req.quaternion: float64[]
    @param req.quaternion: orientation of the goal (x, y, z, w).
    
    @returns: 0 on success, 1 on errors
    """
    
    if req.limb == "left" or req.limb == "right":
        arm = Limb(req.limb)
        #Define the final goal
        pos = []
        pos.append(req.position[0])
        pos.append(req.position[1])
        pos.append(req.position[2])

        orient = []

        orient.append(req.quaternion[0])
        orient.append(req.quaternion[1])
        orient.append(req.quaternion[2])
        orient.append(req.quaternion[3])
        
        try:
            # reformat the solution arrays into a dictionary
            joint_solution = ik_tracking(req.limb,pos,orient)   #joint_solution is an object type ReturnValue
            
            if joint_solution.isError == 1:
                rospy.logwarn("Cannot reach the goal")
            else:
                # set arm joint positions to solution
                arm.move_to_joint_positions(joint_solution.limb_joints)
        except rospy.ServiceException, e:
            rospy.logerr("Error in Inverse Kinematic problem")

def pause_resume_handler(req):
    """
    Service used to pause and resume a playback.
    
    @type req.mode: uint8
    @param req.mode: 0 to pause, 1 to resume.
    
    @returns: 0 on success, 1 on errors
    """
    global pb, playbacking, starting_pause, pause_state
    
    #Every time we change from Resume to Pause -> We start counting the the time passed, then we add it to the pb.paused_time when resuming
    if playbacking == True:
        if req.mode != pb.pause_state:
            if req.mode == 1: #Pausing
                global line_executed
                line_executed = pb.line_executed
                pause_state = req.mode
                pb.pause_state = pause_state
                rospy.loginfo("Paused!")
                starting_pause = rospy.get_time()
                return 0
            elif req.mode == 0: #Resuming
                pause_state = req.mode
                pb.pause_state = pause_state
                rospy.loginfo("Resumed!")
                pb.paused_time += rospy.get_time() - starting_pause
                
        else:
            rospy.logwarn("Cannot change to state to the same one!")
            return 1
    else:
        rospy.logwarn("Playback is stop running!")
        return 1

#pbr_node initialization
def pbr_server_baxter():
    """Main of the node. It makes available the services and wait for requests.
    """
    rospy.loginfo("Initializing node... ")
    rospy.init_node('pbr_server_baxter')
    rospy.loginfo("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled
    
    global left_gripper, right_gripper
    
    left_gripper = baxter_interface.Gripper('left', CHECK_VERSION)
    right_gripper = baxter_interface.Gripper('right', CHECK_VERSION)
    
    global pub, pub2
    pub = rospy.Publisher('recording_status', record_status, queue_size=2)
    pub2 = rospy.Publisher('modify_playback_status', modify_playback, queue_size=2)

    rospy.loginfo("Enabling robot... ")
    rs.enable()

    service1 = rospy.Service('playback', Playback, playback_handler)
    service2 = rospy.Service('record_stop', RecordStop, record_stop_handler)
    service3 = rospy.Service('record_start', RecordStart, record_start_handler)
    service4 = rospy.Service('gripper', Gripper, gripper_handler)
    service5 = rospy.Service('reach_goal', ReachGoal, reach_goal_handler)
    service6 = rospy.Service('pause_resume', PauseResume, pause_resume_handler)
    rospy.loginfo("PBR node executed -> providing playback/record services.")

    def clean_shutdown():
        rospy.loginfo("\nExiting example...")
        if not init_state:
            rospy.loginfo("Disabling robot...")
            rs.disable()
    rospy.on_shutdown(clean_shutdown)

    rospy.spin()

if __name__ == "__main__":
    pbr_server_baxter()