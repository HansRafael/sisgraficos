import pyautogui as pygui
import sys
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
from Quartz.CoreGraphics import CGEventCreateScrollWheelEvent

class gestureControll():
    def __init__(self) -> None:
        self.sizeScreen = pygui.size()

    def mouseEvent(self, type, posx, posy):
        theEvent = CGEventCreateMouseEvent(
                    None, 
                    type, 
                    (posx,posy), 
                    kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)

    def mousemove(self, posx,posy):
        self.mouseEvent(kCGEventMouseMoved, posx,posy)

    def scrollWheel(self, num_times, upOrDown):
        for i in range(1, num_times):
            multiplier = 1 - (float(i) / num_times)
            speed = (4 * multiplier) * upOrDown
            event = CGEventCreateScrollWheelEvent(None, 0, 1, speed)
            CGEventPost(kCGHIDEventTap, event)

    def mouseclick(self,posx,posy):
        # uncomment this line if you want to force the mouse 
        # to MOVE to the click location first (I found it was not necessary).
        #mouseEvent(kCGEventMouseMoved, posx,posy);
        self.mouseEvent(kCGEventLeftMouseDown, posx,posy)
        self.mouseEvent(kCGEventLeftMouseUp, posx,posy)