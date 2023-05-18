#Based off OpenPose Python Examples and Brighton Li Thesis vid_pose.py

import sys
import cv2
import os
from sys import platform
import argparse
from tqdm import tqdm
import json
import numpy as np
from utils.key_points import key_points 
from utils.height import calculate_pixel_cm_ratio

def process_video(vid_path: str, patient_data: object):
    """Processes raw video with OpenPose and generates keypoints json and video output
    in "output/{video_name}
    Reading OpenPose flags from opParams.json

    Args:
        vid_path (str): absolute path to video file
        patient_data (object): object contatining patient data
    """
    try:
        # Import Openpose (Windows/Ubuntu/OSX)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            # Windows Import
            if platform == "win32":
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append(dir_path + './python/openpose/Release')
                os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + './x64/Release;' +  dir_path + './bin;'
                import pyopenpose as op
            else:
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append('../python')
                # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
                # sys.path.append('/usr/local/python')
                from openpose import pyopenpose as op
        except ImportError as e:
            print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

        class FrameCounter():
            def __init__(self, max_frames):
                self.max_frames = max_frames
                self.current_frame = 0
                self.progress = 0

            def incre_frame(self):
                self.current_frame += 1
                self.progress = (self.current_frame/self.max_frames)*100

        # Flags
        parser = argparse.ArgumentParser()
        args = parser.parse_known_args()

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        with open("openpose/opParams.json") as params_file:
            params = json.load(params_file)


        cap = cv2.VideoCapture(vid_path)
        width = cap.get(3)
        height = cap.get(4)
        fps = cap.get(5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if (total_frames < 1): total_frames = 1

        file_name = os.path.splitext(os.path.basename(vid_path))[0]

        output_path = "./output/" + str(file_name)

        if (not os.path.exists(output_path)):
            os.mkdir(output_path)

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        #Set video output to .avi as PyQt MediaPlayer doesnt support mp4 natively
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        location = output_path + '/video.avi'
        out = cv2.VideoWriter(location, fourcc, fps, (int(width),
            int(height)))


        
        #Command line progress bar
        frame_num = 0
        pbar = tqdm(total=100)
        progress = (1 / total_frames) * 100
        fc = FrameCounter(total_frames)


        json_data = { 
            "vid_info": {
                "fps": fps
            },
            "patient_data": patient_data,
            "keypoints": []
            }

        print("Starting Openpose processing")

        pixel_cm_ration_array = []

        while (cap.isOpened()):
            retrivedFrame, frame = cap.read()

            if (retrivedFrame):
                # Process Image
                datum = op.Datum()
                imageToProcess = frame 
                datum.cvInputData = imageToProcess
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))


                cv2.putText(imageToProcess, str(frame_num), (100,100), font, 1, 
                        (255,255,255), 1)
                json_data['keypoints'].append({})
                
                json_data['keypoints'][frame_num]["time_elapsed (s)"] = frame_num / fps
                if (datum.poseKeypoints is not None):
                    for key in key_points.keys():
                        json_data['keypoints'][frame_num][key] = [float(datum.poseKeypoints[0][key_points[key]][0]),float(datum.poseKeypoints[0][key_points[key]][1])]  
                else:
                    for key in key_points.keys():
                        json_data['keypoints'][frame_num][key] = [0, 0]

                output_frame = datum.cvOutputData

                pixel_cm_ration_array.append(calculate_pixel_cm_ratio(int(patient_data["height"]), json_data['keypoints'][frame_num])) 

                cv2.imshow("Vid", output_frame)
                out.write(output_frame)

                frame_num += 1
                fc.incre_frame()
                pbar.update(progress)
                key = cv2.waitKey(15)
                if key == 27: break
            else:
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        pbar.close
        print("Generating Json")


        json_data["vid_info"]["pixel-cm-ratio"] = np.median(pixel_cm_ration_array)
        #save to json
        with open(output_path + "/keypoints.json", 'w') as outfile:
            json.dump(json_data, outfile, indent=4)

    except Exception as e:
        print(e)
        cv2.destroyAllWindows()
