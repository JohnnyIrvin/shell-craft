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

def main() -> None:
    """
    The main entry point for the script. Assumes that "git" is installed.
    Makes an assumption that the first argument is the tag to use for the
    changelog.

    Example:
        python build/change_log.py trunk

    Raises:
        ValueError: If the first argument is not a valid tag.

    Returns:
        None: None
    """
    import sys
    import subprocess

    print(
        subprocess.run(
            [ 
                "git",
                "log",
                '--pretty=format:"[%H](https://github.com/JohnnyIrvin/shell-craft/commit/%H) %s ([%an](mailto:%ae))%C(auto)"',
                "--no-merges",
                "--source",
                f"{sys.argv[1]}..HEAD",
            ],
            capture_output=True,
            text=True,
        ).stdout
    )

if __name__ == "__main__":
    main()
