import re

sc = re.compile("[0-9a-f]{2}\s")

mappings = []

with open("win-us-kai.klc", "r", encoding="UTF-16") as f:
    for line in f:
        line = line.strip()
        # Only lines with scan codes
        if not sc.match(line[:3]):
            continue
        # Remove comments
        if "//" in line:
            line = line[:line.index("//")]
        elements = line.split("\t")
        # Clean elements
        for i in range(len(elements) - 1, 0, -1):
            # Remove quotation marks
            elements[i] = elements[i].replace('"', '')
            # Remove empty elements
            if elements[i] == '':
                del elements[i]
        key = {}
        key["SC"] = elements[0]
        key["VK"] = elements[1]
        if len(elements) > 2:
            key["Cap"] = elements[2]
        if len(elements) > 3:
            key["Default"] = elements[3]
        if len(elements) > 4:
            key["Shift"] = elements[4]
        if len(elements) > 5:
            key["Ctrl"] = elements[5]
        if len(elements) > 6:
            key["AltGr"] = elements[6]
        if len(elements) > 7:
            key["Shift-AltGr"] = elements[7]
        mappings.append(key)

with open("out.ahk", "w", encoding="UTF-8") as f:
    for m in mappings:
        if "Default" in m:
            target = m["Default"]
            if len(target) == 4:
                target = "Send {{U+{}}}".format(target)
            f.write("SC0{}::{}\n".format(m["SC"], target))
        if "Shift" in m:
            target = m["Shift"]
            if len(target) == 4:
                target = "Send {{U+{}}}".format(target)
            f.write("+SC0{}::{}\n".format(m["SC"], target))
        if "AltGr" in m and m["AltGr"] != "-1":
            target = m["AltGr"]
            if len(target) == 4:
                target = "Send {{U+{}}}".format(target)
            f.write("<^>!SC0{}::{}\n".format(m["SC"], target))
            f.write(">!SC0{}::{}\n".format(m["SC"], target))
        if "Shift-AltGr" in m and m["Shift-AltGr"] != "-1":
            target = m["Shift-AltGr"]
            if len(target) == 4:
                target = "Send {{U+{}}}".format(target)
            f.write("+<^>!SC0{}::{}\n".format(m["SC"], target))
            f.write("+>!SC0{}::{}\n".format(m["SC"], target))
    with open('include.ahk', 'r', encoding='utf-8') as inc:
        for line in inc:
            f.write(line)
