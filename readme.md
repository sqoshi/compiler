# Compiler

## Table of contents

* [Installation](#installation)
* [Launch](#launch)
* [Introduction](#Introduction)
* [General info](#general-info)
* [Warnings](#warnings)
* [Code Example](#code-example)
* [Technologies](#technologies)

## Installation
Installation can be carried out automatically with alternatively:
```shell
make
```


or

```shell script
bash install.sh
```


If script and make would fail than installation need to be done manually:
```shell
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo pip3 install -r requirements.txt
```
If `pip3 install -r requirements.txt` fails than also packages below need to be installed 
manually:
```shell
sudo pip install termcolor==1.1.0
sudo pip install numpy==1.19.5
sudo pip install ply==3.11
```
## Launch

```shell script
python3 kompilator.py in_file out_file
```

## Introduction

Compiler takes some code in Pascal- like imperative language
 defined by grammar in general info section and produces 
a machine code which is accepted by a
virtual machine attached in working tree( maszyna-wirtualna).

### Example of imperative language (binary notation of a number)
```python
1 DECLARE
2   n,p
3 BEGIN
4       READ n ;
5       REPEAT
6       p := n / 2;
7       p := 2 * p ;
8       IF n > p THEN
9           WRITE 1;
10      ELSE
11          WRITE 0;
12      ENDIF
13      n := n / 2;
14  UNTIL n != 0;
15 END
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

### Language Grammar

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
- When number is odd perform inc ( increase by 1 )

Reduce number in each iteration ( respectively /2 , -1). 
Reversed output of this loop is a generated number in given register.

### Arithmetic operations
#### Multiplication

We are checking parity of value in register b. 
It is worth to keep smaller number in reduced register.(10^3 time save.)

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

As we can see in example below same 
algorithm can be used to find result of mod and integer unsigned division.

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
## Warnings
Warnings can be turned on with flag --warnings as third argument. User can face some 
yellow warnings which main response is to inform about that when we refer to array cell using variable
( for example arr(0:15);a:=123; arr(a) ) than on python side we can not check if arr(a) is 'outside the array', because 
python does not know what virtual machine hold under memory address of  variable 'a'.


## Code Example

#### Equality

```python
def p_condition_eq(p):
    """condition   : value EQ value"""
    v1 = get_value(p[1], 'c', p.lineno(1), 'd')
    v2 = get_value(p[3], 'd', p.lineno(3), 'b')
    m1, m2, m3 = spawn_frogs_multiple(3)
    p[0] = (pack(v1 + v2 +
                 cmd('reset', 'e') +
                 cmd('add', 'e', 'c') +
                 cmd('reset', 'f') +
                 cmd('add', 'f', 'd') +
                 cmd('sub', 'e', 'd') +
                 cmd('sub', 'f', 'c') +
                 cmd('jzero', 'e', frogs[m3]) +
                 cmd('jump', frogs[m2]) +
                 m3 + cmd('jzero', 'f', frogs[m1]) +
                 cmd('jump', frogs[m2]) +
                 m1,
                 '<<eq>>'), m2)

```

## Technologies

- python
- ply
- termcolor
- numpy