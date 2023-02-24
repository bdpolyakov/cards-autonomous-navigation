#!/usr/bin/env python
import rospy
import threading
import cv2
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from flask import Flask, render_template, redirect, Response


# numpy and scipy
import numpy as np
from scipy.ndimage import filters

app = Flask(__name__)

bridge = CvBridge()

cv_image = 0

def callback(data):
    global cv_image
    print("received")
    try:
        # cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        #cv2.imshow("Image window", cv_image)
        np_arr = np.fromstring(data.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        print('Original Dimensions : ',cv_image.shape)
 
        scale_percent = 30 # percent of original size
        width = int(cv_image.shape[1] * scale_percent / 100)
        height = int(cv_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        
        # resize image
        resized = cv2.resize(cv_image, dim, interpolation = cv2.INTER_AREA)
    except CvBridgeError as e:
        print(e)

    # d = rospy.Duration(1, 0)
    # rospy.sleep(d)


threading.Thread(target=lambda: rospy.init_node('test_node5', disable_signals=True)).start()
image_sub = rospy.Subscriber("axis/image_raw/compressed/", CompressedImage, callback)


def gen():
    global cv_image
    while True:
        #success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', cv_image)
        frame = jpeg.tobytes()
        
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # from og server
    app.run(host='0.0.0.0', port=5000, debug=False)