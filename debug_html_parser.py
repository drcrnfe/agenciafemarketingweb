from html.parser import HTMLParser
from pathlib import Path

html = Path('index.html').read_text(encoding='utf-8')

class DebugParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        print(f"ENDTAG: </{tag}> at line {self.getpos()[0]} col {self.getpos()[1]}")

p = DebugParser()
p.feed(html)
print('Done')
