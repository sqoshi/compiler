from source.parser import parser, frogs
from source.beautify import unpack, kill_frogs
import os
from termcolor import colored
from subprocess import PIPE, Popen, STDOUT


def test_compiler(f1, f2='/home/piotr/Documents/studies/compiler/result.mr'):
    mw = "/home/piotr/Documents/studies/compiler/virtual_machine/maszyna-wirtualna-cln"
    with open(f1, "r+") as f:
        with open(f2, "w+") as f_out:
            parsed = parser.parse(f.read(), tracking=True)
            clear = unpack(parsed)
            no_labels = kill_frogs(clear, frogs)
            f_out.write(no_labels)
    os.system('{} {}'.format(mw, f2))


path = "/home/piotr/Documents/studies/compiler/tests/gotests/tests/"
# path = "/home/piotr/Documents/studies/compiler/tests/gebatests/"
# path = "/home/piotr/Documents/studies/compiler/tests/gotests/errors/"
# path = "/home/piotr/Documents/studies/compiler/tests/examples/errors/"


def print_tests():
    my_tests = os.listdir(path)
    my_tests.sort()
    for i, x in enumerate(my_tests):
        print('{}. {}'.format(colored(i, 'yellow'), colored(x[:-4], 'green')))
    ch = int(input('Choose something :='))
    print(colored(my_tests[ch], 'blue'))
    test_compiler(f1=path + my_tests[ch])


print_tests()


def test_all(path='/home/piotr/Documents/studies/compiler/examples/tests', output='result.mr'):
    arr = [path + "/" + file for file in os.listdir(path) if
           os.path.isfile(os.path.join(path, file)) and '.imp' in file]
    for file in arr:
        with open(file, "r") as f:
            with open(output, "w") as f_out:
                try:
                    parsed = parser.parse(f.read(), tracking=True)
                    clear = unpack(parsed)
                    no_labels = kill_frogs(clear, frogs)
                    f_out.write(no_labels)
                    f_out.close()
                    command = "." + '/home/piotr/Documents/studies/compiler/virtual_machine/maszyna-wirtualna' + " " \
                              + output
                    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                    print('x' * 100)
                    for line in p.stdout:
                        line = line.rstrip()
                        print(colored(line, 'green'))
                    print('x' * 100)
                except:
                    pass


def test_errors(p1='/home/piotr/Documents/studies/compiler/examples/errors'):
    arr = os.listdir(p1)
    arr.sort()
    errs = len(arr)
    for file in arr:
        try:
            test_compiler(f1=p1 + file)
            print(colored('No Error in file {}'.format(file), 'green'))
            errs -= 1
        except:
            print(colored('Error in file {}'.format(file), 'yellow'))
    print('errors = len(arr) +> {}'.format(errs == len(arr)))


def tests_errors_all():
    test_errors('/home/piotr/Documents/studies/compiler/tests/gotests/errors')
    test_errors('/home/piotr/Documents/studies/compiler/tests/examples/errors/')
