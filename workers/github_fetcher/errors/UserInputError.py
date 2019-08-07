class UserInputError(Exception):
    """
    Exception representing invalid user input such as command line arguments.
    Alternatively, this can also represented a problem caused by
    invalid user input further down the line.
    Simply put, the problem can / must be fixed by modifying the user input.

    Attributes:
        message {string} -- Error message to print.
        code {int} -- Exit code to use.
    """

    def __init__(self, message, code=1):
        self.message = message
        self.code = code

