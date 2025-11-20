import time
from datetime import datetime

def load_data(filename):
    try:
        with open(filename, "r") as file:
            return eval(file.read())
    except:
        return{}
    
def save_data(filename,data):
    with open(filename, )