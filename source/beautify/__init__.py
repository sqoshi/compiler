import subprocess

tags = False


def gc():
    subprocess.call(".bash gc.bash 2>/dev/null")


def remove_marks(text, labels):
    stack = list(labels.keys())
    line_no = dict()
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for k in stack:
            if k in line:
                line_no[k] = i
                lines[i] = lines[i].replace(k, "")
    for i, line in enumerate(lines):
        for k, v in labels.items():
            if v in line:
                try:
                    lines[i] = line.replace(v, str(line_no[k] - i))
                except KeyError:
                    pass
    result = '\n'.join(lines)
    return result


def concat(*args):
    return ' '.join(args)


def nl() -> str:
    return "\n"


def pack(txt, tag="##"):
    if tags:
        return '[' + tag + ']' + " " + txt + " " + '[' + tag[-2:] + tag[2:-2] + tag[:2] + ']'
    else:
        return txt


def unpack(text: str) -> str:
    output = ""
    for line in text.split("\n"):
        if line != '':
            output += line.lstrip() + "\n"
    return output


def mark(labels_dict):
    val = len(labels_dict)
    key = '~~LABELJUMPTO>' + str(val) + '<~~'
    labels_dict[key] = '~~LABEL>' + str(val) + '<~~'
    return key
