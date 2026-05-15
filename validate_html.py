from html.parser import HTMLParser
from pathlib import Path

class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):
            return
        self.stack.append(tag)

    def handle_endtag(self, tag):
        # ignore end tags for void elements (may be emitted by parser for self-closing tags)
        if tag in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):
            return
        if not self.stack:
            self.errors.append(f'Unexpected closing </{tag}>')
            return
        if self.stack[-1] == tag:
            self.stack.pop()
            return
        if tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f'Missing closing </{self.stack[-1]}> before </{tag}>')
                self.stack.pop()
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
                return
        self.errors.append(f'Closing </{tag}> without open tag')

html = Path('index.html').read_text(encoding='utf-8')
parser = TagChecker()
parser.feed(html)
print('Unclosed tags:', parser.stack)
print('Errors:', parser.errors[:20])
