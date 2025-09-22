import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
from engine.rules import Diagnose
from engine.facts import Sintoma

class SistemaGUI:
    def __init__(self):
        # Cargar síntomas y fallas desde JSON
        with open("data/sintoms.json", "r", encoding="utf-8") as f:
            self.sintomas_data = json.load(f)

        # Configuración de la ventana
        self.root = tk.Tk()
        self.root.title("Sistema de Diagnóstico Vehicular")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f2f2f2")

        tk.Label(
            self.root,
            text="Sistema de Diagnóstico Vehicular",
            font=("Arial", 18, "bold"),
            bg="#f2f2f2",
            fg="#333333"
        ).pack(pady=15)

        # Motor experto
        self.engine = Diagnose()
        self.engine.reset()

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f2f2f2")
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # =========================
        # Izquierda: síntomas
        # =========================
        self.frame_sintomas = tk.Frame(main_frame, bg="#e6f7ff", bd=2, relief="groove")
        self.frame_sintomas.pack(side="left", fill="both", expand=True, padx=(0,10))

        tk.Label(
            self.frame_sintomas,
            text="Seleccione los síntomas:",
            font=("Arial", 14, "bold"),
            bg="#e6f7ff"
        ).pack(pady=10)

        # Scroll para síntomas
        canvas = tk.Canvas(self.frame_sintomas, bg="#e6f7ff", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_sintomas, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#e6f7ff")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Variables de checkboxes
        self.checkbox_vars = {}

        for categoria, sintomas in self.sintomas_data.items():
            cat_frame = tk.LabelFrame(
                scrollable_frame,
                text=categoria,
                padx=10, pady=10,
                bg="#e6f7ff", fg="#0059b3",
                font=("Arial", 12, "bold")
            )
            cat_frame.pack(fill="x", padx=10, pady=5)

            for sintoma, info in sintomas.items():
                var = tk.BooleanVar()
                nivel = info.get("nivel", "leve") if isinstance(info, dict) else "leve"
                color_texto = "#b30000" if nivel == "critico" else "#004d00"
                cb = tk.Checkbutton(
                    cat_frame,
                    text=sintoma,
                    variable=var,
                    anchor="w",
                    justify="left",
                    bg="#e6f7ff",
                    fg=color_texto,
                    font=("Arial", 10, "bold" if nivel=="critico" else "normal")
                )
                cb.pack(anchor="w")
                self.checkbox_vars[sintoma] = var

        tk.Button(
            self.frame_sintomas,
            text="Diagnosticar",
            command=self.diagnosticar,
            bg="#3399ff", fg="white",
            font=("Arial", 12, "bold"),
            padx=10, pady=5
        ).pack(pady=15)

        # =========================
        # Derecha: resultados y alertas
        # =========================
        self.frame_resultados = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="sunken")
        self.frame_resultados.pack(side="right", fill="both", expand=True)

        tk.Label(
            self.frame_resultados,
            text="Alertas Críticas",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#b30000"
        ).pack(pady=5)

        self.alerta_text = tk.Text(
            self.frame_resultados,
            height=4,
            font=("Arial", 12, "bold"),
            bg="#ffe6e6",
            fg="#b30000"
        )
        self.alerta_text.pack(fill="x", padx=5, pady=5)

        tk.Label(
            self.frame_resultados,
            text="Resultados del diagnóstico",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=5)

        self.resultado_text = scrolledtext.ScrolledText(
            self.frame_resultados,
            wrap="word",
            font=("Arial", 11)
        )
        self.resultado_text.pack(fill="both", expand=True, padx=5, pady=5)

        self.root.mainloop()

    def diagnosticar(self):
        # Limpiar resultados anteriores
        self.resultado_text.delete('1.0', tk.END)
        self.alerta_text.delete('1.0', tk.END)

        # Obtener síntomas seleccionados
        sintomas_seleccionados = [s for s, var in self.checkbox_vars.items() if var.get()]
        if not sintomas_seleccionados:
            messagebox.showwarning("Aviso", "Seleccione al menos un síntoma.")
            return

        # Reiniciar motor experto
        self.engine.reset()
        self.engine.fallas_detectadas = {}

        # Declarar síntomas correctamente
        for sintoma in sintomas_seleccionados:
            self.engine.declare(Sintoma(nombre=sintoma))

        # Ejecutar motor experto
        self.engine.run()

        # Mostrar resultados
        fallas_ordenadas = self.engine.get_fallas_ordenadas()
        if not fallas_ordenadas:
            self.resultado_text.insert(tk.END, "No se encontraron fallas.\n")
            return

        # Primera falla → alerta crítica
        falla_critica = fallas_ordenadas[0][0]
        self.alerta_text.insert(tk.END, f"⚠ {falla_critica}\n")

        # Mostrar todas las fallas ordenadas por prioridad
        for falla, peso in fallas_ordenadas:
            self.resultado_text.insert(tk.END, f"→ {falla} (prioridad: {peso})\n")

# Ejecutar la interfaz
if __name__ == "__main__":
    SistemaGUI()
