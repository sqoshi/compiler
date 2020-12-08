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
## Launch
```shell script
python3 compiler.py in_file out_file
```
## Introduction
Compiler takes some code in language below and produces a machine code which is accepted by a virtual
machine attached in working tree( maszyna-wirtualna)
### Example of imperative language (binary notation of a number)
```python
1 DECLARE
2   n,p
3 BEGIN
4       READ n ;
5       REPEAT
6       p := n /2;
7       p :=2* p ;
8       IF n > p THEN
9           WRITE 1;
10      ELSE
11          WRITE 0;
12      ENDIF
13      n := n /2;
14  UNTIL n =0;
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
###................................................................................................................. Numbers Generator
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
while b>0:
    if b%2==0: 
        a=a*2
        b=b/2
    else:
        ab=ab*a
        b=b-1
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
##### First Attempt
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
###### Code 
```python

def p_expression_division(p):
    """expression   : value DIV value"""
    command = standard_render(p[1], p[3], 'd', 'c', str(p.lineno(2)))
    m1, m2, m3, m4, m5, m6 = spawn_frogs_multiple(6)
    p[0] = pack(command +
                rs_reg('a') + nl() +
                'JZERO c ' + frogs[m1] + nl() +
                'JZERO d ' + frogs[m1] + nl() +
                rs_reg('e') + nl() +
                rs_reg('f') + nl() +
                rs_reg('b') + nl() +
                'ADD b c' + nl() +
                m3 + rs_reg('e') + nl()  # while outer
                + 'ADD e c' + nl()
                + 'SUB e d' + nl()
                + 'JZERO e ' + frogs[m5] + nl()
                + 'JUMP ' + frogs[m1] + nl()
                + m5 + rs_reg('f') + nl()
                + 'INC f' + nl()
                + 'SHL c' + nl()
                + m4+rs_reg('e') + nl()
                + 'ADD e c' + nl()
                + 'SUB e d' + nl()
                + 'JZERO e ' + frogs[m6] + nl()
                + 'JUMP ' + frogs[m2] + nl()
                + m6 + 'SHL f' + nl()
                + 'SHL c' + nl()
                + 'JUMP ' + frogs[m4] + nl()
                + m2 + 'ADD a f' + nl()
                + rs_reg('f') + nl()
                + 'SHR c' + nl()
                + 'SUB d c' + nl()
                + 'RESET c' + nl()
                + 'ADD c b' + nl()
                + 'JUMP ' + frogs[m3] + nl()
                + m1
                                + m1, '<<div')

```
##### Second Attempt
```python
    a = 0
    while d >= c:
        e = c
        f = 1
        while d >= e :
            f *= 2
            e *= 2
        f = f / 2
        e = e / 2
        d -= e
        a += f
```
###### Code 
```python


def p_expression_division(p):
    """expression   : value DIV value"""
    command = standard_render(p[1], p[3], 'd', 'c', str(p.lineno(2)))
    m1, m2, m3, m4, m5, m6 = spawn_frogs_multiple(6)
    p[0] = pack(command +
                rs_reg('a') + nl() +
                'JZERO c ' + frogs[m1] + nl() +
                'JZERO d ' + frogs[m1] + nl() +
                m5 + rs_reg('b') + nl() +
                'ADD b d' + nl()
                + 'SUB b c' + nl()
                + 'JZERO b ' + frogs[m1] + nl()
                + rs_reg('f') + nl()
                + 'INC f' + nl()
                + rs_reg('e') + nl()
                + 'ADD e c' + nl()
                + m6 + rs_reg('b') + nl()
                + 'ADD b d' + nl()
                + 'SUB b e' + nl()
                + 'JZERO b ' + frogs[m4] + nl()
                + 'SHL e' + nl()
                + 'SHL f' + nl()
                + 'JUMP ' + frogs[m6] + nl()
                + m4 + 'SHR e' + nl()
                + 'SHR f' + nl()
                + 'SUB d e' + nl()
                + 'ADD a f' + nl()
                + 'JUMP ' + frogs[m5] + nl()
                + m1, '<<div')
```
```python
def p_expression_modulo(p):
    """expression   : value MOD value"""
    command = standard_render(p[1], p[3], 'a', 'c', str(p.lineno(2)))
    m1, m2, m3, m4, m5, m6 = spawn_frogs_multiple(6)
    p[0] = pack(command +
                rs_reg('d') + nl() +
                'JZERO c ' + frogs[m1] + nl() +
                'JZERO a ' + frogs[m1] + nl() +
                rs_reg('e') + nl() +
                rs_reg('f') + nl() +
                rs_reg('b') + nl() +
                'ADD b c' + nl() +
                m3 + rs_reg('e') + nl()  # while outer
                + 'ADD e c' + nl()
                + 'SUB e a' + nl()
                + 'JZERO e ' + frogs[m5] + nl()
                + 'JUMP ' + frogs[m1] + nl()
                + m5 + rs_reg('f') + nl()
                + 'INC f' + nl()
                + 'SHL c' + nl()
                + m4 + rs_reg('e') + nl()
                + 'ADD e c' + nl()
                + 'SUB e a' + nl()
                + 'JZERO e ' + frogs[m6] + nl()
                + 'JUMP ' + frogs[m2] + nl()
                + m6 + 'SHL f' + nl()
                + 'SHL c' + nl()
                + 'JUMP ' + frogs[m4] + nl()
                + m2 + 'ADD d f' + nl()
                + rs_reg('f') + nl()
                + 'SHR c' + nl()
                + 'SUB a c' + nl()
                + 'RESET c' + nl()
                + 'ADD c b' + nl()
                + 'JUMP ' + frogs[m3] + nl()
                + m1, '<<mod')
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
