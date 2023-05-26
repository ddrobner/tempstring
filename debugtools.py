from globals import globalmanager
from memory_profiler import profile

def memoryprofile(fn):
    return profile(fn) if globalmanager.getParam("debug") else fn