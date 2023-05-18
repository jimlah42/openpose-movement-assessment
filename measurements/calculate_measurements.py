import json
from measurements.Measurement import Measurement
from typing import List

def calculate(path: str, measurements: List[Measurement]) -> bool:
    """Calculates the measurement values for each measurement on each frame, outputs to "keypoints" json file in output

    Args:
        path (str): path to output/{file_name} folder 
        measurements (List[Measurement]): List of all measurement objects to be processed

    Returns:
        bool: returns True if no errors occur
    """
    try:
        with open(path + "/keypoints.json") as keypoints_file:
            keypoints = json.load(keypoints_file)


        keypoints["measurements_info"] = []

        for measurement in measurements:
            
            keypoints["measurements_info"].append({
                "name": measurement.name,
                "type": measurement.type,
                "info": measurement.info_readable(),
                "params": measurement.params()
            })



        keypoints["measurements"] = []
        frame = 0
        for points in keypoints["keypoints"]:
            
            keypoints["measurements"].append({})

            for measurement in measurements:

                value = measurement.calculate(points)
                
                keypoints["measurements"][frame]["time_elapsed (s)"] = frame / keypoints["vid_info"]["fps"]


                if (not measurement.convert_pixel_to_cm):
                    keypoints["measurements"][frame][measurement.name] = value
                else:
                    ratio = keypoints["vid_info"]["pixel-cm-ratio"]
                    if (value != None):
                        keypoints["measurements"][frame][measurement.name] = value / ratio
                    else:
                        keypoints["measurements"][frame][measurement.name] = value


            frame += 1
        

        with open(path + "/keypoints.json", 'w') as outfile:
            json.dump(keypoints, outfile, indent=4)
        
        return True
    except Exception as e:
        print(e)
        return False
