import json
import csv
from typing import List
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np



def get_measurement_names(path: str) -> List[str]:
    """Reads keypoints json file and returns all names of measurements

    Args:
        path (str): path to output/{file_name} folder

    Returns:
        List[str]: List of measurement names
    """


    # print(str(path + "/keypoints.json"))
    
    with open(str(path + "/keypoints.json")) as json_file:
        jsondata = json.load(json_file)


    try:
        measurement_data = jsondata["measurements"]
    except:
        print("No measurements found")
        return []


    measurements = measurement_data[0].keys()

    return measurements


def generate_csv(json_path: str, measurements: List[str], filename: str) -> bool:
    """Generates .CSV (comma-seperated-values) file for given measurements

    Args:
        json_path (str): path to output/{file_name} containing the keypoints file to process
        measurements (List[str]): List of measurement names to include
        filename (str): file name to save the file as (".csv" will be added)

    Returns:
        bool: returns True if sucessful 
    """

    if (len(measurements) < 1):
        return False

    with open(str(json_path + "/keypoints.json")) as json_file:
        jsondata = json.load(json_file)

    csv_file = open(str(json_path + "/" + filename + ".csv"), "w", newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(measurements)

    measurement_data = jsondata["measurements"]

    for frame in measurement_data:
        row = [] 
        for measurement in measurements:
            row.append(frame[measurement])
         
        csv_writer.writerow(row)

    csv_file.close()

    return True


def generate_plot(json_path: str, title:str, measurements: List[str]):
    """Generates pyplot graph for given measurements read from a keypoints file
    If time_elapse is not included X-axis will be frames

    Args:
        json_path (str): path to output/{file_name} containing the keypoints file to process
        title (str): title of the plot 
        measurements (List[str]): List of measurement names to include in the plot

    """
    
    if (len(measurements) < 1):
        return False

    with open(str(json_path + "/keypoints.json")) as json_file:
        jsondata = json.load(json_file)


    measurement_data = jsondata["measurements"]
    
    measurement_array = []
    use_time = False
    frame_nums = []
    frame_no = 0



    for i, measurement in enumerate(measurements):
        measurement_array.append([])
        if (measurement == "time_elapsed (s)"):
            use_time = True
        for frame in measurement_data: 
            if (not use_time):
                frame_nums.append(frame_no)
                frame_no += 1
            measurement_array[i].append(frame[measurement])

    
    for i, measurement in enumerate(measurements):

        if (use_time):
            if (i > 0):
                measurement_array[i] = signal.savgol_filter(measurement_array[i], window_length=11, polyorder=3, mode="nearest")
                plt.plot(measurement_array[0], measurement_array[i], label= measurement)
        else:
            measurement_array[i] = signal.savgol_filter(measurement_array[i], window_length=11, polyorder=3, mode="nearest")
            plt.plot(frame_nums, measurement_array[i], label= measurement)


    plt.legend(loc='best')    
    plt.title(title)
    plt.show()

