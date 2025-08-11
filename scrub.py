# For scrubbing addresses and comments off of assembly code
# James Wilde

import pyperclip, re, sys, pyautogui, time

LINE_PATTERN = re.compile(r"""
^
# --- Address ---
(?P<address>0x[0-9a-fA-F]+)
\s*
# --- Relative Address ---
(?P<rel_address><\+\d+>:)
\s*
# --- Operation ---
(?P<operation>.*?)
# --- Comment ---
(?P<comment>\s*[;#].*)?
$
""", re.VERBOSE)

def main():
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)

    args = "".join(sys.argv[1:]).lower()

    try:
        asm_code = pyperclip.paste()
        if not asm_code:
            print("\nWarning: Clipboard is empty. Exiting now")
            return
    except pyperclip.PyperclipException as e:
        print(f'\nError: Unable to access clipboard.\nDetails: {e}')
        return

    scrubbed_asm_code = []
    for line in asm_code.splitlines():
        match = LINE_PATTERN.match(line.strip())
        if not match:
            if 'c' in args:
                scrubbed_asm_code.append(line)
            continue

        scrubbed_line = []

        # add in address line if not scrubbed
        if 'a' not in args:
            scrubbed_line.append(match.group('address'))

        # add in relative address line if not scrubbed
        if 'r' not in args:
            scrubbed_line.append(match.group('rel_address'))

        # add in operation line
        scrubbed_line.append(match.group('operation'))

        # add in comment line if not scrubbed
        if 'c' not in args:
            scrubbed_line.append(match.group('comment'))

        scrubbed_asm_code.append(' '.join(scrubbed_line))

    final_output = '\n'.join(scrubbed_asm_code)
    print("Done! Final output:\n")
    pyperclip.copy(final_output)

if __name__ == "__main__":
    main()
