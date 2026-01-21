import tkinter as tk
from tkinter import messagebox

class CalculadoraAvanzada(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora basica ZerxStar v2.0")
        self.geometry("600x500")
        self.configure(padx=10, pady=10)

        # Temas 
        self.temas = {
            "Oscuro": {"bg": "#1e1e1e", "btn": "#333333", "txt": "#ffffff", "accent": "#d400b4", "hist": "#2d2d2d"},
            "Claro": {"bg": "#f3f3f3", "btn": "#ffffff", "txt": "#000000", "accent": "#0067b8", "hist": "#e1e1e1"}
        }
        self.tema_actual = "Oscuro"
        self.historial_lista = []

        self.setup_ui()

    def setup_ui(self):
        t = self.temas[self.tema_actual]
        self.configure(bg=t["bg"])

        # --- (Layout Horizontal) ---
        self.main_container = tk.Frame(self, bg=t["bg"])
        self.main_container.pack(fill="both", expand=True)

        # --- Calculadora ---
        self.calc_frame = tk.Frame(self.main_container, bg=t["bg"])
        self.calc_frame.pack(side="left", fill="both", expand=True, padx=5)

        self.pantalla = tk.Entry(self.calc_frame, font=("Segoe UI", 32), borderwidth=0, 
                                 bg=t["bg"], fg=t["txt"], justify="right")
        self.pantalla.pack(fill="x", pady=(20, 10))

        self.btn_container = tk.Frame(self.calc_frame, bg=t["bg"])
        self.btn_container.pack(fill="both", expand=True)

        # --- Lado Derecho: Historial ---
        self.hist_frame = tk.Frame(self.main_container, bg=t["hist"], width=200)
        self.hist_frame.pack(side="right", fill="both", padx=5)
        
        tk.Label(self.hist_frame, text="Historial", font=("Segoe UI", 12, "bold"), 
                 bg=t["hist"], fg=t["txt"]).pack(pady=10)
        
        self.hist_box = tk.Listbox(self.hist_frame, bg=t["hist"], fg=t["txt"], 
                                   borderwidth=0, font=("Segoe UI", 10))
        self.hist_box.pack(fill="both", expand=True, padx=5, pady=5)

        self.crear_botones()
        self.crear_menu()

    def crear_botones(self):
        for widget in self.btn_container.winfo_children():
            widget.destroy()

        botones = [
            ['C', '(', ')', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['.', '0', 'DEL', '=']
        ]

        t = self.temas[self.tema_actual]
        for r, fila in enumerate(botones):
            for c, texto in enumerate(fila):
                color = t["accent"] if texto == '=' else t["btn"]
                btn = tk.Button(self.btn_container, text=texto, font=("Segoe UI", 11),
                                bg=color, fg="white" if texto == '=' else t["txt"],
                                borderwidth=0, cursor="hand2",
                                command=lambda x=texto: self.click(x))
                btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        for i in range(4): self.btn_container.grid_columnconfigure(i, weight=1)
        for i in range(5): self.btn_container.grid_rowconfigure(i, weight=1)

    def click(self, tecla):
        if tecla == '=':
            try:
                expr = self.pantalla.get()
                res = eval(expr)
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(tk.END, str(res))
                # Guardar en historial
                item = f"{expr} = {res}"
                self.hist_box.insert(0, item)
            except:
                messagebox.showerror("Error", "Operación inválida")
        elif tecla == 'C':
            self.pantalla.delete(0, tk.END)
        elif tecla == 'DEL':
            actual = self.pantalla.get()
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(tk.END, actual[:-1])
        else:
            self.pantalla.insert(tk.END, tecla)

    def crear_menu(self):
        menu_bar = tk.Menu(self)
        tema_menu = tk.Menu(menu_bar, tearoff=0)
        tema_menu.add_command(label="Modo Oscuro", command=lambda: self.cambiar_tema("Oscuro"))
        tema_menu.add_command(label="Modo Claro", command=lambda: self.cambiar_tema("Claro"))
        menu_bar.add_cascade(label="Opciones", menu=tema_menu)
        menu_bar.add_command(label="Limpiar Historial", command=lambda: self.hist_box.delete(0, tk.END))
        self.config(menu=menu_bar)

    def cambiar_tema(self, nombre):
        self.tema_actual = nombre
        # Reiniciar UI para aplicar colores
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()

if __name__ == "__main__":
    app = CalculadoraAvanzada()
    app.mainloop()