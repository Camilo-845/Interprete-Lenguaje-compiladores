from flask import Flask, request, jsonify, abort
from Lexer import Lexer
import json

app = Flask(__name__)


@app.route('/lexer', methods=['Post'])
def tokenizar():
  try:
    assert request.json.get("data")
    data = request.json['data']
    lex = Lexer()
    lex.build()
    result = json.dumps({"result ": [str(ob) for ob in lex.tokenizar(data)]})
    print(result)
    return result
  except AssertionError:
    abort(400,description = "No se proporciono el valor data")
  except:
     abort(500, description = "Error interno")


if __name__ == "__main__":
    app.run(debug=True)