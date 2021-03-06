#include <ros/ros.h>
#include "std_msgs/Float64.h"
#include <tf/transform_broadcaster.h>
#include <math.h>
/**
 * @file
 */

/** x coordinate of the Kinect with respect to the Baxter robot */	double x_kinect = 0.0; 
/** y coordinate of the Kinect with respect to the Baxter robot */	double y_kinect = 0.0;
/** z coordinate of the Kinect with respect to the Baxter robot */	double z_kinect = 0.0;

/** @brief Class to publish periodically the transformation between Baxter and Kinect
 */
class TF_Broadcaster{
    /** TF_Broadcaster:
     * - subscribe to /cur_tilt_angle to know the current tilt angle of the Kinect
     */
    public:
    TF_Broadcaster(){
        angle_sub = nh.subscribe("cur_tilt_angle", 2, &TF_Broadcaster::angleCB, this);
    }
    /**
     * Angle callback function
     * acquires the current tilt angle of the Kinect that is useful to know how the world frame should be oriented
     * @param[in]  angle_msg	current tilt angle of the Kinect
     */
    void angleCB(const std_msgs::Float64& angle_msg){
        if(angle_msg.data <= 30.0 && angle_msg.data >= -30.0)
        {
                angle = floor(angle_msg.data);
        }
    }

	float radians(void);
	float degrees(void);
	
protected:
    ros::NodeHandle nh; /**< Node Handle */
    ros::Subscriber angle_sub;  /**< Subscriber to /cur_tilt_angle */
    
    double angle = 20.0; /**< Current tilt angle of the Kinect */
};

/** Metod returning the current tilt angle of the Kinect in radians
 */
float TF_Broadcaster::radians(void){ 
	return angle * M_PI / 180;
}
/** Metod returning the current tilt angle of the Kinect in degrees
 */
float TF_Broadcaster::degrees(void){ 
	return angle;
}
    
/**
 * Main function: 
 * a TF broadcaster is created in order to add to the tree of frames:
 * 	- The world frame: in correspondence of the control board and with the same orientation of the Kinect;
 * 	- two frames for images in rviz (robot LCD and FSM schema).
 */
int main(int argc, char** argv)
{
	ros::init(argc, argv, "kinect_broadcaster");
	ros::NodeHandle n("~");

	// position of the Kinect with respect to the control board
	n.param<double>("x_kinect", x_kinect, 0.3);
	n.param<double>("y_kinect", y_kinect, 0.3);
	n.param<double>("z_kinect", z_kinect, 0.3);

	// current tilt angle of the Kinect in radians
	float rad_angle;

	TF_Broadcaster tf_broadcaster;

	ros::Rate r(10000);
	tf::TransformBroadcaster broadcaster;

	// Add two frames for images in rviz (robot LCD and FSM schema)
	tf::Transform image_frame;
	image_frame.setOrigin(tf::Vector3(0.20, 0.0, 0.90));
	tf::Quaternion image_rotation;
	image_rotation.setRPY(-1.57, 0, 1.57);
	image_frame.setRotation(image_rotation);

	tf::Transform image_frame_fsm;
	image_frame_fsm.setOrigin(tf::Vector3(0.20, 0.90, 1.40));
	image_frame_fsm.setRotation(image_rotation);

	tf::Transform change_frame;
	change_frame.setOrigin(tf::Vector3(x_kinect, y_kinect, z_kinect));

	tf::Quaternion frame_rotation;
    
	while(ros::ok()){
		
		// Negative because of the y axis grows downwards
		rad_angle = - tf_broadcaster.radians();
		
		frame_rotation.setRPY(0, rad_angle, 0); // pitch = current tilt angle of the Kinect
		change_frame.setRotation(frame_rotation);
		
		broadcaster.sendTransform(tf::StampedTransform(change_frame, ros::Time::now(), "world_frame", "camera_link"));
		broadcaster.sendTransform(tf::StampedTransform(image_frame, ros::Time::now(), "world_frame", "image_frame"));
		broadcaster.sendTransform(tf::StampedTransform(image_frame_fsm, ros::Time::now(), "world_frame", "image_frame_fsm"));
				
		ros::spinOnce();
		r.sleep();
	}

    return 0;
}
