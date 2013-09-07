
DEBUG_SIM = False


def traceMe():
    if DEBUG_SIM:
        from pydevd import settrace
        settrace(suspend = False, trace_only_current_thread = False)