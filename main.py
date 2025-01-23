# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from cadastro_alunos import CadastroAlunos
from cadastro_turmas import CadastroTurmas
from gerar_escalas import GerarEscalas
from data_manager import carregar_dados, salvar_dados


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerar Escalas")
        self.root.geometry("1280x720")

        # Adicionando imagem de fundo
        self.background_image = Image.open("C:/Users/halis/OneDrive/Documentos/Gerar_Escalas/logo.jpg")
        self.bg_img = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.root, width=self.bg_img.width(), height=self.bg_img.height())
        self.canvas.pack(fill="both", expand=True)

        # Centralizando a imagem de fundo
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        # Estilo personalizado
        self.style = ttk.Style()

        # Estilo personalizado para botões (Texto preto em fundo claro)
        self.style.configure("Custom.TButton",
                             font=("Helvetica", 12, "bold"),
                             padding=10)

        self.style.map("Custom.TButton",
                       foreground=[('disabled', '#000000'),
                                   ('!disabled', '#000000')],
                       background=[('active', '#D3D3D3'),
                                   ('!disabled', '#F0F0F0')])

        # Estilo personalizado para labels
        self.style.configure("Custom.TLabel",
                             font=("Helvetica", 14),
                             background="#f0f0f0",
                             foreground="#333333")

        # Carregando dados salvos
        self.turmas, self.alunos_por_turma = carregar_dados()

        # Adicionando Notebook (abas)
        self.notebook = ttk.Notebook(self.canvas)
        self.notebook.place(relx=0.5, rely=0.5, anchor="center")

        # Criando as abas
        self.create_tabs()

        # Salvando dados ao fechar o programa
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_tabs(self):
        # Aba Cadastro de Turmas
        tab_cadastro_turmas = ttk.Frame(self.notebook)
        self.notebook.add(tab_cadastro_turmas, text="Cadastro de Turmas")
        self.create_cadastro_turmas_widgets(tab_cadastro_turmas)

        # Aba Cadastro de Alunos
        tab_cadastro_alunos = ttk.Frame(self.notebook)
        self.notebook.add(tab_cadastro_alunos, text="Cadastro de Alunos")
        self.create_cadastro_alunos_widgets(tab_cadastro_alunos)

        # Aba Gerar Escalas
        tab_gerar_escalas = ttk.Frame(self.notebook)
        self.notebook.add(tab_gerar_escalas, text="Gerar Escalas")
        self.create_gerar_escalas_widgets(tab_gerar_escalas)

    def create_cadastro_turmas_widgets(self, tab):
        label = ttk.Label(tab, text="Cadastro de Turmas", style="Custom.TLabel")
        label.pack(pady=20)
        btn_cadastro_turmas = ttk.Button(tab, text="Abrir Cadastro de Turmas",
                                         command=self.abrir_cadastro_turmas,
                                         style="Custom.TButton")
        btn_cadastro_turmas.pack(padx=10, pady=10)

    def create_cadastro_alunos_widgets(self, tab):
        label = ttk.Label(tab, text="Cadastro de Alunos", style="Custom.TLabel")
        label.pack(pady=20)
        btn_cadastro_alunos = ttk.Button(tab, text="Abrir Cadastro de Alunos",
                                         command=self.abrir_cadastro_alunos,
                                         style="Custom.TButton")
        btn_cadastro_alunos.pack(padx=10, pady=10)

    def create_gerar_escalas_widgets(self, tab):
        label = ttk.Label(tab, text="Gerar Escalas", style="Custom.TLabel")
        label.pack(pady=20)
        btn_gerar_escalas = ttk.Button(tab, text="Abrir Gerar Escalas",
                                       command=self.abrir_gerar_escalas,
                                       style="Custom.TButton")
        btn_gerar_escalas.pack(padx=10, pady=10)

    def abrir_cadastro_turmas(self):
        cadastro_turmas_window = tk.Toplevel(self.root)
        cadastro_turmas_window.geometry("1024x768")
        CadastroTurmas(cadastro_turmas_window, self.turmas, self.alunos_por_turma)

    def abrir_cadastro_alunos(self):
        if not self.turmas:
            messagebox.showwarning("Erro", "Por favor, cadastre as turmas primeiro.")
            return
        cadastro_alunos_window = tk.Toplevel(self.root)
        cadastro_alunos_window.geometry("1024x768")
        CadastroAlunos(cadastro_alunos_window, self.turmas, self.alunos_por_turma)

    def abrir_gerar_escalas(self):
        if not self.turmas or not any(self.alunos_por_turma.values()):
            messagebox.showwarning("Erro", "Por favor, cadastre turmas e alunos primeiro.")
            return
        gerar_escalas_window = tk.Toplevel(self.root)
        gerar_escalas_window.geometry("1024x768")
        GerarEscalas(gerar_escalas_window, self.turmas, self.alunos_por_turma)

    def on_closing(self):
        # Salva os dados antes de fechar
        salvar_dados(self.turmas, self.alunos_por_turma)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
