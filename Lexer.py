import ply.lex as lex

reserved  = {
    'si': 'SI',
    'sino': 'SINO',
    'decimal': 'TIPO_DECIMAL',
    'entero': 'TIPO_ENTERO',
    'verdadero':'VERDADERO',
    'falso':'FALSO',
    'letras': 'TIPO_CADENA_TEXTO',
    'guail': 'MIENTRAS',
    'por': 'POR',
    'es': 'IGUAL',
}

class Lexer(object):
    # List of token names.   This is always required
    tokens = [
        'VARIABLE',
        'NUMERO',
        'MAS',
        'MENOS',
        'MULTIPLICA',
        'DIVIDE',
        'PARENTESIS_I',
        'PARENTESIS_D',
        'CORCHETE_I',
        'CORCHETE_D',
        'FIN_SENTENCIA',
        'IGUAL',
        'COMENTARIO',
        'ID'
    ] + list(reserved.values())

    # Regular expression rules for simple tokens
    t_VARIABLE = r'\#'
    t_MAS    = r'\+'
    t_MENOS   = r'-'
    t_MULTIPLICA   = r'\*'
    t_DIVIDE  = r'/'
    t_PARENTESIS_I  = r'\('
    t_PARENTESIS_D = r'\)'
    t_CORCHETE_I  = r'\{'
    t_CORCHETE_D = r'\}'
    t_FIN_SENTENCIA = r'\;'
    t_ignore_COMMENT = r'\$.*'

    # A regular expression rule with some action code
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID')   # Check for reserved words
        return t
    # Note addition of self parameter since we're in a class
    def t_NUMERO(self,t):
        r'\d+'
        t.value = int(t.value)
        return t
    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    # A string containing ignored characters (spaces and tabs)
    
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             print(tok)

# Build the lexer and try it out

if __name__ == '__main__':
    m = Lexer()
    m.build()           # Build the lexer
    m.test("(3 + 4) * 5 ;$hola 5*1 \n * si (falso) hola es 1 sino;")     # Test it