from experta import KnowledgeEngine, Rule, MATCH
from engine.facts import Sintoma, Falla
import json

def cargar_base_conocimiento(ruta="data/sintoms.json"):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

class Diagnose(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.base = cargar_base_conocimiento()
        self.fallas_detectadas = {}

    # -------------------------
    # Regla genérica: cualquier síntoma genera fallas según JSON
    # -------------------------
    @Rule(Sintoma(nombre=MATCH.s))
    def regla_generica(self, s):
        for categoria, sintomas in self.base.items():
            if s in sintomas:
                for falla in sintomas[s].get("fallas", []):
                    self.fallas_detectadas[falla] = self.fallas_detectadas.get(falla, 0) + 1
                    self.declare(Falla(nombre=falla))

    # -------------------------
    # Reglas complejas y combinaciones coherentes
    # -------------------------
    @Rule(Sintoma(nombre="Motor no arranca") & Sintoma(nombre="Luces tenues") & Sintoma(nombre="Indicador de batería parpadea"))
    def bateria_total(self):
        self.fallas_detectadas["Batería completamente descargada"] = self.fallas_detectadas.get("Batería completamente descargada", 0) + 5
        self.declare(Falla(nombre="Batería completamente descargada"))

    @Rule(Sintoma(nombre="Motor no arranca") & Sintoma(nombre="Arranque ruidoso"))
    def motor_arranque(self):
        self.fallas_detectadas["Motor de arranque desgastado"] = self.fallas_detectadas.get("Motor de arranque desgastado", 0) + 4
        self.declare(Falla(nombre="Motor de arranque desgastado"))

    @Rule(Sintoma(nombre="Humo excesivo") & Sintoma(nombre="Testigo de temperatura") & Sintoma(nombre="Testigo de aceite"))
    def recalentamiento_motor(self):
        self.fallas_detectadas["Recalentamiento severo del motor"] = self.fallas_detectadas.get("Recalentamiento severo del motor", 0) + 5
        self.declare(Falla(nombre="Recalentamiento severo del motor"))

    @Rule(Sintoma(nombre="Frenos flojos") & Sintoma(nombre="Dirección dura") & Sintoma(nombre="Vibraciones fuertes"))
    def problemas_frenos_suspension(self):
        self.fallas_detectadas["Problemas combinados: frenos y suspensión"] = self.fallas_detectadas.get("Problemas combinados: frenos y suspensión", 0) + 4
        self.declare(Falla(nombre="Problemas combinados: frenos y suspensión"))

    # -------------------------
    # Encadenamiento lógico
    # -------------------------
    @Rule(Falla(nombre="Batería completamente descargada") & Sintoma(nombre="Motor no arranca"))
    def falla_secundaria_arranque(self):
        self.fallas_detectadas["Problema en sistema de arranque"] = self.fallas_detectadas.get("Problema en sistema de arranque", 0) + 3
        self.declare(Falla(nombre="Problema en sistema de arranque"))

    @Rule(Falla(nombre="Recalentamiento severo del motor") & Sintoma(nombre="Frenos flojos"))
    def riesgo_motor_frenos(self):
        self.fallas_detectadas["Riesgo de daño severo al motor y frenos"] = self.fallas_detectadas.get("Riesgo de daño severo al motor y frenos", 0) + 4
        self.declare(Falla(nombre="Riesgo de daño severo al motor y frenos"))

    @Rule(Falla(nombre="Fallo motor electrónico") & Sintoma(nombre="Humo excesivo"))
    def detener_inmediatamente(self):
        self.fallas_detectadas["Recomendación: detener vehículo inmediatamente"] = self.fallas_detectadas.get("Recomendación: detener vehículo inmediatamente", 0) + 5

    # -------------------------
    # Obtener fallas ordenadas por prioridad
    # -------------------------
    def get_fallas_ordenadas(self):
        return sorted(self.fallas_detectadas.items(), key=lambda x: x[1], reverse=True)
