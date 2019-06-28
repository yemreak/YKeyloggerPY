#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pandas

#############################################
#                 IPYNB ALANI           
#############################################

""" NAME = "28.06.2019"
DIR_LOGS = "keylogs"
PATH_TO_LOGS = f"/content/drive/My Drive/Documents/KeyLogs/Logs/{NAME}.rar"
PATH_TO_CSV = f"/content/drive/My Drive/Documents/KeyLogs/Csv/{NAME}.csv"

!rm "{PATH_TO_CSV}"
!mkdir -p "{DIR_LOGS}"
!cp "{PATH_TO_LOGS}" "{DIR_LOGS}"
!cd "{DIR_LOGS}" && unrar e *.rar
!rm -rf "{DIR_LOGS}"/*.rar """

#############################################
#            EVRENSEL DEĞİŞKENLER           
#############################################

NAME = "28.06.2019"
DIR_LOGS = "keylogs"
DEBUG = True

PATH_TO_LOGS = f"/content/drive/My Drive/Documents/KeyLogs/Logs/{NAME}.rar"
PATH_TO_CSV = f"/content/drive/My Drive/Documents/KeyLogs/Csv/{NAME}.csv"

COLUMNS = [
    "UTC Time",
    "Boot Time",
    "MessageName",
    "Message",
    "Window",
    "WindowName",
    "Ascii",
    "Key",
    "KeyID",
    "ScanCode",
    "Extended",
    "Injected",
    "Alt",
    "Transition"
]

DATA_FRAME = pandas.DataFrame(columns=COLUMNS)
COL_SIZE = len(DATA_FRAME.columns)

loglist = os.listdir(DIR_LOGS)
num_log = len(loglist)
for log in loglist:
    logpath = os.path.join(DIR_LOGS, log)
    num_log = num_log - 1
    
    try:
      if DEBUG:
        print(f"The file that is converting: '{logpath}'")
        print(f"Remaining File: {num_log}")
    
      if os.path.isfile(logpath):
          with open(logpath, "r", encoding = "utf-8") as file:
            i = 0
            data = []
            for line in file:
              if len(line.strip()) > 0:
                  index = line.index(":")
                  value = line[index + 1:].strip()
                  data.append(value)
                  
                  if len(data) == COL_SIZE:
                    DATA_FRAME.loc[i] = data
                    data.clear()
                    i += 1
                    
          with open(PATH_TO_CSV, "a+", encoding="utf-8") as file:
            DATA_FRAME.to_csv(file, header=file.tell()==0)
            DATA_FRAME.drop(DATA_FRAME.index, inplace=True)
                  
    except Exception as e:
      print(f"Error in {logpath}")
      print(e)
      print()
      
    if DEBUG:
      print(f"Size of csv: {sum(1 for _ in pandas.read_csv(PATH_TO_CSV))}")

print("Finished")
