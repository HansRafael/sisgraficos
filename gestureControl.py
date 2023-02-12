import pyautogui as pygui

class GestureControl():
    def __init__(self) -> None:
        self.sizeScreen = pygui.size()

    def mouse_move(self, posx,posy):
        pygui.moveTo(posx,posy)

    def scroll_wheel(self, num_times, upOrDown):
        pygui.scroll(num_times*upOrDown)
            
    def mouse_click(self,posx,posy):
        pygui.click()

    def take_screenshot(self, path):
        pygui.screenshot(path)
