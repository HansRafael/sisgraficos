import pyautogui as pygui
import Quartz
import LaunchServices
from Cocoa import NSURL
import Quartz.CoreGraphics as CG
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
from Quartz.CoreGraphics import CGEventCreateScrollWheelEvent

class GestureControl():
    def __init__(self) -> None:
        self.sizeScreen = pygui.size()

    def mouseEvent(self, type, posx, posy):
        theEvent = CGEventCreateMouseEvent(
                    None, 
                    type, 
                    (posx,posy), 
                    kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)

    def mouse_move(self, posx,posy):
        self.mouseEvent(kCGEventMouseMoved, posx,posy)

    def scroll_wheel(self, num_times, upOrDown):
        for i in range(1, num_times):
            multiplier = 1 - (float(i) / num_times)
            speed = (4 * multiplier) * upOrDown
            event = CGEventCreateScrollWheelEvent(None, 0, 1, speed)
            CGEventPost(kCGHIDEventTap, event)

    def mouse_click(self,posx,posy):
        self.mouseEvent(kCGEventLeftMouseDown, posx,posy)
        self.mouseEvent(kCGEventLeftMouseUp, posx,posy)

    def take_screenshot(self, path):
        dpi = 72
        region = CG.CGRectInfinite

        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        url = NSURL.fileURLWithPath_(path)
        dest = Quartz.CGImageDestinationCreateWithURL(
            url,
            LaunchServices.kUTTypePNG, 1, None
            )
        prop = {
            Quartz.kCGImagePropertyDPIWidth: dpi,
            Quartz.kCGImagePropertyDPIHeight: dpi,
            }
        Quartz.CGImageDestinationAddImage(dest, image, prop)
        Quartz.CGImageDestinationFinalize(dest)
