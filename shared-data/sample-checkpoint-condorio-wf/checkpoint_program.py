#!/usr/bin/env python3
import argparse
import os
import signal
import sys
import time
import traceback

from pathlib import Path

def parse_args(args):
    parser = argparse.ArgumentParser(
            description="A checkpointing toy program that will print"
            " [0 - num_iterations) while sleeping 1 second between each iteration. If a TERM"
            " is received, the current number will be written to a file (saved_state.txt) so that"
            " the program may resume where it left off. The program will first check for"
            " the existence of the checkpoint file in cwd and use it if it exists."
        )
    
    parser.add_argument(
        "num_iterations",
        type=int,
        help="number of iterations (seconds to run for)"
    )

    return parser.parse_args()

if __name__=="__main__":
    args = parse_args(sys.argv[1:])
    CHECKPOINT_FILE = "saved_state.txt"
    NUM_ITERATIONS = args.num_iterations
    
    # initial starting point
    i = 0
    try:
        
        # use checkpoint file if it exists
        try:
            with open(CHECKPOINT_FILE, mode="r") as f:
                i = int(f.read())
                
                # with nonsharedfs, we don't need a placeholder file
                # but have this here as an example anyway
                if i == -1:
                    i = 0
                    print("placed holder file: {} found, starting with i = 0".format(CHECKPOINT_FILE))
                else:
                    print("{} found, starting with i = {}".format(CHECKPOINT_FILE, i))
        except FileNotFoundError as e:
            print("{} not found, starting with i = 0".format(CHECKPOINT_FILE))

        # define SIGTERM handler
        # because of scope, we have access to i in here
        def SIGTERM_handler(signum, frame):
            print("Signal: {} received, writing checkpoint file with state {} to {}".format(
                    signum, i, CHECKPOINT_FILE
                ))

            with open(CHECKPOINT_FILE, mode="w") as f:
                f.write(str(i))

        # set handler
        signal.signal(signal.SIGTERM, SIGTERM_handler)

        # start computation 
        print("pid: {}".format(os.getpid()))
        for _ in range(NUM_ITERATIONS):
            # for testing
            #if i == 10:
            #    os.kill(os.getpid(), signal.SIGTERM)
            
            # for testing
            #if i == 2:
            #    raise RuntimeError("oops something went wrong")

            print(i)

            if i == NUM_ITERATIONS - 1:
                break

            i += 1
            time.sleep(1)
    except Exception as e:
        traceback.print_exc()
    finally:
        # if we encounter an error during computation, save state
        # else save state anyway as we may want to continue from this point
        # in the future
        with open(CHECKPOINT_FILE, mode="w") as f:
            f.write(str(i))
            
        print("writing checkpoint file: {} with state {}".format(CHECKPOINT_FILE, i))
    

'''
alternatively use functools.partial to create closure

from functools import partial

def handler(global_var, signal, frame):
    print(global_var)

def main():
    g_var = "test"
    signal.signal(signal.SIGTERM, partial(handler, g_var))
'''

