import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

IMPRESSORAS = {
    "Bambu Lab A1 (150W)": 150,
    "Bambu Lab A1 Mini (80W)": 80,
    "Bambu Lab P1S (350W)": 350,
    "Ender 3 V2 (350W)": 350,
    "Prusa MK4 (300W)": 300,
    "Outra (Manual)": 0
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("S.Y.S.T.E.M. - Business & Cost Dashboard")
        self.geometry("1100x800") 

        self.label_titulo = ctk.CTkLabel(self, text="GESTÃO DE CUSTOS E PRECIFICAÇÃO", 
                                         font=("Orbitron", 26, "bold"), text_color="#00d4ff")
        self.label_titulo.pack(pady=20)

        self.master_container = ctk.CTkFrame(self, fg_color="transparent")
        self.master_container.pack(expand=True, anchor="center", padx=20)

        # --- COLUNA ESQUERDA: INPUTS ---
        self.frame_esquerda = ctk.CTkFrame(self.master_container, fg_color="transparent")
        self.frame_esquerda.pack(side="left", padx=(0, 50))

        # SEÇÃO 1: PRODUÇÃO ATUAL
        self.label_sec1 = ctk.CTkLabel(self.frame_esquerda, text="[ PRODUÇÃO ATUAL ]", font=("Orbitron", 13), text_color="#00d4ff")
        self.label_sec1.pack(anchor="w", pady=(0, 5))

        self.criar_legenda(self.frame_esquerda, "PESO DO MATERIAL (gramas)")
        self.entry_peso = ctk.CTkEntry(self.frame_esquerda, width=320, height=30)
        self.entry_peso.pack(pady=(0, 8), anchor="w")

        self.criar_legenda(self.frame_esquerda, "TEMPO ESTIMADO (Horas)")
        self.entry_tempo = ctk.CTkEntry(self.frame_esquerda, width=320, height=30)
        self.entry_tempo.pack(pady=(0, 8), anchor="w")

        self.criar_legenda(self.frame_esquerda, "MÃO DE OBRA (€ TOTAL)")
        self.entry_mao_obra = ctk.CTkEntry(self.frame_esquerda, width=320, height=30)
        self.entry_mao_obra.insert(0, "0.00")
        self.entry_mao_obra.pack(pady=(0, 8), anchor="w")

        self.criar_legenda(self.frame_esquerda, "PREÇO DE VENDA DESEJADO (€)")
        self.entry_venda = ctk.CTkEntry(self.frame_esquerda, width=320, height=30, border_color="#00ff00")
        self.entry_venda.pack(pady=(0, 8), anchor="w")

        ctk.CTkFrame(self.frame_esquerda, height=2, width=320, fg_color="#333333").pack(pady=10, anchor="w")

        # SEÇÃO 2: CUSTOS FIXOS
        self.label_sec2 = ctk.CTkLabel(self.frame_esquerda, text="[ CUSTOS FIXOS E BASE ]", font=("Orbitron", 13), text_color="#00d4ff")
        self.label_sec2.pack(anchor="w", pady=(0, 5))

        self.criar_legenda(self.frame_esquerda, "MODELO DA MÁQUINA")
        self.combo_maq = ctk.CTkComboBox(self.frame_esquerda, values=list(IMPRESSORAS.keys()), width=320, height=30)
        self.combo_maq.set("Bambu Lab A1 (150W)")
        self.combo_maq.pack(pady=(0, 8), anchor="w")

        self.criar_legenda(self.frame_esquerda, "PREÇO DO FILAMENTO (€/KG)")
        self.entry_preco_kg = ctk.CTkEntry(self.frame_esquerda, width=320, height=30)
        self.entry_preco_kg.insert(0, "15")
        self.entry_preco_kg.pack(pady=(0, 8), anchor="w")

        self.criar_legenda(self.frame_esquerda, "CUSTO ENERGIA kWh (€)")
        self.entry_kwh = ctk.CTkEntry(self.frame_esquerda, width=320, height=30)
        self.entry_kwh.insert(0, "0.15")
        self.entry_kwh.pack(pady=(0, 8), anchor="w")

        self.criar_legenda(self.frame_esquerda, "EMBALAGEM / EXTRAS (€)")
        self.entry_extra = ctk.CTkEntry(self.frame_esquerda, width=320, height=30)
        self.entry_extra.insert(0, "0.00")
        self.entry_extra.pack(pady=(0, 8), anchor="w")

        # --- BOTÃO CORRIGIDO E VISÍVEL ---
        self.btn_calc = ctk.CTkButton(self.frame_esquerda, text="EXECUTAR CÁLCULO", 
                                      font=("Roboto", 14, "bold"), height=45, width=320,
                                      fg_color="#005f73", hover_color="#00d4ff",
                                      command=self.calcular)
        self.btn_calc.pack(pady=15, anchor="w")

        # --- BARRA VERTICAL ---
        self.divisor = ctk.CTkFrame(self.master_container, width=2, height=600, fg_color="#00d4ff")
        self.divisor.pack(side="left")

        # --- COLUNA DIREITA: RESULTADOS ---
        self.frame_direita = ctk.CTkFrame(self.master_container, fg_color="transparent")
        self.frame_direita.pack(side="left", padx=(50, 0))

        self.label_status = ctk.CTkLabel(self.frame_direita, text="STATUS: SISTEMA OPERACIONAL", 
                                         font=("Courier New", 12), text_color="#aaaaaa")
        self.label_status.pack(anchor="w")

        self.label_resultado = ctk.CTkLabel(self.frame_direita, 
                                            text="Material:    € 0.00\nEnergia:     € 0.00\nDesgaste:    € 0.00\nMão de Obra: € 0.00\nExtras:      € 0.00\n------------------\nCUSTO TOTAL: € 0.00", 
                                            font=("Courier New", 18), text_color="white", justify="left")
        self.label_resultado.pack(pady=20, anchor="w")

        self.label_lucro = ctk.CTkLabel(self.frame_direita, 
                                        text="LUCRO: € 0.00\nMARGEM: 0%", 
                                        font=("Courier New", 26, "bold"), text_color="#00ff00", justify="left")
        self.label_lucro.pack(pady=10, anchor="w")

    def criar_legenda(self, container, texto):
        label = ctk.CTkLabel(container, text=texto, font=("Arial", 10, "bold"), text_color="white")
        label.pack(anchor="w", pady=(0, 1))

    def calcular(self):
        try:
            peso = float(self.entry_peso.get().replace(',', '.'))
            tempo = float(self.entry_tempo.get().replace(',', '.'))
            mao_obra = float(self.entry_mao_obra.get().replace(',', '.'))
            venda = float(self.entry_venda.get().replace(',', '.'))
            preco_kg = float(self.entry_preco_kg.get().replace(',', '.'))
            kwh_preco = float(self.entry_kwh.get().replace(',', '.'))
            extras = float(self.entry_extra.get().replace(',', '.'))
            
            potencia = IMPRESSORAS[self.combo_maq.get()]
            
            c_mat = (preco_kg / 1000) * peso
            c_ene = (potencia / 1000) * tempo * kwh_preco
            c_desgaste = tempo * 0.05
            
            custo_total = c_mat + c_ene + c_desgaste + extras + mao_obra
            lucro_abs = venda - custo_total
            margem = (lucro_abs / venda) * 100 if venda > 0 else 0
            
            res = (f"Material:    € {c_mat:.2f}\n"
                   f"Energia:     € {c_ene:.2f}\n"
                   f"Desgaste:    € {c_desgaste:.2f}\n"
                   f"Mão de Obra: € {mao_obra:.2f}\n"
                   f"Extras:      € {extras:.2f}\n"
                   f"------------------\n"
                   f"CUSTO TOTAL: € {custo_total:.2f}")
            
            self.label_resultado.configure(text=res)
            
            lucro_txt = f"LUCRO:  € {lucro_abs:.2f}\nMARGEM: {margem:.1f}%"
            self.label_lucro.configure(text=lucro_txt)
            self.label_lucro.configure(text_color="#00ff00" if lucro_abs >= 0 else "#ff4d4d")
            self.label_status.configure(text="STATUS: ANÁLISE CONCLUÍDA", text_color="#00ff00")
            
        except Exception:
            messagebox.showerror("ERRO", "Preencha todos os campos com números.")

if __name__ == "__main__":
    app = App()
    app.mainloop()