import tkinter as tk
import PiMotor
import time

m1 = PiMotor.Stepper("STEPPER1")
m2 = PiMotor.Stepper("STEPPER2")


        
root = tk.Tk()
root.title("Arrow Buttons")

frame = tk.Frame(root)

frame.pack(fill=tk.BOTH, expand=True)

frame.columnconfigure(1, weight=1)
frame.rowconfigure(1,weight=1)

button_up = tk.Button(frame, text="Up", command=m2.backward(float(2.5) / 1000.0, int(4)))
button_down = tk.Button(frame, text="Down", command=m2.forward(float(2.5) / 1000.0, int(4)))
button_left = tk.Button(frame, text="Left", command=m1.backward(float(3) / 1000.0, int(4)))
button_right = tk.Button(frame, text="Right", command=m1.forward(float(3) / 1000.0, int(4)))

button_up.grid(row=0, column=1, padx=5, pady=5)
button_down.grid(row=2, column=1, padx=5, pady=5)
button_left.grid(row=1, column=0, padx=5, pady=5)
button_right.grid(row=1, column=2, padx=5, pady=5)

root.mainloop()


