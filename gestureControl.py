import pyautogui as pygui
import sys


class gestureControll():
    def __init__(self) -> None:
        self.sizeScreen = pygui.size()

    def mouseMovement(self, x:int, y:int):
        pygui.moveTo(x, y)

    def clickMovemnt(self, x:int, y:int, clicks=1):
        pygui.click(x, y, clicks)

