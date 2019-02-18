# -*- coding: utf-8 -*-


class Error(Exception):
    """Error code with traceback

    Attributes:
        error_code (int): Error code
        message (str): Erorr message
    """

    def __init__(self, error_code, message):
        """init with error_code and message

        Args:
            error_code (int): Error code
            message (str): Error message
        """
        self.error_code = error_code
        self.message = message

    def __str__(self):
        """Error message

        Returns:
            str: Error message
        """
        return self.message

    def __int__(self):
        """Error code

        Returns:
            int: Error code
        """
        return self.error_code
