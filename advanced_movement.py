from pololu_3pi_2040_robot import robot
import time

# Initialize components
motors = robot.Motors()
encoders = robot.Encoders()
display = robot.Display()

# Adjust these values based on your robot's performance
SIDE_LENGTH = 1000  # Encoder counts for 15 cm forward (example value)
HALF_SIDE_LENGTH = SIDE_LENGTH // 2 # Half the length of SIDE_LENGTH
GAP_LENGTH = SIDE_LENGTH // 4 # Length of gaps in between each potted plant
TURN_ANGLE = 217  # Further reduced encoder counts for a 90-degree turn (adjust as needed)
MOTOR_SPEED = motors.MAX_SPEED // 6  # Set motor speed to half of maximum speed

# Function to move the robot forward by a specific encoder count
def move_forward(target_counts):
    left_start, right_start = encoders.get_counts()  # Get initial encoder counts
    motors.set_speeds(MOTOR_SPEED, MOTOR_SPEED)
    
    while True:
        left_current, right_current = encoders.get_counts()
        left_diff = left_current - left_start
        right_diff = right_current - right_start
        
        if left_diff >= target_counts and right_diff >= target_counts:
            break

        # Display encoder counts for debugging
        display.fill_rect(40, 48, 64, 16, 0)
        display.text(f"L: {left_diff:>8}", 0, 48)
        display.text(f"R: {right_diff:>8}", 0, 56)
        display.show()
    
    motors.set_speeds(0, 0)  # Stop the motors

# Function to turn the robot 90 degrees right
def turn_right(target_counts):
    left_start, right_start = encoders.get_counts()  # Get initial encoder counts
    motors.set_speeds(MOTOR_SPEED, -MOTOR_SPEED)
    
    while True:
        left_current, right_current = encoders.get_counts()
        left_diff = left_current - left_start
        right_diff = right_current - right_start
        
        if left_diff >= target_counts and abs(right_diff) >= target_counts:
            break

        # Display encoder counts for debugging
        display.fill_rect(40, 48, 64, 16, 0)
        display.text(f"L: {left_diff:>8}", 0, 48)
        display.text(f"R: {right_diff:>8}", 0, 56)
        display.show()

    motors.set_speeds(0, 0)  # Stop the motors

# Function to turn the robot 90 degrees left
def turn_left(target_counts):
    left_start, right_start = encoders.get_counts()  # Get initial encoder counts
    motors.set_speeds(-MOTOR_SPEED, MOTOR_SPEED)  # Reverse the left motor, move the right motor forward
    
    while True:
        left_current, right_current = encoders.get_counts()
        left_diff = left_current - left_start
        right_diff = right_current - right_start

        # Check if both motors have reached the target
        if abs(left_diff) >= target_counts and right_diff >= target_counts:
            break

        # Display encoder counts for debugging
        display.fill_rect(40, 48, 64, 16, 0)
        display.text(f"L: {left_diff:>8}", 0, 48)
        display.text(f"R: {right_diff:>8}", 0, 56)
        display.show()

    motors.set_speeds(0, 0)  # Stop the motors




# PROCESSES

def sweep_row_process(c):
    for i in range(c):
        sweep_plant_process()
        move_forward(SIDE_LENGTH)
        time.sleep(0.5)
        
        if (i != c-1):
            move_forward(GAP_LENGTH)
            time.sleep(0.5)
    
def sweep_plant_process():
    for i in range(4):
        move_forward(HALF_SIDE_LENGTH)
        time.sleep(3) # 3 seconds to take a photo of the plant
        # INSERT "TAKE A PHOTO" FUNCTION HERE
        move_forward(HALF_SIDE_LENGTH)
        time.sleep(0.5)
        turn_right(TURN_ANGLE)
        time.sleep(0.5)

def even_transition_process():
    turn_left(TURN_ANGLE)
    time.sleep(0.5)
    move_forward(GAP_LENGTH)
    time.sleep(0.5)
    turn_left(TURN_ANGLE)
    time.sleep(0.5)

def odd_transition_process():
    turn_right(TURN_ANGLE)
    time.sleep(0.5)
    move_forward(SIDE_LENGTH)
    time.sleep(0.5)
    move_forward(GAP_LENGTH)
    time.sleep(0.5)
    move_forward(SIDE_LENGTH)
    time.sleep(0.5)
    turn_right(TURN_ANGLE)
    time.sleep(0.5)
    

def even_home_process(r):
    turn_right(TURN_ANGLE)
    time.sleep(0.5)
    
    for i in range(r):
        move_forward(SIDE_LENGTH)
        time.sleep(0.5)
        
        if (i != r-1):
            move_forward(GAP_LENGTH)
            time.sleep(0.5)
    
    turn_right(TURN_ANGLE)
    time.sleep(0.5)

def odd_home_process(c, r):
    turn_right(TURN_ANGLE * 2)
    time.sleep(0.5)
    
    for i in range(c):
        move_forward(SIDE_LENGTH)
        time.sleep(0.5)
        
        if (i != c-1):
            move_forward(GAP_LENGTH)
            time.sleep(0.5)
    
    turn_right(TURN_ANGLE)
    time.sleep(0.5)
    
    for i in range(r - 1):
        move_forward(SIDE_LENGTH)
        time.sleep(0.5)
        
        if (i != r-1):
            move_forward(GAP_LENGTH)
            time.sleep(0.5)
    
    turn_right(TURN_ANGLE)
    time.sleep(0.5)





# Main loop to move in a 15 cm square pattern
def main ():
    # Change these to control how many rows and columns the robot should navigate.
    cols = 2
    rows = 3
    
    for i in range(rows):
        sweep_row_process(cols)
    
        if i < rows - 1:  # Ensure a transition only happens if there is a next row
    
            if i % 2 == 0:
                even_transition_process()
            else:
                odd_transition_process()
    
    if (rows % 2 == 0):
        even_home_process(rows)
    else:
        odd_home_process(cols, rows)
    
    # Stop the robot after completing the square
    motors.set_speeds(0, 0)
        
main()