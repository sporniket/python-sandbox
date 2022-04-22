# Colored console logs
# GNU GPL v3

MARKER_TRACE = "\033[90mTRACE\033[0m --"
MARKER_DEBUG = "\033[2mDEBUG\033[0m --"
MARKER_INFO = "\033[96mINFO \033[0m --"
MARKER_OK = "\033[92mOK   \033[0m --"
MARKER_WARN = "\033[93mWARN \033[0m --"
MARKER_ERROR = "\033[1;91mERROR\033[0m --"
MARKER_FATAL = "\033[1;101mFATAL\033[0m --"


def log(marker, message):
    print(f"{marker} {message}")

def trace(message):
    log(MARKER_TRACE, message)

def debug(message):
    log(MARKER_DEBUG, message)

def info(message):
    log(MARKER_INFO, message)

def ok(message):
    log(MARKER_OK, message)

def warn(message):
    log(MARKER_WARN, message)

def error(message):
    log(MARKER_ERROR, message)

def fatal(message):
    log(MARKER_FATAL, message)

### demo
if __name__ == "__main__":
    trace("hello trace")
    debug("hello debug")
    info("hello info")
    ok("hello ok")
    warn("hello warn")
    error("hello error")
    fatal("hello fatal")
