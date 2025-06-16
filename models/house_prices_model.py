import os
import pickle

class House:
    def __init__(self, tamanho, ano, garagem):
        self.tamanho = tamanho
        self.ano = ano 
        self.garagem = garagem

class Model:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        model_path = os.path.join(base_dir, 'modelo.sav')
        self.modelo = pickle.load(open(model_path, 'rb'))

    def predict(self, size, year, garage):
        try:
            preco = self.modelo.predict([[float(size), float(year), float(garage)]])[0].round(2)
        except Exception as e:
            print(f"Erro na previsão: {e}")
            raise
        return preco
