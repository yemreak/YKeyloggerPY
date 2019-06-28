#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pandas

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
for log in loglist:
    logpath = os.path.join(DIR_LOGS, log)
    
    try:
      if DEBUG:
        print(f"The file that is converting: '{logpath}'")
    
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
      
    print(len(pandas.read_csv(PATH_TO_CSV)))
