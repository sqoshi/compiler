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
```jupyter
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
### Arithmetic operations ( Algorithms )
#### Numbers Generator
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

#### Division

## Code Example
#### Equality
```python
def p_condition_eq(p):
    """condition   : value EQ value"""
    command = standard_render(p[1], p[3], 'c', 'd', str(p.lineno(2)))
    m1, m2, m3 = get_marks(3)
    p[0] = (pack(command
                 + rs_reg('e') + nl() + 'ADD e c' + nl()
                 + rs_reg('f') + nl() + 'ADD f d' + nl()
                 + "SUB e d" + nl()
                 + "SUB f c" + nl()
                 + 'JZERO e ' + jump_label[m3] + nl()
                 + 'JUMP ' + jump_label[m2] + nl()
                 + m3 + 'JZERO f ' + jump_label[m1] + nl()
                 + 'JUMP ' + jump_label[m2] + nl()
                 + m1
                 , '<<EQ'), m2)
```
## Technologies
- python
- ply
- numpy
- os
