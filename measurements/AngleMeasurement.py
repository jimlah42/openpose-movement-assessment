from measurements.Measurement import Measurement
import numpy as np
import cv2

class AngleMeasurement(Measurement):
    """Measurement of the angle between two points pivoting around a third point
    Inherits Measurement type
    """
    def __init__(self, name, point1, point2, pivot):
        super().__init__(name)
        self.type = "Angle"
        self.point1 = point1
        self.point2 = point2
        self.pivot = pivot
        self.convert_pixel_to_cm = False
    
    def calculate(self, points) -> float:
        """Calculates the angle between two points pivoting around a third points

        Args:
            points (dict): object containing keypoint data for a frame

        Returns:
            float: calculated angle in degrees
        """
        p1 = points[self.point1]
        p2 = points[self.point2]
        piv = points[self.pivot]

        p1ToPivot = np.asarray(p1) - np.asarray(piv)
        p2ToPivot = np.asarray(p2) - np.asarray(piv)

        cosine_angle = np.dot(p1ToPivot, p2ToPivot) / (np.linalg.norm(p1ToPivot) * np.linalg.norm(p2ToPivot))
        angle = np.arccos(cosine_angle)

        return np.degrees(angle)

    def draw(self, points, value, frame):
        """Draws a black line from p1 to pivot then from pivot to p2 and displays the name and value a the pivot

        Args:
            points (dict): object containing keypoint data for a frame
            value (float): angle value in degrees
            frame (cv2 image array): frame to modify 

        Returns:
            cv2 image array: modified frame
        """
        p1 = list(map(int, points[self.point1]))
        p2 = list(map(int, points[self.point2]))
        pivot = list(map(int, points[self.pivot])) 

        frame = cv2.line(frame, tuple(p1), tuple(pivot), (0,0,0), 9)
        frame = cv2.line(frame, tuple(p2), tuple(pivot), (0,0,0), 9)
        frame = cv2.putText(frame, self.name + ": " + str(round(value,2)), tuple(pivot), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)


        return frame


    def info_readable(self) -> str:
        return str("Angle between " + self.point1 + " and " + self.point2 + " pivoting around " + self.pivot)
    
    def params(self):
        return {
            "point1": self.point1,
            "point2": self.point2,
            "pivot": self.pivot
        }