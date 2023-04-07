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
from semver import Version
from pydantic import BaseModel


class VersionBump(BaseModel):
    version: str

    def bump(self, commit_messages: list[str]) -> "VersionBump":
        """
        Bumps the version based on the commit messages.

        Args:
            commit_messages (list[str]): The commit messages to use for bumping the version.

        Returns:
            VersionBump: A new VersionBump object with the bumped version.
        """
        version = Version.parse(self.version)

        if any("BREAKING CHANGE" in message for message in commit_messages):
            return VersionBump(version=str(version.bump_major()))
        elif any(message.strip().startswith('feat') for message in commit_messages):
            return VersionBump(version=str(version.bump_minor()))
        elif any(message.strip().startswith("fix") for message in commit_messages):
            return VersionBump(version=str(version.bump_patch()))
        
        return VersionBump(version=str(version))
    
def get_version() -> VersionBump:
    """
    Gets the version from the "pyproject.toml" file.

    Returns:
        VersionBump: A VersionBump object with the version.
    """
    with open("pyproject.toml", "r") as f:
        for line in f:
            if line.startswith("version"):
                return VersionBump(version=line.split("=")[1].strip().replace('"', ''))
            
def write_version(version: VersionBump) -> None:
    """
    Writes the version to the "pyproject.toml" file.

    Args:
        version (VersionBump): The version to write to the file.
    """
    with open("pyproject.toml", "r") as f:
        lines = f.readlines()
        
    with open("pyproject.toml", "w") as f:
        for line in lines:
            if line.startswith("version"):
                f.write(f'version = "{version.version}"\n')
            else:
                f.write(line)

def main() -> None:
    """
    The main entry point for the script. Assumes that "git" is installed.
    Makes an assumption that the first argument is the tag to use for the
    version bump.

    If the first argument is "--version", then the version will be printed
    to the console.

    Example:
        python build/semver_bump.py trunk

        or

        python build/semver_bump.py --version

    Raises:
        ValueError: If the first argument is not a valid tag.

    Returns:
        None: None
    """
    import sys
    import subprocess

    if sys.argv[1] == "--version":
        print(get_version().version)
        return
    
    write_version(
        get_version().bump(
            subprocess.run([
                "git", "log", "--format=%B", "--no-merges",
                f"{sys.argv[1]}..HEAD"],
                capture_output=True
            ).stdout.decode(
                "utf-8"
            ).split("\n")
        )
    )

if __name__ == "__main__":
    main()
