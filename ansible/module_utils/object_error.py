# -*- coding: utf-8 -*-

# Copyright (c) 2018 Michail Topaloudis
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Yama: Base Object with Error Collecting abilities.
<ansible.module_utils.remote_management.yama.object_error>"""

import sys


class ErrorObject(object):
    """Error Collector
    """
    messages = []
    reseterrors = False # Reset errors before every command call.

    def __init__(self):
        """Init - Does nothing at the moment.
        """
        pass

    def err(self, code=0, message=''):
        """The function that receives the errors.

        :param code: (int) Error ID
        :param message: (str) Message
        :return: (bool) False
        """
        getframe_expr = 'sys._getframe({}).f_code.co_name'
        self.messages.append(eval(getframe_expr.format(2)) \
                            + ':{0}:{1}'.format(code, message))
        return False

    def err0(self):
        """Empties the error list.

        :return: (bool) True
        """
        self.messages = []
        return True

    def errc(self):
        """Counts the number of errors.

        :return: (int) Number of errors
        """
        return len(self.messages)

    def errors(self):
        """Prints the errors.

        :return: (str) Concatenated string with all messages
        """
        return '\n'.join(self.messages)
