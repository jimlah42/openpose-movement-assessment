import numpy as np

# heel -> knee, knee to hip, midhip to neck, neck to nose + offset

def calculate_pixel_cm_ratio(height:int, points):

    total_dist = 0
    offset = 10

    total_dist += get_distance("LHeel", "LKnee", points)
    total_dist += get_distance("LKnee", "LHip", points)
    total_dist += get_distance("MidHip", "Neck", points)
    total_dist += get_distance("Neck", "Nose", points)
    total_dist += offset


    return total_dist / height


def get_distance(point1, point2, points) -> float:
    """Calculates euclidean distance between two points from keypoint data

    Args:
        points (dict): object containing keypoint data for one frame 

    Returns:
        float: calculated distance value in pixels
    """
    p1 = points[point1]
    p2 = points[point2]

    if ((p1[0] == 0 and p1[1] == 0) or (p2[0] == 0 and p2[1] == 0)):
        distance = None
    else:
        distance = np.linalg.norm(np.asarray(p1) - np.asarray(p2))
    if (distance == None):
        return 0
    return distance