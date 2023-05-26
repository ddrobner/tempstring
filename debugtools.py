from globals import globalmanager
from memory_profiler import profile

def memoryprofile(fn):
    """Enables memory profiling if the debug flag is set

    Args:
        fn (function): The function being decorated

    Returns:
        function: The decorated function
    """
    return profile(fn) if globalmanager.getParam("debug") else fn