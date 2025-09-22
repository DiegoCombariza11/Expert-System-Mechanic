from experta import KnowledgeEngine, Rule, MATCH
from engine.facts import vehicle
import json

with open('data/sintoms.json') as f:
    sintomas_data = {s["nombre"]: s["posible_fallas"] for s in json.load(f) }

class diagnose(KnowledgeEngine):
   
    def __init__(self):
        super().__init__()
        self.resultados = {}

    @Rule(vehicle(sintoma=MATCH.sintoma))
    def diagnostico(self, sintoma):
        if sintoma in sintomas_data:
            self.resultados[sintoma] = sintomas_data[sintoma]
        else:
            self.resultados[sintoma] = []

    def get_fallas(self, sintoma):
        return self.resultados.get(sintoma, [])
