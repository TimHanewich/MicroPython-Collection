import machine
import time
import sys
import select

def example1():
    while True:
        
        # read all that are available, while there is some available
        received:bytes = bytes() # collection heap
        while select.select([sys.stdin], [], [], 0)[0]: # there is at least 1 byte available to be read
            data:bytes = sys.stdin.buffer.read(1) # collect that 1 byte
            received = received + data # append it to the heap
        
        # if there was some data that we received (all collected at once), handle it
        if len(received) > 0:
            print("Received data: " + str(received))
            
        # handle what needs to be done (processing, reacting to inputs, etc.)
        print("Hello at time " + str(time.ticks_ms()) + "!")
        
        # small wait period
        time.sleep(3)

def example2():
    while True:
        
        # If there is data available, what for it all to finish (until a newline character is received)
        if select.select([sys.stdin], [], [], 0)[0]: # there is at least 1 byte available to be read, so we are being sent something!
            
            # read the data line!
            # this will read the entirety of the bytes available to read, but will wait until the newline character is at the end to continue. 
            # This IS a blocking function, so the program will stop and sit here until the newline is received. 
            # In other words, it is sort of like "waiting for the PC (client) to finish sending what it is in the middle of sending".
            data:bytes = sys.stdin.buffer.readline() 

            # handle the data however necessary
            print("Just received this data: " + str(data))
            
            
        # handle what needs to be done (processing, reacting to inputs, etc.)
        print("Hello at time " + str(time.ticks_ms()) + "!")
        
        # small wait period
        time.sleep(0.5)

example2()