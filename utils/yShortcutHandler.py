from utils import yDebugger

if __name__ == "__main__":
    print("Yardımcı modüldür, direkt olarak kullanılamaz")

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

#############################################
#            EVRENSEL DEĞİŞKENLER           
#############################################

SHORTCUT = (162, 164, 36) # CTRL + ALT + HOME

isShortcut = False
list_press = [False, False, False]

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
    yDebugger.debugInfo("Kısayol aktif")

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

