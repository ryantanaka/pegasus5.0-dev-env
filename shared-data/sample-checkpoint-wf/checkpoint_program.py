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
            " [0-100) while sleeping 1 second between each iteration. If a TERM"
            " is received, the current number will be written to a file so that"
            " the program may resume where it left off."
        )

    parser.add_argument(
                "-c",
                "--checkpoint",
                type=str,
                help="the checkpoint file to resume from"
            )

    return parser.parse_args()

if __name__=="__main__":
    args = parse_args(sys.argv[1:])

    i = 0

    if args.checkpoint:
        try:
            with open(args.checkpoint, "r") as f:
                i = int(f.read())
        except FileNotFoundError as e:
            print("Checkpoint file: {} not found".format(args.checkpoint))
            sys.exit(1)
    
    def SIGTERM_handler(signum, frame):
        CHECKPOINT_FILE = Path(".") / "saved_state.txt"
        print("Signal: {} received, writing checkpoint file with state {} to {}".format(
                signum, i, CHECKPOINT_FILE.resolve()
            ))

        with CHECKPOINT_FILE.open(mode="w") as f:
            f.write(str(i))

    signal.signal(signal.SIGTERM, SIGTERM_handler)

    print("pid: {}".format(os.getpid()))
    for _ in range(100):
        if i == 100:
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

