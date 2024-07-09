import pyperclip
c = 1
cp = str([pyperclip.paste()]).replace("[", '').replace("]", '').replace("", '').replace("'", '').replace('"', '')
if c:
    pyperclip.copy(cp)
