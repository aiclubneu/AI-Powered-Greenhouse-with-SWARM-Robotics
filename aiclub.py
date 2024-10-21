from pololu_3pi_2040_robot import robot
import time

# Initialize components
motors = robot.Motors()
encoders = robot.Encoders()
display = robot.Display()

# Adjust these values based on your robot's performance
SIDE_LENGTH = 1000  # Encoder counts for 15 cm forward (example value)
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

# Function to turn the robot 90 degrees
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

# Main loop to move in a 15 cm square pattern
for _ in range(4):
    move_forward(SIDE_LENGTH)  # Move forward by one side length
    time.sleep(0.5)  # Brief pause before turning
    turn_right(TURN_ANGLE)  # Turn right by 90 degrees
    time.sleep(0.5)  # Brief pause after turning

# Stop the robot after completing the square
motors.set_speeds(0, 0)
