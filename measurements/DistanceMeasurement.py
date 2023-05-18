from measurements.Measurement import Measurement
import numpy as np
import cv2

class DistanceMeasurement(Measurement):
    """Measurement of the euclidean distance between two points
    Inherits Measurement type

    """
    def __init__(self, name, point1, point2):
        super().__init__(name)
        self.type = "Distance"
        self.point1 = point1
        self.point2 = point2
        self.convert_pixel_to_cm = True
    
    def calculate(self, points) -> float:
        """Calculates euclidean distance between measurements two points from keypoint data

        Args:
            points (dict): object containing keypoint data for one frame 

        Returns:
            float: calculated distance value in pixels
        """
        p1 = points[self.point1]
        p2 = points[self.point2]

        if ((p1[0] == 0 and p1[1] == 0) or (p2[0] == 0 and p2[1] == 0)):
            distance = None
        else:
            distance = np.linalg.norm(np.asarray(p1) - np.asarray(p2))
        return distance


    def draw(self, points, value, frame):
        """Draws a black line between two points and text with name and value at the midpoint of the two points

        Returns:
            cv2 image array: modified frame
        """
        
        if (value != None):

            p1 = list(map(int, points[self.point1]))
            p2 = list(map(int, points[self.point2]))
            midpoint = [int((p1[0]+p2[0])/2),int((p1[1]+p2[1])/2)]

            frame = cv2.line(frame, tuple(p1), tuple(p2), (0,0,0), 9)
            frame = cv2.putText(frame, self.name + ": " + str(round(value,2)), tuple(midpoint), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        return frame


    def info_readable(self) -> str:
        return str("Distance between " + self.point1 + " and " + self.point2)

    def params(self):
        return {
            "point1": self.point1,
            "point2": self.point2,
        }