import textwrap
import termcolor
import time

class Logger:
    """Logger to control verbose printing"""
    def __init__(self, color="cyan", max_depth=10, debug_messages=False):
        self.keys = [""]
        self.color = color
        self.pending_newline = False
        self.max_depth = max_depth
        self.debug_messages = debug_messages

    def set_debug(self, debug_messages):
        self.debug_messages = debug_messages

    def set_depth(self, max_depth):
        self.max_depth = max_depth

    def __call__(self, key):
        return self.LoggerContext(self, key)

    class LoggerContext:
        def __init__(self, outer, key):
            self.outer = outer
            self.key = key
            self.start_time = None

        def __enter__(self):
            self.outer.enter(self.key)
            self.outer.keys += [self.key]
            self.start_time = time.time()

        def __exit__(self, exc_type, exc_value, traceback):
            end_time = time.time()
            duration = int((end_time - self.start_time) * 1000)
            self.outer.keys.pop()
            self.outer.exit(f"{duration} ms")

    def print_colored(self, message, *args, **kwargs):
        print(termcolor.colored(message, self.color), flush=True, *args, **kwargs)

    def _pad(self, message):
        return textwrap.indent(message, " " * ((len(self.keys) - 1) * 2))

    def enter(self, *args):
        if len(self.keys) > self.max_depth:
            return
        if self.pending_newline:
            self.print_colored("]")
            self.pending_newline = False
        message = " ".join(map(str, args))
        self.print_colored(self._pad(f"[{message}..."), end="")
        self.pending_newline = True

    def exit(self, *args):
        if len(self.keys) > self.max_depth:
            return
        message = " ".join(map(str, args))
        if self.pending_newline:
            self.print_colored(f" {message}]")
        else:
            self.print_colored(self._pad(f"[{message}]"))
        self.pending_newline = False

    def log(self, *args):
        if len(self.keys) > self.max_depth:
            return
        if self.pending_newline:
            self.print_colored("]")
            self.pending_newline = False
        message = " ".join(map(str, args))
        self.print_colored(self._pad(f"[{message}]"))

    def debug(self, *args):
        if self.debug_messages:
            self.log(*args)

    def print(self, *args, **kwargs):
        if self.pending_newline:
            self.print_colored("]")
            self.pending_newline = False
        print(*args, **kwargs)

    def error(self, *args, **kwargs):
        if self.pending_newline:
            self.print_colored("]")
            self.pending_newline = False
        print(*args, **kwargs)


# Create an instance of the logger
log = Logger()

if __name__ == "__main__":
    log = Logger(max_depth=10)
    # Test the logger
    with log("Main"):
        log.log("This is a log message")

    with log("No time"):
        log.log("This is a log message")
        with log("Beep"):
            log.log("This is a log message")
            with log("Boop"):
                log.print("Real messages")
                log.log("This is a log message")
                log.error("MOo")
            log.log("This is a log message")
        with log("Bop"):
            pass

