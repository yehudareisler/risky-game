class Logger:
    @staticmethod
    def log(message, verbose):
        if verbose:
            print(message)
