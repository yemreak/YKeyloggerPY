#############################################
#               SABİT DEĞERLER              
#############################################

LVL_DEBUG = 2 # Tuş basımı dahil her bilgiyi gösterir 
LVL_INFO = 1  # Ek bilgileri de gösterir
LVL_NONE = 0  # Çıktı yok

#############################################
#            EVRENSEL DEĞİŞKENLER           
#############################################

LOG_LVL = LVL_NONE

def debugInfo(message):
    if LOG_LVL >= LVL_INFO:
        print(message)


def debugDebug(message):
    if LOG_LVL >= LVL_DEBUG:
        print(message)


def setLogLvl(lvl):
    global LOG_LVL
    LOG_LVL = lvl

    debugInfo("Loglama aktif")
