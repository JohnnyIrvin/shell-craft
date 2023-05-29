# Copyright (c) 2023 Johnathan P. Irvin and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from os import getppid

from psutil import NoSuchProcess, Process


def get_calling_shell() -> str:
    """
    Get the name of the shell that called this script. This is used to determine
    the default prompt type. If the calling shell is PowerShell or pwsh, it is converted
    to "powershell" to match the prompt type. If the calling shell is not recognized,
    the default prompt type is "bash".

    If the calling shell cannot be determined, the default prompt type is "bash".

    Returns:
        str: The name of the shell.
    """
    try:
        return (
            "powershell" 
            if Process(getppid()).name() in 
            ["pwsh", "powershell"] else "bash"
        )
    except NoSuchProcess:
        return "bash"
