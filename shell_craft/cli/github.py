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
from dataclasses import dataclass
from urllib.parse import urlencode, urljoin


@dataclass
class GitHubArguments:
    title: str
    labels: list[str]
    body: str

    def as_url(self, repository: str) -> str:
        """
        Generates a URL to open an issue or feature request for the
        GitHub repository.

        Args:
            repository (str): The URL to the GitHub repository.

        Returns:
            str: The URL to open an issue or feature request for the
                GitHub repository.
        """        
        return (
            urljoin(
                repository.rstrip('/') + '/',
                'issues/new'
            )
            + '?'
            + urlencode({
                'title': self.title,
                'labels': ','.join(self.labels),
                'body': self.body
            })
        )
    
    @staticmethod
    def from_prompt(prompt: str) -> 'GitHubArguments':
        """
        Parses data from

        ```
        ---
        name: <Name Of Bug>
        about: <Short Description>
        labels: < Documentation, Enhancement, Question, Bug, etc. >
        ---

        <body>
        ```
        """
        tokens = prompt.split('---')

        if len(tokens) != 3:
            raise ValueError('Invalid prompt.')
        
        _, metadata, body = tokens

        tokens = metadata.split('\n')
        metadata = {
            token.split(':')[0].strip(): ':'.join(token.split(':')[1:]).strip()
            for token in tokens
        }

        return GitHubArguments(
            title=metadata['name'],
            labels=metadata['labels'].split(','),
            body=metadata['about'] + '\n\n' + body.strip()
        )
