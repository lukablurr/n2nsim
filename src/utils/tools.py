from subprocess import call


def run_cmd(args):
    print("Run command: %s" % (" ".join(args)))
    retval = call(args)
    if retval:
        print("Command exit code: %d" % retval)
        raise Exception("Failed to run command!")

