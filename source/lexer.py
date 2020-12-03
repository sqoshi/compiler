import ply.lex

tokens = ('DECLARE', 'BEGIN', 'END',
          'PLUS', 'MINUS', 'DIV', 'MULT', 'MOD',
          'NUM', 'ID', 'ASSIGN',
          'EQ', 'NEQ', 'LEQ', 'GEQ', 'LT', 'GT',
          'LBR', 'RBR', 'COLON', 'SEMICOLON','COMMA',
          'READ', 'WRITE',
          'IF', 'THEN', 'ELSE', 'ENDIF',
          'WHILE', 'DO', 'ENDWHILE',
          'REPEAT', 'UNTIL',
          'FOR', 'FROM', 'TO', 'DOWNTO', 'ENDFOR',)

t_ignore_COMMENT = r'\[[^\]]*\]'
t_ignore = ' \t'

t_DECLARE = r'DECLARE'
t_BEGIN = r'BEGIN'
t_END = r'END'


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_READ = r'READ'
t_WRITE = r'WRITE'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIV = r'\/'
t_MULT = r'\*'
t_MOD = r'\%'

t_ASSIGN = r':='
t_EQ = r'='
t_NEQ = r'!='
t_LEQ = r'<='
t_GEQ = r'>='
t_LT = r'<'
t_GT = r'>'

t_LBR = r'\('
t_RBR = r'\)'
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','

t_IF = r'IF'
t_THEN = r'THEN'
t_ELSE = r'ELSE'
t_ENDIF = r'ENDIF'
t_DO = r'DO'
t_FOR = r'FOR'
t_FROM = r'FROM'
t_TO = r'TO'
t_DOWNTO = r'DOWNTO'
t_ENDFOR = r'ENDFOR'
t_WHILE = r'WHILE'
t_REPEAT = r'REPEAT'
t_UNTIL = r'UNTIL'
t_ENDWHILE = r'ENDWHILE'


def t_newline(t):
    r'\r?\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Wrong char {}".format(t.value[0]))
    t.lexer.skip(1)


t_ID = r'[_a-z]+'

lexer = ply.lex.lex()
