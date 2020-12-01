def label_to_line(text):
    stack = list(jump_label.keys())
    for i, line_content in enumerate(text.split('\n')):
        if re.match('~~LABELJUMPTO>[0-9]+<~~',line_content):
            print('success')