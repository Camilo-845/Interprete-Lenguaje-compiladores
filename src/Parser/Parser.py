import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from ply import yacc
from Lexer.Lexer import Lexer

class Parser:

    tokens = Lexer.tokens
    precedence = (
        ('left', 'IGUAL', 'SINO'),
        ('left', 'MAYOR', 'MENOR'),
        ('left', 'MAS', 'MENOS'),
        ('left', 'MULTIPLICA', 'DIVIDE'),
        ('right', 'UMENOS'),
    )

    def __init__(self) -> None:
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self, debug=True)
        self.variables = {}

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

    def p_statement_expr(self, p):
        'statement : expression'
        p[0] = p[1]

    def p_statement_if(self, p):
        '''statement : SI PARENTESIS_I expression PARENTESIS_D ENTONCES CORCHETE_I statement CORCHETE_D SINO CORCHETE_I statement CORCHETE_D
                     | SI PARENTESIS_I expression PARENTESIS_D ENTONCES CORCHETE_I statement CORCHETE_D'''
        if len(p) == 13:
            p[0] = ('si_sino', p[3], p[7], p[11])
        else:
            p[0] = ('si', p[2], p[4])

    def p_expression_binope(self, p):
        '''expression : expression MAS expression
                    | expression MENOS expression
                    | expression MULTIPLICA expression
                    | expression DIVIDE expression
                    | expression MENOR expression
                    | expression MAYOR expression
                    | expression IGUAL expression
                    '''
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3] 
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = float(p[1]) / float(p[3])
        elif p[2] == 'menor':
            p[0] = p[1] < p[3]
        elif p[2] == 'mayor':
            p[0] = p[1] > p[3]
        elif p[2] == 'igual':
            p[0] = p[1] == p[3]

    def p_expression_uminus(self, p):
        'expression : MENOS expression %prec UMENOS'
        p[0] = -p[2]

    def p_expression_group(self, p):
        'expression : PARENTESIS_I expression PARENTESIS_D'
        p[0] = p[2]

    def p_expression_numero(self, p):
        'expression : NUMERO'
        p[0] = p[1]

    def p_expression_varible(self, p):
        'expression : VARIABLE ID'
        if p[2] not in self.variables:
            print(f"Undefined variable => {p[2]}")
        else:
            p[0] = self.variables[p[2]]

    def p_assignment(self, p):
        'factor : VARIABLE ID ASIGNACION expression'
        self.variables[p[2]] = p[4]
        p[0] = p[4]

    def p_factor_boolean(self,p):
        '''expression : VERDADERO
                      | FALSO'''
        p[0] = p[1]

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]



if __name__ == '__main__':
    parser = Parser()
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(Lexer().test(s))
        print(result)
