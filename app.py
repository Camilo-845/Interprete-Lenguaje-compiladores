import sys
import os

# Agregar 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Importaciones necesarias
from flask import Flask, request, jsonify, abort
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
import json

app = Flask(__name__)

lex1 = Lexer()

@app.route('/lexer', methods=['POST'])
def tokenizar():
    try:
        assert request.json.get("data")
        data = request.json['data']
        lex = Lexer()
        result = json.dumps({"result": [str(ob) for ob in lex.tokenizar(data)]})
        print(result)
        return result
    except AssertionError:
        abort(400, description="No se proporciono el valor data")
    except:
     abort(500, description = "Error interno")

@app.route('/parser', methods=['POST'])
def interpretar():
    try:
        assert request.json.get("data")
        data = request.json['data']
        parser = Parser()
        result = json.dumps({"result": str(parser.parse(data))})
        print(result)
        return result
    except AssertionError:
        abort(400, description="No se proporciono el valor data")
    except:
     abort(500, description = "Error interno")

if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)
    app.run(port=port, debug=False)
