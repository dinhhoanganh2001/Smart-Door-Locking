from Adafruit_IO import Client,Data
import cv2
import sys
import time
from device import readSerial

from PIL import Image


AIO_USERNAME = "hungak01"
AIO_KEY = "aio_Nrsd87hRDxU3HWNPQzvuQLQaDNxt"


fr_button = "fr-button"
fr_button2 = "fr-button2"
fr_image = "fr-image"
fr_screen = "fr-screen"

FEED_ID = [fr_button, fr_button2, fr_image, fr_screen]


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
    # Subscribe to changes on a feed named DemoFeed.
    for id in FEED_ID:
        client.subscribe(id)

def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format(mid, granted_qos[0]))

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

def take_photo():
    cam = cv2.VideoCapture(0)

    x = 0
    while x < 30:
        ret, frame = cam.read()
        x += 1
    if not ret:
        raise "failed to grab frame"
    cv2.waitKey(1)
    img_name = "opencv_frame_{}.png".format(0)
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))

    cam.release()
    return frame

def get_image_pil():
    """
      Take a photo, optimize it with PIL, and publish it to Adafruit IO.
    """

    # stream = io.BytesIO()
    img = take_photo()
    img_pil = Image.fromarray(img)
    print('> capturing')
    #
    # # Tweak point 1: if your data size is too big, try reducing the original
    # # dimensions here.
    # img_pil.save(stream, 'jpeg')
    # stream.seek(0)
    # print('> converting')
    # value = base64.b64encode(stream.read())
    # if len(value) > 102400:
    #     print ("image is too big!")
    #     print ("  got %i bytes" % len(value))
    #     time.sleep(2)
    #     return
    #
    # print ('Publishing {0}... {1} bytes to image-stream.'.format(value[0:32], len(value)))
    return img_pil


