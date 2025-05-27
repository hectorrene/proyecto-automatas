class AnalizadorLexico:
    def __init__(self, entrada):
        self.entrada = entrada
        self.tokens = []
        self.lexico = []
        self.operadores_validos = ['+', '-', '*', '/', '=']
        self.operadores_invalidos = ['**', '==', '!=', '<=', '>=']
        self.parentesis = ['(', ')']

    def es_letra(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z')

    def es_digito(self, c):
        return '0' <= c <= '9'

    def es_alfa_num(self, c):
        return self.es_letra(c) or self.es_digito(c)

    def analizar(self):
        i = 0
        while i < len(self.entrada):
            c = self.entrada[i]

            if c == ' ':
                i += 1
                continue

            # Operadores inválidos
            if i + 1 < len(self.entrada):
                par = c + self.entrada[i + 1]
                if par in self.operadores_invalidos:
                    print("Operador inválido:", par)
                    self.lexico = ['Vuelva a empezar']
                    return self.lexico

            # Paréntesis
            if c in self.parentesis:
                self.tokens.append(c)
                i += 1
                continue

            # Identificador
            if self.es_letra(c):
                ident = ''
                while i < len(self.entrada) and self.es_alfa_num(self.entrada[i]):
                    ident += self.entrada[i]
                    i += 1
                self.tokens.append(ident)
                continue

            # Número con signo
            if c in '+-' and i + 1 < len(self.entrada) and self.es_digito(self.entrada[i + 1]):
                if len(self.tokens) == 0 or self.tokens[-1] in ['=', '(']:
                    num = c
                    i += 1
                    while i < len(self.entrada) and self.es_digito(self.entrada[i]):
                        num += self.entrada[i]
                        i += 1
                    self.tokens.append(num)
                    continue
                else:
                    self.tokens.append(c)
                    i += 1
                    continue

            # Número sin signo
            if self.es_digito(c):
                num = ''
                while i < len(self.entrada) and self.es_digito(self.entrada[i]):
                    num += self.entrada[i]
                    i += 1
                self.tokens.append(num)
                continue

            # Operador válido
            if c in self.operadores_validos:
                self.tokens.append(c)
                i += 1
                continue

            # Carácter inválido
            print("Caracter inválido:", c)
            self.lexico = ['Vuelva a empezar']
            return self.lexico

        # Clasificación de tokens
        for t in self.tokens:
            if t in self.operadores_invalidos:
                print("Operador inválido:", t)
                self.lexico = ['Vuelva a empezar']
                break
            elif t in self.operadores_validos:
                self.lexico.append(t)
            elif t in self.parentesis:
                self.lexico.append(t)
            elif self.es_letra(t[0]):
                es_id = True
                for c in t:
                    if not self.es_alfa_num(c):
                        es_id = False
                        break
                if es_id:
                    self.lexico.append('id')
                else:
                    print("Identificador inválido:", t)
                    self.lexico = ['Vuelva a empezar']
                    break
            elif (t[0] in '+-' and len(t) > 1 and all(self.es_digito(c) for c in t[1:])) or all(self.es_digito(c) for c in t):
                self.lexico.append('num')
            else:
                print("Token no reconocido:", t)
                self.lexico = ['Vuelva a empezar']
                break

        return self.lexico


class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens

    def analizar(self):
        if 'Vuelva a empezar' in self.tokens:
            print("Vuelva a empezar")
            return False

        if self.tokens.count('(') != self.tokens.count(')'):
            print("Hay un desbalance de paréntesis.")
            print("Vuelva a empezar")
            return False

        if len(self.tokens) < 3 or self.tokens[0] != 'id' or self.tokens[1] != '=':
            print("Orden incorrecto de tokens")
            print("Vuelva a empezar")
            return False

        for i in range(1, len(self.tokens)):
            actual = self.tokens[i]
            anterior = self.tokens[i - 1]

            if actual in ['+', '-', '*', '/'] and anterior in ['+', '-', '*', '/']:
                print("No se puede tener dos operadores lógicos juntos.")
                print("Vuelva a empezar")
                return False

            if actual == '(' and anterior == 'num':
                print("No puede ir un '(' después de un número.")
                print("Vuelva a empezar")
                return False

            if actual == 'num' and anterior == ')':
                print("No puede ir un número después de ')'.")
                print("Vuelva a empezar")
                return False

            if actual == '+' and anterior == '=':
                print("Un '+' debe estar después de un número o id.")
                print("Vuelva a empezar")
                return False

        return True


# Programa principal
entrada = input("Escribe una expresión: ")

lexico = AnalizadorLexico(entrada)
tokens = lexico.analizar()

sintactico = AnalizadorSintactico(tokens)
if sintactico.analizar():
    for token in tokens:
        print(token, end=' ')
    print("\nExpresión válida")
