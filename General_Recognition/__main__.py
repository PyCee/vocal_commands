#!/usr/bin/env python3

import Speech_Handler as sh

handler = sh.Speech_Handler()

running = True
launch_count = 0
climb_count = 0
hi_count = 0

def launch():
    global launch_count
    launch_count += 1
    print("Launching")
def climb():
    global climb_count
    climb_count += 1
    print("Climbing")
def increment_hi():
    global hi_count
    hi_count += 1
    print("Greetings")
def stop():
    global handler
    handler.stop()

keyword_callbacks = [
    ["fire", launch, 1e-90],
    ["climb", climb, 1e-90],
    ["hi", increment_hi, 1e-900],
    ["stop", stop, 1e-90]
]

handler.start(keyword_callbacks)

while handler.is_active():
    pass

print("Program is ending because you said \'Stop\'")
print("You \'Launched\' vocally " + str(launch_count) + " time(s)")
print("You told me to climb " + str(climb_count) + " time(s)")
print("You said \'hi\' " + str(hi_count) + " time(s)")
