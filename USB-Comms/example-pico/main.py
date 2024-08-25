import machine
import time
import sys
import select

def example():

    # initialize a "heap" - an array of bytes that we will constantly append to until we are ready to process what is there (i.e. a newline character/break character is in there)
    heap:bytes = bytes()

    # infinite loop to receive, process, and send
    while True:
        
        # read and collect all that are available, while there is some available
        while select.select([sys.stdin], [], [], 0)[0]: # there is at least 1 byte available to be read
            data:bytes = sys.stdin.buffer.read(1) # collect that 1 byte (1 byte at a time)
            heap = heap + data # append it to the heap
        
        # handle what was received if there is a sequence split in it
        # the sequence split just means the client (PC) has written what it intended to write. Usually a newline (\n or \r\n) character, but you can set it to whatever you want.
        split_sequence:bytes = "\r".encode()
        while split_sequence in heap: # if the heap has the split sequence in it

            # extract the first chunk, split from the rest by a split sequence
            split_position:int = heap.find(split_sequence) # find where the split sequence is
            chunk:bytes = heap[0:split_position] # extract the first chunk, but not the split sequence
            heap = heap[split_position + 1:] # set the heap to the remainder, stripping out both the first chunk and the split sequence

            # handle this chunk
            print("Chunk: " + str(chunk))
            
        # handle what needs to be done (processing, reacting to inputs, etc.)
        print("Hello at time " + str(time.ticks_ms()) + "!")
        
        # small wait period
        time.sleep(0.5)

example()