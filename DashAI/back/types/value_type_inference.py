import numpy as np
import pandas as pd

import re
#Rules for detections, it is temporarily so later it would be implemented inside classes on value_types.py

def number_inference(column, sample_size=100, treshold=0.7):

    #Si es número, debería implicar casteo a float. posteriormente

    number_pattern = r"[-]?(\d+[,\.]\d*|\d*[,\.]\d+|\d+)"
    
    if len(column) < sample_size:
        sample_size = len(column)
        

    random_values = df[column].sample(n=sample_size)

    count = 0
    for value in random_values:
        str_value = str(value)
        if re.match(number_pattern, str_value):
            print(str_value, " is a number")
            count+=1
    
    if count/sample_size >= treshold:
        return "number"
    else:
        return "non-numeric"
    
def date_inference(column, sample_size=100, treshold=0.7):
    date_pattern = r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"
    
    if len(column) < sample_size:
        sample_size = len(column)
        

    random_values = df[column].sample(n=sample_size)

    count = 0
    for value in random_values:
        str_value = str(value)
        if re.match(date_pattern, str_value):
            print(str_value, " is a date")
            count+=1
    
    if count/sample_size >= treshold:
        return "date"
    else:
        return "non-date" 


















data = {
    "Forma A": ["1,5", "2,3", "4,7", "0,1", "-3,14", "5,0", "0,6", "-2,5", "10,0", "3,14159"],
    "Forma B": ["1.5", "2.0", "3.00", "0.25", "-4.5", "0.0", "7.00", "-0.1", "2.8", "-5.678"],
    "Forma C": [1.50, 2.0, 3.4, 0.80, -6.0, 8.00, -2.2, 4.0, 9.0, 0.90],
    "Forma D": [",5", ",33", ",0", ",55", ",0", ",0", ",25", ",0", ",10", ",01"],
    "Forma E": [".5", ".33", ".0", ".55", ".0", ".0", ".25", ".0", ".10", ".01"],
    "Forma F": ["4", 54, "3,4", "1.2", 1.4, "membrillo", "caracol", "1,5", "2,3", "4,7"],
}

df = pd.DataFrame(data)


for column in df.columns:
    print(column)
    print(column, number_inference(column))
    print()