import cv2
import os
import sys
from tqdm import tqdm
from typing import List
from measurements.Measurement import Measurement
import json
import traceback

class FrameCounter():
    """Class used to create progress bar in command line 
    """
    def __init__(self, max_frames):
        self.max_frames = max_frames
        self.current_frame = 0
        self.progress = 0

    def incre_frame(self):
        self.current_frame += 1
        self.progress = (self.current_frame/self.max_frames)*100

def draw_measurements(path: str, measurements: List[Measurement], anonymise: bool) -> bool:
    """Draws all measurements for a given processed video

    Args:
        path (str): path to output/{file_name} folder
        measurements (List[Measurement]): List of all measurements in file
        anonymise (bool): True if patient face should be blurred

    Returns:
        bool: True if successful
    """
    try:
        vid_path = path + "/video.avi"
        cap = cv2.VideoCapture(vid_path)
        width = cap.get(3)
        height = cap.get(4)
        fps = cap.get(5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        file_name = os.path.splitext(os.path.basename(vid_path))[0]
        if (total_frames < 1): total_frames = 1

        output_path = path
        print(output_path)
    
        with open(path + "/keypoints.json") as keypoints_file:
            keypoints = json.load(keypoints_file)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        location = output_path + '/video_with_measurements.avi'
        out = cv2.VideoWriter(location, fourcc, fps, (int(width),
            int(height)))
        

        #Command line progress bar
        frame_num = 0
        pbar = tqdm(total=100)
        progress = (1 / total_frames) * 100
        fc = FrameCounter(total_frames)

        while (cap.isOpened()):
            retrivedFrame, frame = cap.read()

            if (retrivedFrame):
                points = keypoints["keypoints"][frame_num]
                time = keypoints["measurements"][frame_num]["time_elapsed (s)"]

                output_frame = frame

                if (anonymise):
                    nose = points["Nose"]

                    if (nose[0] != 0 and nose[1] != 0):

                        w = 100
                        h = 80
                        x = int(nose[0])
                        if x < w: x = w
                        y = int(nose[1])
                        if y < h: y = h

                        face = output_frame[y-h:y+h, x-w:x+w]


                        face = cv2.GaussianBlur(face, (35,35), 30)

                        cv2.imshow("test", face)

                        output_frame[y-h:y+h, x-w:x+w] = face

                output_frame = cv2.putText(output_frame, "Time elapsed (s): " + str(round(time,2)), (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

                for measurement in measurements:

                    measurement_value = keypoints["measurements"][frame_num][measurement.name]
                    output_frame = measurement.draw(points, measurement_value, output_frame)

                

                cv2.imshow("Vid", output_frame)
                out.write(output_frame)

                frame_num += 1
                fc.incre_frame()
                pbar.update(progress)
            else:
                break


        cap.release()
        out.release()
        cv2.destroyAllWindows()
        pbar.close
        
        return True
    except Exception as e:
        print(e)
        traceback.print_exc()
        return False