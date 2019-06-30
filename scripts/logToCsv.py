#@title CSV'e çevirici{ vertical-output: true, display-mode: "form" }

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pandas

#############################################
#            EVRENSEL DEĞİŞKENLER           
#############################################

NAME = "29-30.06.2019"  #@param {type:"string"}
DIR_LOGS = "keylogs"  #@param {type:"string"}
DEBUG = True  #@param {type:"boolean"}
to_drive = True #@param {type:"boolean"}

PATH_TO_LOGS = f"/content/drive/My Drive/Documents/KeyLogs/Logs/{NAME}.rar"  #@param {type:"string"}
PATH_TO_CSV = f"/content/drive/My Drive/Documents/KeyLogs/Csv/{NAME}.csv"  #@param {type:"string"}

if to_drive:
  if 'mount' not in locals() or not mount:
      from google.colab import drive
      drive.mount('/content/drive')
      mount = True


if 'copied' not in locals() or not copied:
  !mkdir -p "{DIR_LOGS}" && \
  cp "{PATH_TO_LOGS}" "{DIR_LOGS}" && \
  cd "{DIR_LOGS}" && unrar e *.rar && \
  rm -rf *.rar  && \
  rm "{PATH_TO_CSV}"
  copied = True

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

if DEBUG:
  print(f"File count: {num_log}")
  print()

for log in loglist:
    logpath = os.path.join(DIR_LOGS, log)
    num_log = num_log - 1
    
    try:
      if DEBUG:
        print(f"The file that is converting: '{logpath}'")
        print(f"Remaining File: {num_log}")
        print()
    
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
      print(f"Size of csv: {len(pandas.read_csv(PATH_TO_CSV))}")
      print()

print("Finished")
