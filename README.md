# Electric_vehicle_DashBoard

Hello coders, this is a project of electric vehical dashboard design with several functionality using PyQt (Qt framework).

## Description 
  I made this dashboard.py as a PyQt QWidget type, so you can embed this with your existing QMainWindow application by importing it or you can also use this as a stand-alone application for other purposes. At this point you have a question of how to do that? that's why I also provide a demo1.py and demo2.py file. 
### The demo1.py file 
  It is to demonstrate of how you can use the dsahboard.py as a stand-alone application and how to connect the vehical state to the dashboard.
### The demo2.py file 
  It is to demonstrate of how you can use the dashboard.py as a sub QWidget with your PyQt application and how to connect the vehical state to the dashboard.

## Features 
### Basic features contains
    1) This module provide a electric vehical dashboard dimension of 16:9 aspect ratio (default size 1280x720).
    2) You can able resize respect to 16:9 aspect ratio.
    3) Header with date-time display and break light display.
    4) Speedometer with auto reset to 0 kmph enable or disable option.
    5) Speedometer range adjustment from 40 to 400 kmph. default range is 0 to 200 kmph.
    6) Battery percentage indicator.
    7) Charging state indicator.
    8) Accelerator state indicator.
    9) Break state indicator.
    10) Horn state indicator.
    11) Left and right turn indicator.
  Note:
    You can control the above states by using, several function provided in 'TriggerAction' class.
### Some cool features:
    1) Start page with start button and creator info button.
    2) Loading screen (launch after start button pressed).
    3) You can skip any of the above pages or both page.
    3) dashboard popup animation.
    4) you can also embed this dashboard with your own application created using PyQt by using 'DashBoard' class.
    
## Provided functions with discription

### DashBoard() 
  This is a pyqt widget class to embed the dashboard to other pyqt widgets or applications.
  #### class functions
  1) show_dashboard(hide_creator_button: bool = False, skip_start_screen: bool = False, skip_loading_screen: bool = False) - To show dashboard in parent window
  
### TriggerAction() 
  This class contain all functionality settings of dashboard.
#### class functions
  1) launch_dashboard() - Open dashboard as seperate window
  2) set_dashboard_size(width: int, height: int) - To set dashboard
  3) hide_creator_button(hide: bool) - To hide creator info button
  4) skip_start_screen(skip: bool) - To skip start screen and directly go to loding screen
  5) skip_loading_screen(skip: bool) - To skip loading screen and directly go to dashboard screen
  6) set_speedometer_range(top_speed: int) - To set speedometer range
  7) apply_accelerator() - To activate accelerator
  8) release_accelerator() - To deactivate accelerator
  9) set_speed(current_speed: int) - To update current speed
  10) set_speedometer_resetter_state(state: bool) - To turn on or off speedometer internal reset function to 0 kmph after accelerator release
  11) apply_break() - To activate break
  12) release_break() - To deactivate break
  13) sound_horn() - To activate horn
  14) off_horn() - To deactivate horn
  15) left_indicator_on_or_off() - On or off left indicator
  16) right_indicator_on_or_off() - On or off right indicator
  17) update_battery_power(current_battery_power: int) - To set current battery power level in percentage
  18) charging_on() - To indicate charging is on
  19) charging_off() - To indicate charging is off
    
## Output

https://user-images.githubusercontent.com/78413761/219974154-664373d3-62d0-4a67-8669-e143cdd564b1.mp4
    
## Conclusion 
  If you found any bug or you want any feature kindly inform it.
  If you want any application like this fell free to contact me. the contact info given below.
    
## Contact:

 YouTube : https://www.youtube.com/channel/UC8W9MLLVK0wZjg9DwJiyivQ

 Mail address : k.prasannagh@gmail.com

 Follow me on instagram : https://www.instagram.com/prasanna_rdj_fan
