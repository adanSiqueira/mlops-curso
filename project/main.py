import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from googletrans import Translator
from models.house_prices_model import Model 

load_dotenv()
modelo = Model()

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = os.getenv('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('BASIC_AUTH_PASSWORD')
basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return "Minha primeira API."

@app.route('/sentimento/<frase>')
async def translator(frase):
    translator = Translator()
    frase_en = await translator.translate(frase, dest='en')
    texto = frase_en.text
    polaridade = TextBlob(texto).sentiment.polarity
    return f'Polaridade: {polaridade}'

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    params = request.get_json()
    
    # Espera que o JSON tenha as chaves: tamanho, ano, garagem
    try:
        size = params['tamanho']
        year = params['ano']
        garage = params['garagem']
    except KeyError as e:
        return {'erro': f'Parâmetro ausente: {str(e)}'}, 400

    price = modelo.predict(size, year, garage)
    
    preco_formatado = f"{price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return jsonify({'preco_estimado': f'O Preço estimado do imóvel é {preco_formatado} $'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)