import cv2, datetime, os, time, requests, subprocess, argparse
from picamera.array import PiRGBArray
from picamera import PiCamera

img_path = "%s%s" % (os.getcwd(), "/images")
url = 'http://training.socif.co:8000/upload' # deployment
n = 1
cams = 1
sleep_time = 10

def set_1080p(x):
    if x == 1:
        cam1.set(3, 1920)
        cam1.set(4, 1080)
    elif x == 2:
        cam2.set(3, 1920)
        cam2.set(4, 1080)
    elif x == 3:
        cam3.set(3, 1920)
        cam3.set(4, 1080)
    else:
        pass

def set_720p(x):
    if x == 1:
        cam1.set(3, 1280)
        cam1.set(4, 720)
    elif x == 2:
        cam2.set(3, 1280)
        cam2.set(4, 720)
    elif x == 3:
        cam3.set(3, 1280)
        cam3.set(4, 720)
    else:
        pass

def set_480p(x):
    if x == 1:
        cam1.set(3, 640)
        cam1.set(4, 480)
    elif x == 2:
        cam2.set(3, 640)
        cam2.set(4, 480)
    elif x == 3:
        cam3.set(3, 640)
        cam3.set(4, 480)
    else:
        pass

# main
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Send images from USB cameras to a HTTP server.')
    parser.add_argument(
        '-i',
        '--interval',
        default=10 ,
        type=int,
        help='Time delay between shots (seconds) (default: 10)'
    )

    parser.add_argument(
        '-r',
        '--resolution',
        default=480,
        type=int,
        help='Resolution of cameras (args: 1080, 720 or 480) (default: 480)'
    )

    parser.add_argument(
        '-t',
        '--test',
        default=url,
        type=str,
        help='Enable test mode via test URL for local testing (default: deployment mode URL)'
    )

    parser.add_argument(
        '-c',
        '--cameras',
        default=cams,
        type=int,
        help='Set the amount of cameras to be sent (default: 1)'
    )
    
    args = parser.parse_args()
    
    # argument parsing
    if args.interval >= 0 and args.interval < 3600:
        sleep_time = args.interval
    else:
        sleep_time = 10
    
    if args.test:
        url = args.test

    cam1 = PiCamera()
    rawCap = PiRGBArray(cam1)

    time.sleep(0.1)

    while True:
        # default res - 640 x 480
        # cam 1
        if args.cameras == 3:
            cam1 = cv2.VideoCapture(0)
            cam2 = cv2.VideoCapture(2)
            cam3 = cv2.VideoCapture(4)

            if args.resolution == 1080:
                set_1080p(1)
                set_1080p(2)
                set_1080p(3)
            elif args.resolution == 720:
                set_720p(1)
                set_720p(2)
                set_720p(3)
            else:
                set_480p(1)
                set_480p(2)
                set_480p(3)

            ret1, img1 = cam1.read()
            ret2, img2 = cam2.read()
            ret3, img3 = cam3.read()

            t_now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

            cam1.release()
            cam2.release()
            cam3.release()

            if ret1 == True:
                print("Captured image {} from camera 1!".format(n))
            else:
                print("Image {} not captured from camera 1!".format(n))

            if ret2 == True:
                print("Captured image {} from camera 2!".format(n))
            else:
                print("Image {} not captured from camera 2!".format(n))

            if ret3 == True:
                print("Captured image {} from camera 3!".format(n))
            else:
                print("Image {} not captured from camera 3!".format(n))
            
            img_name1 = "minibus_{}.jpg".format(t_now)
            img_file_path1 = os.path.join(img_path, img_name1)
            cv2.imwrite(img_file_path1, img1)

            img_name2 = "minibus_{}.jpg".format(t_now)
            img_file_path2 = os.path.join(img_path, img_name2)
            cv2.imwrite(img_file_path2, img2)

            img_name3 = "minibus_{}.jpg".format(t_now)
            img_file_path3 = os.path.join(img_path, img_name3)
            cv2.imwrite(img_file_path3, img3)

        elif args.cameras == 2:
            cam1 = cv2.VideoCapture(0)
            cam2 = cv2.VideoCapture(2)

            if args.resolution == 1080:
                set_1080p(1)
                set_1080p(2)
            elif args.resolution == 720:
                set_720p(1)
                set_720p(2)
            else:
                set_480p(1)
                set_480p(2)

            ret1, img1 = cam1.read()
            ret2, img2 = cam2.read()

            t_now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

            cam1.release()
            cam2.release()

            if ret1 == True:
                print("Captured image {} from camera 1!".format(n))
            else:
                print("Image {} not captured from camera 1!".format(n))

            if ret2 == True:
                print("Captured image {} from camera 2!".format(n))
            else:
                print("Image {} not captured from camera 2!".format(n))

            img_name1 = "minibus_{}.jpg".format(t_now)
            img_file_path1 = os.path.join(img_path, img_name1)
            cv2.imwrite(img_file_path1, img1)

            img_name2 = "minibus_{}.jpg".format(t_now)
            img_file_path2 = os.path.join(img_path, img_name2)
            cv2.imwrite(img_file_path2, img2)

        else:
            
            cam1.capture(rawCap, format="bgr")
            image = rawCap.array
            #cam1 = cv2.VideoCapture(0)

            # if args.resolution == 1080:
            #     set_1080p(1)
            # elif args.resolution == 720:
            #     set_720p(1)
            # else:
            #     set_480p(1)

            # ret1, img1 = cam1.read()

            t_now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

            # cam1.release()

            # if ret1 == True:
            #     print("Captured image {} from camera 1!".format(n))
            # else:
            #     print("Image {} not captured from camera 1!".format(n))

            img_name1 = "minibus_{}.jpg".format(t_now)
            img_file_path1 = os.path.join(img_path, img_name1)
            cv2.imwrite(img_file_path1, image)
            rawCap.truncate(0)


        # check temp
        temp = subprocess.check_output(['vcgencmd', 'measure_temp'])
        
        # send images
        headers = {
            'filename' : img_name1,
            'temp' : str(temp)[2:-3]
        }

        if args.cameras == 3: 
            files = [
                ('file', open(img_file_path1, 'rb')),
                ('file', open(img_file_path2, 'rb')),
                ('file', open(img_file_path3, 'rb'))
            ]
        elif args.cameras == 2:
            files = [('file', open(img_file_path1, 'rb')), ('file', open(img_file_path2, 'rb'))]
        else:
            files = [('file', open(img_file_path1, 'rb'))]

        r = requests.post(url, headers=headers, files=files)
        if r.status_code == 200:
            print("Successfully sent image {}!".format(n))
        else:
            print('Image {} not sent!'.format(n))
        
        time.sleep(sleep_time)  # 10 sec sleep

        # delete images
        if args.cameras == 3:
            print("Deleting image {} from camera 1!".format(n))
            os.remove(os.path.join(img_path, img_name1))
            print("Deleting image {} from camera 2!".format(n))
            os.remove(os.path.join(img_path, img_name2))
            print("Deleting image {} from camera 3!".format(n))
            os.remove(os.path.join(img_path, img_name3))
        elif args.cameras == 2:
            print("Deleting image {} from camera 1!".format(n))
            os.remove(os.path.join(img_path, img_name1))
            print("Deleting image {} from camera 2!".format(n))
            os.remove(os.path.join(img_path, img_name2))
        else:
            print("Deleting image {} from camera 1!".format(n))
            os.remove(os.path.join(img_path, img_name1))

        n += 1