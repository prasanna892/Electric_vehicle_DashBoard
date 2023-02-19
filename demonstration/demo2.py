from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

from dashboard import DashBoard, TriggerAction
import keyboard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My DashBoard")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: blue;")
        
        self.dashboard_widget = DashBoard(self)
        self.dashboard_widget.move(0, 0)
        self.dashboard_widget.setFixedSize(880, 495)  # aspect ratio 16:9
        self.dashboard_widget.show_dashboard(skip_start_screen=True) # showing dashboard with start screen skipped

        self.dashboard_widget_action()

    def dashboard_widget_action(self):
        self.trigger_action = TriggerAction()  # creating dashboard trigger
        self.trigger_action.set_speedometer_range(100)
        self.trigger_action.charging_on()

        # key hook
        keyboard.hook(self.dashboard_widget_Key_event)

    def dashboard_widget_Key_event(self, event): # this kry function is same as what you see in demo1.py
        if event.event_type == 'down':  # assume key down event is active event of vehical properties
            if event.name == 'w':  # press accelerator
                self.trigger_action.apply_accelerator()
            if event.name == 'space':  # press break
                self.trigger_action.apply_break()
            if event.name == 'h':  # press horn
                self.trigger_action.sound_horn()
            if event.name == 'left':  # triger left indicator state
                self.trigger_action.left_indicator_on_or_off()
            if event.name == 'right':  # triger right indicator state
                self.trigger_action.right_indicator_on_or_off()

            # below is how to turn on or off speedometer resetter internal function
            if event.name == 'r':
                self.trigger_action.set_speedometer_resetter_state(False)
            if event.name == 'f':
                self.trigger_action.set_speedometer_resetter_state(True)

            # below is the demonstration of how to set speed, battery value and charging state 
            # press 'c' to watch changes
            # Note: setting speed, battery value and charging state before dashboard popup is not possible
            if event.name == 'c':
                self.trigger_action.set_speed(150)
                self.trigger_action.update_battery_power(70)
                self.trigger_action.charging_off()

        if event.event_type == 'up':  # assume key up event is passive event vehical properties
            if event.name == 'w':  # release accelerator
                self.trigger_action.release_accelerator()
            if event.name == 'space':  # release break
                self.trigger_action.release_break()
            if event.name == 'h':  # release horn
                self.trigger_action.off_horn()

            # here indicator is not called because basically indicator is a 
            # toggle switch not a push button


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

    print("finished")