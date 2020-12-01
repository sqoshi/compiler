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


## Code Example
```python
def p_expression_value(p):
    '''expression   : value'''
    p[0] = load_value(p[1], "a", str(p.line(1)))
```
## Technologies
- Pyton 3.9
- ply
