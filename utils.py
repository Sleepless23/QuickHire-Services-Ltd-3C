import json
from datetime import datetime
import os

#hr pin for corrections 
HR_PIN = "1234"

#ensure exports and db folder exists
os.makedirs('exports', exist_ok=True)
os.makedirs('db', exist_ok=True)

#load json file
def load_json(file_name):
    if not os.path.exists(file_name):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        return []
    with open(file_name, 'r') as f:
        return json.load(f)

#save json file
def save_json(file_name, data):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

#get current timestamp string
def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#parse timestamp string to datetime
def parse_time(timestr):
    return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")

#validate integer input
def input_int(prompt):
    while True:
        val = input(prompt).strip()
        if val == "":
            print("Invalid input! Please enter a number.")
            continue
        if val.lstrip('-').isdigit():
            return int(val)
        print("Invalid input! Please enter a number.")

#validate non-negative integer
def input_pos_int(prompt):
    while True:
        v = input_int(prompt)
        if v >= 0:
            return v
        print("Please enter zero or a positive number.")

#validate float input
def input_float(prompt):
    while True:
        val = input(prompt).strip()
        if val == "":
            print("Invalid input! Please enter a number.")
            continue
        try:
            return float(val)
        except ValueError:
            print("Invalid input! Please enter a number.")

#validate non-empty string
def input_str(prompt):
    while True:
        val = input(prompt).strip()
        if val == "":
            print("Invalid input! Cannot be empty.")
            continue
        return val