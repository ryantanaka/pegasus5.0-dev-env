#!/usr/bin/env python3
import sys
try:
    import tensorflow as tf
except ModuleNotFoundError:
    print("test requires tensorflow 2.3")
    sys.exit(1)

tf.debugging.set_log_device_placement(True)
# Create some tensors
a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
c = tf.matmul(a, b)

print(c)
