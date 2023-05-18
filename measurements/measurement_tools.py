from typing import List
import json
from measurements.Measurement import Measurement
from measurements.DistanceMeasurement import DistanceMeasurement
from measurements.AngleMeasurement import AngleMeasurement

def get_measurement_objects(path: str) -> List[Measurement]:
    """Reads keypoints json file and builds all measurement objects

    Args:
        path (str): path to output/{file_name} folder

    Returns:
        List[Measurement]: List of Measurement objects read from file
    """
    
    try:
        with open(str(path + "/keypoints.json")) as json_file:
            jsondata = json.load(json_file)
        measurements = jsondata["measurements_info"]
    except:
        measurement_objects = []
        return measurement_objects
    
    measurement_objects = []
    for measurement in measurements:
        name = measurement["name"]
        type = measurement["type"]
        params = measurement["params"]
        if (type == "Distance"):
            measurement_obj = DistanceMeasurement(name, params["point1"], params["point2"])
        elif (type == "Angle"):
            measurement_obj = AngleMeasurement(name, params["point1"], params["point2"], params["pivot"])

        measurement_objects.append(measurement_obj)
    
    return measurement_objects

