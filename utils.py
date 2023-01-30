
import math

def get_area_box(boxArea) -> float:
    return (boxArea[2] - boxArea[0]) * (boxArea[3] - boxArea[1]) // 100

def get_center_rectangle(boxArea) -> tuple[int]:
    xCenter = (boxArea[0] + boxArea[2]) / 2
    yCenter = (boxArea[1] + boxArea[3]) / 2
    return xCenter, yCenter

def get_distance(indexFingerTip, middleFingerTip) -> float:
    xIndex, yIndex = indexFingerTip[1], indexFingerTip[2]
    xMiddle, yMiddle = middleFingerTip[1], middleFingerTip[2]
    return(math.dist([xIndex,yIndex], [xMiddle, yMiddle]))