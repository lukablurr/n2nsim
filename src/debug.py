DEBUG_SIM = False


def traceMe():
    if DEBUG_SIM:
        import pydevd
        pydevd.settrace(suspend = False)
        pydevd.GetGlobalDebugger().setExceptHook(Exception, True, False)