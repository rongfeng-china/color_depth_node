#!/usr/bin/env python
import roslib
#roslib.load_manifest('my_image')
import sys, rospy, cv2, os, rosgraph.masterapi
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image, CompressedImage,RegionOfInterest
from cv_bridge import CvBridge, CvBridgeError

class cvBridgeDemo():
    def __init__(self):
        self.node_name = "cv_bridge_demo"
        
        rospy.init_node(self.node_name)
        
        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)
        
        # Create the OpenCV display window 
        self.cv_window_name = self.node_name
        cv2.namedWindow(self.cv_window_name, 1)
        cv2.moveWindow(self.cv_window_name, 25, 75)     
        cv2.namedWindow("Depth Image", 1)
        cv2.moveWindow("Depth Image", 25, 350)
        
        self.bridge = CvBridge()
        
        # Subscribe to the camera image and depth topics and set
        # the appropriate callbacks
        self.cmd_sub   = rospy.Subscriber("cmd", String, self.command_callback)
        self.image_sub = rospy.Subscriber("/camera/rgb/image_rect_color", Image, self.image_callback)
        self.depth_sub = rospy.Subscriber("/camera/depth/image_rect_raw", Image, self.depth_callback)
        #
        self.display_image = None
        self.depth_display_image = None
        self.cmd = None
    
        rospy.loginfo("Waiting for image topics...")

    def image_callback(self, ros_image):
        try:
            frame = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        except CvBridgeError, e:
            print e       
        frame = np.array(frame, dtype=np.uint8)
        self.display_image = self.process_image(frame)             
        #cv2.imshow(self.node_name, self.display_image)
        
        # Process any keyboard commands
        '''self.keystroke = cv2.waitKey(5)
        if 32 <= self.keystroke and self.keystroke < 128:
            cc = chr(self.keystroke).lower()
            if cc == 'q':
                # The user has press the q key, so exit
                rospy.signal_shutdown("User hit q key to quit.")'''
                
    def depth_callback(self, ros_image):
        try:
            depth_image = self.bridge.imgmsg_to_cv2(ros_image, "passthrough")
        except CvBridgeError, e:
            print e
        depth_array = np.array(depth_image, dtype=np.float32)         
        cv2.normalize(depth_array, depth_array, 0, 1, cv2.NORM_MINMAX)       
        self.depth_display_image = self.process_depth_image(depth_array)  
        #cv2.imshow("Depth Image", self.depth_display_image)

    def command_callback(self, data1):
        try:
            cmd = data1.data
            rospy.loginfo(rospy.get_caller_id() + "I heard %s", data1.data)
        except CvBridgeError, e:
            print e
        return cmd
          
    def process_image(self, frame):
        '''grey = cv2.cvtColor(frame, cv2.CV_BGR2GRAY)
        grey = cv2.blur(grey, (7, 7)) 
        edges = cv2.Canny(grey, 15.0, 30.0)  '''      
        return frame
    
    def process_depth_image(self, frame):
        return frame
    
    def cleanup(self):
        print "Shutting down vision node."
        cv2.destroyAllWindows()  
    
    def run(self):
        while not rospy.is_shutdown():
            if (self.display_image is None) or (self.depth_display_image is None):
                continue

            if (not self.cmd is None):
                if self.cmd == "yellow":
                    print 'hihihi'

            if (not self.display_image is None) and (not self.depth_display_image is None):
                cv2.imshow(self.node_name, self.display_image)
                cv2.imshow("Depth Image", self.depth_display_image) 
                cv2.waitKey(5)
    
def main(args):       
    try:
        demo = cvBridgeDemo()
        demo.run()
        #rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down vision node."
        cv2.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
