from flask import Flask, jsonify, request
import json
from scrapingMeli import productos

app = Flask(__name__)

@app.route('/mercadoLibre', methods=["GET"])
def mercadoLibre():
    data = json.loads(request.data)
    titulos, urls, precios = productos(data["producto"])
    return jsonify({"datos":{"titulos":titulos, "urls":urls, "precios":precios}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)