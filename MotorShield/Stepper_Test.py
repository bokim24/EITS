import PiMotor
import time

m1 = PiMotor.Stepper("STEPPER1")
m2 = PiMotor.Stepper("STEPPER2")

# Rotate Stepper 1 Contiously in forward/backward direction


while True:
    # Delay and rotations
    delay = input("Motor 1: Delay between steps(ms)?")

    steps = input("Motor 1: How many steps forward?")

    m1.forward(float(delay) / 1000.0, int(steps))

    delay = input("Motor 1: Delay between steps(ms)?")

    steps = input("Motor 1: How many steps backward?")

    m1.backward(float(delay) / 1000.0, int(steps))

    delay = input("Motor 2: Delay between steps(ms)?")

    steps = input("Motor 2: How many steps forward?")

    m2.forward(float(delay) / 1000.0, int(steps))

    delay = input("Motor 2: Delay between steps(ms)?")

    steps = input("Motor 2: How many steps backward?")

    m2.backward(float(delay) / 1000.0, int(steps))
    
        
    
