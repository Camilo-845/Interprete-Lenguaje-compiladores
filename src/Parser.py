from ply import yacc
from Lexer import Lexer

class Parser:
    tokens = Lexer.tokens
    
    def __init__(self) -> None:
        self.lexer = Lexer()
        self.parser = yacc.yacc(module = self)

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

    def p_expression_plus(self, p):
        '''expression : term MAS term
                    | term MENOS term'''
        if p[2] == '+':
            p[0] = p[1] + p[3]
        else:
            p[0] = p[1] - p[3]

    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_term_times(self, p):
        '''term : factor MULTIPLICA factor
                | factor DIVIDE factor'''
        if p[2] == '*':
            p[0] = p[1] * p[3]
        else:
            p[0] = p[1] / p[3]

    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]

    def p_factor_number(self, p):
        'factor : NUMERO'
        p[0] = p[1]


    def p_error(self, p):
        print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

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
        print(result)
