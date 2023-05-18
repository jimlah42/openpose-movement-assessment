class Measurement:
    """Base interface for any measurement type being created
    """
    def __init__(self, name):
        self.name = name
        self.type = "unknown"

    def calculate(self, points) -> float:
        """Calculates given measurement value based of keypoint from frame

        Args:
            points (dict): object containing all keypoint values for one frame

        Returns:
            float: value of calculation
        """
        print("Calculate method not overidden")
        return(-1)


    def draw(self, points, value, frame):
        """Performs cv2 drawing actions to visualise given measurement

        Args:
            points (dict): object containing all keypoint vaules for one frame 
            value (float): measurement value for given frame
            frame (cv2 frame): cv2 image array for given frame
        """
        print("Draw not overridden")
        return(frame)

    def info_readable(self) -> str:
        """Generates human readable information describing the given measurement

        Returns:
            str: Human readable string
        """
        return self.name + " (Default method not overidden)"

    def params(self) -> object:
        """Returns parameters of the measurment as an object
        This is to allow for the object to be rebuilt when read from json

        Returns:
            object: parameters of the object as keys with values
        """
        return "Defualt not overridden"