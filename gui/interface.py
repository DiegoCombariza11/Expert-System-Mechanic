import tkinter as tk
from tkinter import messagebox, scrolledtext
import json

class SistemaGUI:
    def __init__(self):
        # Cargar síntomas y fallas desde JSON
        with open("data/sintoms.json", "r", encoding="utf-8") as f:
            self.sintomas_data = json.load(f)

        # Configuración principal de la ventana
        self.root = tk.Tk()
        self.root.title("Diagnóstico de Vehículos")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f2f2f2")

        # Título principal
        tk.Label(self.root, text="Sistema de Diagnóstico Vehicular", font=("Arial", 18, "bold"), bg="#f2f2f2", fg="#333333").pack(pady=15)

        # Frame principal dividido en dos columnas
        main_frame = tk.Frame(self.root, bg="#f2f2f2")
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # =========================
        # Frame izquierdo: síntomas
        # =========================
        self.frame_sintomas = tk.Frame(main_frame, bg="#e6f7ff", bd=2, relief="groove")
        self.frame_sintomas.pack(side="left", fill="both", expand=True, padx=(0,10))

        tk.Label(self.frame_sintomas, text="Seleccione los síntomas del vehículo:", font=("Arial", 14, "bold"), bg="#e6f7ff").pack(pady=10)

        # Scroll interno para checkboxes
        canvas = tk.Canvas(self.frame_sintomas, bg="#e6f7ff", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_sintomas, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#e6f7ff")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Diccionario de variables de checkboxes
        self.checkbox_vars = {}

        # Separar síntomas críticos y leves
        for categoria, sintomas in self.sintomas_data.items():
            cat_frame = tk.LabelFrame(scrollable_frame, text=categoria, padx=10, pady=10, bg="#e6f7ff", fg="#0059b3", font=("Arial", 12, "bold"))
            cat_frame.pack(fill="x", padx=10, pady=5)
            for sintoma, info in sintomas.items():
                var = tk.BooleanVar()
                # info puede ser dict con "nivel": "critico" o "leve"
                nivel = info.get("nivel", "leve") if isinstance(info, dict) else "leve"
                color_texto = "#b30000" if nivel == "critico" else "#004d00"
                cb = tk.Checkbutton(cat_frame, text=sintoma, variable=var, anchor="w", justify="left", bg="#e6f7ff", fg=color_texto, font=("Arial", 10, "bold" if nivel=="critico" else "normal"))
                cb.pack(anchor="w")
                self.checkbox_vars[sintoma] = var

        # Botón diagnosticar
        tk.Button(self.frame_sintomas, text="Diagnosticar", command=self.diagnosticar, bg="#3399ff", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).pack(pady=15)

        # =========================
        # Frame derecho: resultados
        # =========================
        self.frame_resultados = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="sunken")
        self.frame_resultados.pack(side="right", fill="both", expand=True)

        tk.Label(self.frame_resultados, text="Resultados del diagnóstico", font=("Arial", 14, "bold"), bg="#ffffff", fg="#333333").pack(pady=10)

        self.resultado_text = scrolledtext.ScrolledText(self.frame_resultados, wrap="word", font=("Arial", 11))
        self.resultado_text.pack(fill="both", expand=True, padx=5, pady=5)

        self.root.mainloop()

    def diagnosticar(self):
        # Limpiar resultados anteriores
        self.resultado_text.delete('1.0', tk.END)

        # Obtener síntomas seleccionados
        sintomas_seleccionados = [s for s, var in self.checkbox_vars.items() if var.get()]

        if not sintomas_seleccionados:
            messagebox.showwarning("Aviso", "Seleccione al menos un síntoma.")
            return

        # Buscar fallas asociadas a los síntomas seleccionados
        fallas_detectadas = []
        for categoria, sintomas in self.sintomas_data.items():
            for sintoma, info in sintomas.items():
                fallas = info.get("fallas", []) if isinstance(info, dict) else info
                if sintoma in sintomas_seleccionados:
                    fallas_detectadas.extend(fallas)
                    self.resultado_text.insert(tk.END, f"✓ Síntoma: {sintoma}\n")
                    for falla in fallas:
                        self.resultado_text.insert(tk.END, f"   → Posible falla: {falla}\n")
                    self.resultado_text.insert(tk.END, "\n")

        # Resumen único
        fallas_unicas = set(fallas_detectadas)
        self.resultado_text.insert(tk.END, "\nResumen de posibles fallas:\n")
        for falla in fallas_unicas:
            self.resultado_text.insert(tk.END, f"- {falla}\n")
