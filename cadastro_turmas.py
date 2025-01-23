# cadastro_turmas.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv

class CadastroTurmas:
    def __init__(self, root, turmas, alunos_por_turma):
        self.root = root
        self.root.title("Cadastro de Turmas")
        self.root.geometry("1024x768")
        
        self.turmas = turmas
        self.alunos_por_turma = alunos_por_turma  # Mantém referência ao dicionário de alunos

        # Estilo personalizado
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10)
        style.configure("TLabel", font=("Helvetica", 14), padding=10)
        
        # Interface gráfica
        self.create_widgets()

    def create_widgets(self):
        # Botão de criar turma
        self.btn_criar_turma = ttk.Button(self.root, text="Criar Turma", command=self.criar_turma, style="TButton")
        self.btn_criar_turma.grid(row=0, column=0, padx=10, pady=10)
        
        # Botão de importar lista de turmas
        self.btn_importar_turmas = ttk.Button(self.root, text="Importar Lista de Turmas", command=self.importar_turmas, style="TButton")
        self.btn_importar_turmas.grid(row=0, column=1, padx=10, pady=10)
        
        # Botão de visualizar turmas
        self.btn_visualizar_turmas = ttk.Button(self.root, text="Visualizar Turmas", command=self.visualizar_turmas, style="TButton")
        self.btn_visualizar_turmas.grid(row=0, column=2, padx=10, pady=10)
        
        # Botão de cancelar
        self.btn_cancelar = ttk.Button(self.root, text="Cancelar", command=self.root.destroy, style="TButton")
        self.btn_cancelar.grid(row=0, column=3, padx=10, pady=10)

    def criar_turma(self):
        self.popup_window("Criar Turma", "Nome da Turma:", self.salvar_turma)

    def salvar_turma(self, nome_turma):
        if nome_turma and nome_turma not in self.turmas:
            self.turmas.append(nome_turma)
            self.alunos_por_turma[nome_turma] = []  # Inicializa a lista de alunos da nova turma
            messagebox.showinfo("Sucesso", "Turma criada com sucesso!")
            self.popup.destroy()
        else:
            messagebox.showwarning("Aviso", "Turma já existente ou nome inválido.")

    def importar_turmas(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv"), ("Todos os Arquivos", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    nome_turma = row[0]
                    if nome_turma and nome_turma not in self.turmas:
                        self.turmas.append(nome_turma)
                        self.alunos_por_turma[nome_turma] = []
            messagebox.showinfo("Sucesso", "Turmas importadas com sucesso!")

    def visualizar_turmas(self):
        self.visualizar_turmas_window = tk.Toplevel(self.root)
        self.visualizar_turmas_window.title("Visualizar Turmas")
        self.visualizar_turmas_window.geometry("600x400")
        
        self.turmas_listbox = tk.Listbox(self.visualizar_turmas_window, selectmode=tk.MULTIPLE)
        self.turmas_listbox.pack(padx=10, pady=10)
        
        for turma in self.turmas:
            self.turmas_listbox.insert(tk.END, turma)
        
        btn_excluir = ttk.Button(self.visualizar_turmas_window, text="Excluir", command=self.excluir_turmas, style="TButton")
        btn_excluir.pack(padx=10, pady=10)
        
        btn_editar = ttk.Button(self.visualizar_turmas_window, text="Editar", command=self.editar_turma, style="TButton")
        btn_editar.pack(padx=10, pady=10)
    
    def excluir_turmas(self):
        selecionadas = self.turmas_listbox.curselection()
        if not selecionadas:
            messagebox.showwarning("Aviso", "Nenhuma turma selecionada para exclusão.")
            return
        for index in selecionadas[::-1]:
            turma = self.turmas_listbox.get(index)
            del self.turmas[index]
            del self.alunos_por_turma[turma]  # Remove alunos da turma excluída
        self.visualizar_turmas_window.destroy()
        self.visualizar_turmas()
        messagebox.showinfo("Sucesso", "Turma(s) excluída(s) com sucesso.")

    def editar_turma(self):
        selecionada = self.turmas_listbox.curselection()
        if selecionada:
            turma_atual = self.turmas_listbox.get(selecionada[0])
            self.popup_window("Editar Turma", "Novo Nome da Turma:", self.salvar_edicao_turma, turma_atual)
        else:
            messagebox.showwarning("Aviso", "Selecione uma turma para editar.")

    def salvar_edicao_turma(self, nome_turma, turma_antiga):
        if nome_turma and nome_turma not in self.turmas:
            index = self.turmas.index(turma_antiga)
            self.turmas[index] = nome_turma
            self.alunos_por_turma[nome_turma] = self.alunos_por_turma.pop(turma_antiga)  # Atualiza alunos para a nova turma
            self.visualizar_turmas_window.destroy()
            self.visualizar_turmas()
            messagebox.showinfo("Sucesso", "Turma editada com sucesso.")
            self.popup.destroy()
        else:
            messagebox.showwarning("Aviso", "Turma já existente ou nome inválido.")

    def popup_window(self, title, label_text, save_command, current_value=""):
        self.popup = tk.Toplevel(self.root)
        self.popup.title(title)
        self.popup.geometry("400x200")
        
        lbl = ttk.Label(self.popup, text=label_text, style="TLabel")
        lbl.grid(row=0, column=0, padx=10, pady=10)
        
        self.entry = ttk.Entry(self.popup)
        self.entry.grid(row=0, column=1, padx=10, pady=10)
        self.entry.insert(0, current_value)
        
        btn_salvar = ttk.Button(self.popup, text="Salvar", command=lambda: save_command(self.entry.get(), current_value), style="TButton")
        btn_salvar.grid(row=1, column=0, padx=10, pady=10)
        
        btn_cancelar = ttk.Button(self.popup, text="Cancelar", command=self.popup.destroy, style="TButton")
        btn_cancelar.grid(row=1, column=1, padx=10, pady=10)
