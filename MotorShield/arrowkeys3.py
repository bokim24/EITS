import sys,tty,termios
import PiMotor
import time
import picamera

m1 = PiMotor.Stepper("STEPPER1")
m2 = PiMotor.Stepper("STEPPER2")


class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        if k=='\x1b[A':
                print("up")
                m2.forward(float(3) / 1000.0, int(5))
        elif k=='\x1b[B':
                print("down")
                m2.backward(float(3) / 1000.0, int(5))
        elif k=='\x1b[C':
                print("right")
                m1.forward(float(3) / 1000.0, int(5))
        elif k=='\x1b[D':
                print("left")
                m1.backward(float(3) / 1000.0, int(5))
        else:
                print("not an arrow key!")

def main():
        while True:
                get()

if __name__=='__main__':
        main()
