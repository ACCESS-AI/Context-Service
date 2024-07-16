#!/usr/bin/env python3

import os
os.makedirs("out")

def write_png():
    import shutil
    shutil.copyfile("task/ball.png", "ball.png")

def write_csv():
    with open("out/data.csv", "w") as f:
        f.write("'a','b','cdef'\n1,2,3")

def write_binary():
    pattern = b'\x00\xFF\x00\xFF' * 256
    with open("out/data.mybin", "wb") as f:
        f.write(pattern)

write_png()
write_csv()
write_binary()

