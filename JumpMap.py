import pyperclip, re

LINE_PATTERN = re.compile(r"""
^
# --- Address ---
(?P<address>0x[0-9a-fA-F]+)
\s*
# --- Relative Address ---
(?P<rel_address>[<(]\+\d+[)>]:)
\s*
# --- Operation ---
(?P<operation>.*?)
# --- Comment ---
(?P<comment>\s*[;#].*)?
$
""", re.VERBOSE)

asm_code = pyperclip.paste()

for line in asm_code.splitlines():
    match = LINE_PATTERN.match(line.strip())
    if not match:
        continue
    if match.group('operation')[0] == 'j':
        print(match.group('rel_address'), match.group('operation'))
