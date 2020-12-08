"""def p_command_for_to(p):
    command  : FOR iterator FROM value TO value DO commands ENDFOR
    print(variables)
    print(iterators)
    v1 = p[4]
    v2 = p[6]
    m1, m2 = spawn_frogs_multiple(2)
    prepared_regs = standard_render(v1, v2, 'e', 'f', str(p.lineno(4))) + render_addr(p[2], str(p.lineno(2)), 'c')
    save_get_diff = 'STORE e c' + nl() + "SUB f e" + nl()
    update_regs = nl() + 'DEC f' + nl() \
                  + p[8] \
                  + 'INC e' + nl()
    loop = m2 + 'JZERO f ' + frogs[m1] + update_regs + 'STORE e c' + nl() + 'JUMP ' + frogs[m2] + nl() + m1
    p[0] = pack(prepared_regs + save_get_diff + loop, '<<for_to>>')
    remove_iterator(p[2][1])"""

with open('/home/piotr/Documents/studies/compiler/methd', 'r') as f:
    content = f.read()

    for line in content.split('\n'):
        line = line.replace('\'a\'', 'X')
        line = line.replace('\'d\'', '\'a\'')
        line = line.replace('X', '\'d\'')
        print(line)
