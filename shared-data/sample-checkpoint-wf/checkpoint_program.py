#!/usr/bin/env python3
import argparse
import os
import signal
import sys
import time

from pathlib import Path

def parse_args(args):
    parser = argparse.ArgumentParser(
            description="A checkpointing toy program that will print"
            " [0-90) while sleeping 1 second between each iteration. If a TERM"
            " is received, the current number will be written to a file (saved_state.txt) so that"
            " the program may resume where it left off. The program will first check for"
            " the existence of the checkpoint file in cwd and use it if it exists."
        )

    return parser.parse_args()

if __name__=="__main__":
    args = parse_args(sys.argv[1:])
    CHECKPOINT_FILE = "saved_state.txt"
    NUM_ITERATIONS = 90
    
    i = 0

    try:
        with open(CHECKPOINT_FILE, mode="r") as f:
            i = int(f.read())
            if i == -1:
                i = 0
                print("placed holder file: {} found, starting with i = 0".format(CHECKPOINT_FILE))
            else:
                print("{} found, starting with i = {}".format(CHECKPOINT_FILE, i))
    except FileNotFoundError as e:
        print("{} not found, starting with i = 0".format(CHECKPOINT_FILE))
    
    def SIGTERM_handler(signum, frame):
        print("Signal: {} received, writing checkpoint file with state {} to {}".format(
                signum, i, CHECKPOINT_FILE
            ))

        with open(CHECKPOINT_FILE, mode="w") as f:
            f.write(str(i))

    signal.signal(signal.SIGTERM, SIGTERM_handler)

    print("pid: {}".format(os.getpid()))
    for _ in range(NUM_ITERATIONS):
        # for testing
        #if i == 10:
        #    os.kill(os.getpid(), signal.SIGTERM)
        
        if i == NUM_ITERATIONS - 1:
            break

        print(i)
        i += 1
        time.sleep(1)

'''
alternatively use functools.partial to create closure

from functools import partial

def handler(global_var, signal, frame):
    print(global_var)

def main():
    g_var = "test"
    signal.signal(signal.SIGTERM, partial(handler, g_var))
'''

