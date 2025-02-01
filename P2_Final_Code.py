ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

import random 
#Rylan Ng & Daniel N.
def pickup(containers):
    arm.spawn_cage(randomNumber(containers)) #Spawns a random container
    arm.move_arm(0.567, 0.05, -0.006) #Moves arm to spawned container
    time.sleep(2)
    arm.control_gripper(35)
    time.sleep(2)
    arm.move_arm(0.406, 0.0, 0.483) #Moves arm with container to upright position
#Daniel N.
def randomNumber(numberlist):
    
    number = random.choice(numberlist) #Sets "number" equal to a random value from a list of integers from 1 to 6
    numberlist.remove(number) #Removes the value of number from list of integers
    if (number == 1) or (number == 4):
        print("Set right potentiometer to 24%") #Gives right potentiometer value for the red autoclave
    elif (number == 2) or (number == 5):
        print("Set right potentiometer to 96%") #Gives right potentiometer value for the green autoclave   
    elif (number == 3) or (number == 6):
        print("Set right potentiometer to 76%") #Gives right potentiometer value for the blue autoclave    
    return number
#Paddy E.
def rotation():
    
    item_dropped = False
    old_reading = potentiometer.right()
    while not item_dropped:
        #Loops rotation untill the container is in the proper position for a drop off
        if potentiometer.left() == 0.5:
            new_reading = potentiometer.right()
            delta = new_reading - old_reading
            increment = 348*delta #Sets degree of rotation to a value witin the range of motion of the arm base
            arm.rotate_base(increment) #Rotates the base of the arm by an increment with respect to the value of the right potentiometer
            old_reading = new_reading
        elif (potentiometer.left() == 0.0):
        #Moves the arm to drop off the container at the upper section of the autoclave
            drop_off(1)
            item_dropped = True
            reset_potentiometer()
            time.sleep(2)
        elif (potentiometer.left() == 1.0):
        #Moves the arm to drop off the container at the lower drawer of the autoclave
            drop_off(2)
            item_dropped = True
            reset_potentiometer()
            time.sleep(2)
#Daniel N.
def reset_potentiometer():
    #Creates a checkpoint for the arm to be reset for a new pickup
    
    while potentiometer.left() <= 1.0:
        if (potentiometer.left() == 0.5) and (potentiometer.right() == 0.5):
            arm.home()
            break
#Daniel N.   
def drop_off(position):
    
    if position == 1:
        #Moves arm to the upper section of the autoclave for the small container drop off
        arm.rotate_elbow(-33)
        arm.rotate_shoulder(45)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)   
    elif position == 2:
        #Moves arm to the lower section of the autoclave for the large container drop off
        check_openautoclave(False)
        time.sleep(2)
        arm.rotate_elbow(18)
        arm.rotate_shoulder(25)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)
        check_openautoclave(True)
#Daniel N. & Rylan Ng        
def check_openautoclave(is_open):
#Opens and closes the drawer of the corresponding autoclave that is within range of the arm
    
    if (arm.check_autoclave('blue') == True):
        if (is_open == False):
            arm.open_autoclave('blue')
        else:
            arm.open_autoclave('blue', False) 
    elif (arm.check_autoclave('red') == True):
        if (is_open == False):
            arm.open_autoclave('red')
        else:
            arm.open_autoclave('red', False)    
    elif (arm.check_autoclave('green') == True):
        if (is_open == False):
            arm.open_autoclave('green')
        else:
            arm.open_autoclave('green', False)   
#Daniel N.
def main():
    
    containerlist = [1, 2, 3, 4, 5, 6] #Defines a list containing values of containers to be spawned
    arm.activate_autoclaves()
    arm.home()
    for i in range(6):
    #Loops program until all 6 containers have been dropped off and terminates the program once complete
        pickup(containerlist)
        rotation()
        arm.move_arm(0.406, 0.0, 0.483)
    arm.deactivate_autoclaves()

main()

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

