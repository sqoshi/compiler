# Compiler

## Table of contents

* [Installation](#installation)
* [Launch](#launch)
* [Introduction](#Introduction)
* [General info](#general-info)
* [Code Example](#code-example)
* [Technologies](#technologies)

## Installation

```shell script
./install.sh
```

or

```shell script
bash install.sh
```

## Launch

```shell script
python3 compiler.py in_file out_file
```

## Introduction

Compiler takes some code in imperative language
(gębalang) defined by grammar in general info section (example below) and produces a machine code which is accepted by a
virtual machine attached in working tree( maszyna-wirtualna). We

### Example of imperative language (binary notation of a number)

```python
1
DECLARE
2
n, p
3
BEGIN
4
READ
n;
5
REPEAT
6
p := n / 2;
7
p := 2 * p;
8
IF
n > p
THEN
9
WRITE
1;
10
ELSE
11
WRITE
0;
12
ENDIF
13
n := n / 2;
14
UNTIL
n = 0;
15
END
```

### Example of compiled code (binary notation of a number)

```python
RESET a
STORE a a
INC a
STORE a a
INC a
GET a
LOAD a a
RESET b
ADD b a
SHR b
SHL b
RESET c
ADD c a
SUB c b
JZERO c 5
RESET d
INC d
PUT d
JUMP 3
RESET d
PUT d
SHR a
JZERO a 2
JUMP -16
HALT
```

## General Info

### Grammar

```python
program      -> DECLARE declarations BEGIN commands END
             | BEGIN commands END

declarations -> declarations, pidentifier
             | declarations, pidentifier(num:num)
             | pidentifier
             | pidentifier(num:num)

commands     -> commands command
             | command

command      -> identifier := expression;
             | IF condition THEN commands ELSE commands ENDIF
             | IF condition THEN commands ENDIF
             | WHILE condition DO commands ENDWHILE
             | REPEAT commands UNTIL condition;
             | FOR pidentifier FROM value TO value DO commands ENDFOR
             | FOR pidentifier FROM value DOWNTO value DO commands ENDFOR
             | READ identifier;
             | WRITE value;

expression   -> value
             | value + value
             | value - value
             | value * value
             | value / value
             | value % value

condition    -> value = value
             | value != value
             | value < value
             | value > value
             | value <= value
             | value >= value

value        -> num
             | identifier

identifier   -> pidentifier
             | pidentifier(pidentifier)
             | pidentifier(num)
```

### Numbers Generator
```python
    while number != 0:
    if number % 2 == 0:
        number = number // 2
        commands = concat("SHL", reg, nl(), commands)
    else:
        number -= 1
        commands = concat("INC", reg, nl(), commands)
```

We check the parity of number until we face 0 in number.

- When number is even perform shift left ( multiply by 2 )
- When number is odd perform shift left ( increase by 1 )

Reduce number in each iteration ( respectively /2 , -1).

### Arithmetic operations
#### Multiplication

We are checking parity of value in register b.

```python
while b > 0:
    if b % 2 == 0:
        a = a * 2
        b = b / 2
    else:
        ab = ab * a
        b = b - 1
```

##### Example 3 * 100

ab | a | b | b % 2 |
--- | --- | --- | --- |
0 | 3 | 100 |  True|
0 | 6 | 50 |  True|
0 | 12 | 25 |  False|
12 | 12 | 24 |  True|
12 | 24 | 12 |  True|
12 | 48 | 6 |  True|
12 | 96 | 3 |  False|
108 | 96 | 2 |  True|
108 | 192 | 1 |  False|
300 | 192 | 0 |  END|

#### Division and modulo

As we can see in example below same algorithm can be used to find result of mod and integer unsigned division.

##### Attempt #1

```python
    y_core = y
a = 0
while x >= y:
    R = 1
    y *= 2
    while x >= y:
        R *= 2
        y *= 2
    a += R
    x -= (y / 2)
    y = y_core
```

##### Example 39 / 100

a | b | c | d | A>B|
--- | --- | --- | --- | ---|
39 | 5 | 0 |  0| True  |
39 | 10 | 1 |  0|  True |
39 | 20 | 2 |  0|  True |
39 | 40 | 4 |  0|  False |
19 | 5 | 0 |  4|  True |
19 | 10 | 1 |  4|  True |
19 | 20 | 2 |  4|  False |
9 | 5 | 0 |  6|  True |
9 | 10 | 1 |  6| False  |
4 | 5 | 0 |  7|  False |

##### Attempt #2

```python
    a = 0
while d >= c:
    e = c
    f = 1
    while d >= e:
        f *= 2
        e *= 2
    f = f / 2
    e = e / 2
    d -= e
    a += f
```

## Code Example

#### Equality

```python
def p_condition_eq(p):
    """condition   : value EQ value"""
    command = standard_render(p[1], p[3], 'c', 'd', str(p.lineno(2)))
    m1, m2, m3 = spawn_frogs_multiple(3)
    p[0] = (pack(command
                 + rs_reg('e') + nl() + 'ADD e c' + nl()
                 + rs_reg('f') + nl() + 'ADD f d' + nl()
                 + "SUB e d" + nl()
                 + "SUB f c" + nl()
                 + 'JZERO e ' + frogs[m3] + nl()
                 + 'JUMP ' + frogs[m2] + nl()
                 + m3 + 'JZERO f ' + frogs[m1] + nl()
                 + 'JUMP ' + frogs[m2] + nl()
                 + m1
                 , '<<EQ'), m2)
```

## Technologies

- python
- ply
- numpy
- os
