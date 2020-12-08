def cmd(command, *r):
    brackets = len(r) * '{} '
    return command.upper() + " " + brackets[:-1].format(*r) + '\n'


print(cmd('resest', 'a', 'b'))
