from constants import ErrorType, messages
import datetime

# Error class to return from function containing info
class BotError:
    # Initialize with the type of error (int code), and location where it occurred (string name of function)
    def __init__(self, type, location, suppress_print=False):
        self.type = type
        self.location = location
        self.supress_print = suppress_print

    # String representation of error
    def __str__(self):
        return f"{datetime.datetime.now()}::ERROR: {messages[self.type]} @ {self.location}"

    # Log error and return true if it is an error
    def log(self):
        # If is an error
        if not self.type == ErrorType.NO_ERROR:
            # Log to a file, print error, print, and return True
            with open("log.txt", "a") as errLog:
                errLog.write(str(self)+"\n")
            if not self.supress_print: print(str(self))
            return True
        else:
            # No error, return false
            return False