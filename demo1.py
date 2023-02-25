# This is to demonstration of how you can use the dsahboard.py as a stand-alone 
# application and how to connect the vehical state to the dashboard.

from dashboard import TriggerAction
import keyboard

trigger_action = TriggerAction()  # creating dashboard trigger

# the below five method should be called before calling launch_dashboard() method to take effect
# note: this below five are optional
trigger_action.set_dashboard_size(1366, 768)  # aspect ratio 16:9
trigger_action.hide_creator_button(False)
trigger_action.skip_start_screen(False)
trigger_action.skip_loading_screen(False)
trigger_action.set_speedometer_range(240)

def CustomkeyboardEvent(event):
    if event.event_type == 'down':  # assume key down event is active event of vehical properties
        if event.name == 'w':  # press accelerator
            trigger_action.apply_accelerator()
        if event.name == 'space':  # press break
            trigger_action.apply_break()
        if event.name == 'h':  # press horn
            trigger_action.sound_horn()
        if event.name == 'left':  # triger left indicator state
            trigger_action.left_indicator_on_or_off()
        if event.name == 'right':  # triger right indicator state
            trigger_action.right_indicator_on_or_off()

        # below is how to turn on or off speedometer resetter internal function
        if event.name == 'r':
            trigger_action.set_speedometer_resetter_state(False)
        if event.name == 'f':
            trigger_action.set_speedometer_resetter_state(True)

        # below is the demonstration of how to set speed, battery value and charging state 
        # press 'c' to watch changes
        if event.name == 'c':
            trigger_action.set_speed(150)
            trigger_action.update_battery_power(70)
            trigger_action.charging_on()
            #trigger_action.charging_off() # to off charging light

    if event.event_type == 'up':  # assume key up event is passive event vehical properties
        if event.name == 'w':  # release accelerator
            trigger_action.release_accelerator()
        if event.name == 'space':  # release break
            trigger_action.release_break()
        if event.name == 'h':  # release horn
            trigger_action.off_horn()

        # here indicator is not called because basically indicator is a 
        # toggle switch not a push button

# key hook 
key_hook = keyboard.hook(CustomkeyboardEvent)

# to show dashboard note: this should be called at end of our code
trigger_action.launch_dashboard()  

print("finished")
