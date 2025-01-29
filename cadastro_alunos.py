import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from data_manager import salvar_dados


class CadastroAlunos:
    def __init__(self, root, turmas, alunos_por_turma):
        self.root = root
        self.root.title("Cadastro de Alunos")
        self.root.geometry("1024x768")

        self.turmas = turmas
        self.alunos_por_turma = alunos_por_turma

        # Estilo personalizado
        self.style = ttk.Style()
        self.style.configure("Custom.TButton",
                             font=("Helvetica", 12, "bold"),
                             padding=10)

        self.style.map("Custom.TButton",
                       foreground=[('disabled', '#000000'),
                                   ('!disabled', '#000000')],
                       background=[('active', '#D3D3D3'),
                                   ('!disabled', '#F0F0F0')])

        self.style.configure("Custom.TLabel",
                             font=("Helvetica", 14),
                             foreground="#333333")

        # Interface gráfica
        self.create_widgets()

    def create_widgets(self):
        # Label de título
        label_title = ttk.Label(self.root, text="Cadastro de Alunos", style="Custom.TLabel")
        label_title.grid(row=0, column=0, columnspan=3, pady=20)

        # Caixa de seleção para turmas
        self.label_turma = ttk.Label(self.root, text="Selecione a Turma:", style="Custom.TLabel")
        self.label_turma.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)

        self.turma_selecionada = tk.StringVar()
        self.combo_turmas = ttk.Combobox(self.root, textvariable=self.turma_selecionada,
                                         values=self.turmas, state="readonly")
        self.combo_turmas.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # Entrada de nome do aluno
        self.label_nome = ttk.Label(self.root, text="Nome do Aluno:", style="Custom.TLabel")
        self.label_nome.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_nome = ttk.Entry(self.root, width=30)
        self.entry_nome.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Botão Salvar
        self.btn_salvar = ttk.Button(self.root, text="Salvar",
                                     command=self.salvar_aluno,
                                     style="Custom.TButton")
        self.btn_salvar.grid(row=2, column=2, padx=10, pady=10)

        # Botão Importar
        self.btn_importar = ttk.Button(self.root, text="Importar",
                                       command=self.importar_alunos,
                                       style="Custom.TButton")
        self.btn_importar.grid(row=3, column=0, padx=10, pady=10)

        # Botão Visualizar Alunos
        self.btn_visualizar = ttk.Button(self.root, text="Visualizar Alunos",
                                         command=self.visualizar_alunos,
                                         style="Custom.TButton")
        self.btn_visualizar.grid(row=3, column=1, padx=10, pady=10)

        # Botão Limpar Dados
        self.btn_limpar = ttk.Button(self.root, text="Limpar Dados",
                                     command=self.limpar_dados,
                                     style="Custom.TButton")
        self.btn_limpar.grid(row=4, column=0, padx=10, pady=10)

        # Botão Excluir Aluno
        self.btn_excluir = ttk.Button(self.root, text="Excluir Aluno",
                                      command=self.excluir_aluno,
                                      style="Custom.TButton")
        self.btn_excluir.grid(row=4, column=1, padx=10, pady=10)

        # Botão Cancelar
        self.btn_cancelar = ttk.Button(self.root, text="Cancelar",
                                       command=self.root.destroy,
                                       style="Custom.TButton")
        self.btn_cancelar.grid(row=4, column=2, padx=10, pady=10)

    def salvar_aluno(self):
        turma = self.turma_selecionada.get()
        nome = self.entry_nome.get()
        if turma and nome:
            if nome not in self.alunos_por_turma.setdefault(turma, []):
                self.alunos_por_turma[turma].append(nome)
                messagebox.showinfo("Sucesso", "Aluno salvo com sucesso!")
                self.entry_nome.delete(0, tk.END)
                salvar_dados(self.turmas, self.alunos_por_turma)
            else:
                messagebox.showwarning("Aviso", "Aluno já cadastrado na turma.")
        else:
            messagebox.showwarning("Erro", "Por favor, selecione uma turma e digite o nome do aluno.")

    def importar_alunos(self):
        turma = self.turma_selecionada.get()
        if not turma:
            messagebox.showwarning("Erro", "Por favor, selecione uma turma para importar alunos.")
            return

        file_path = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    alunos = file.readlines()
                    novos_alunos = 0
                    for aluno in alunos:
                        nome_aluno = aluno.strip()
                        if nome_aluno and nome_aluno not in self.alunos_por_turma.setdefault(turma, []):
                            self.alunos_por_turma[turma].append(nome_aluno)
                            novos_alunos += 1

                salvar_dados(self.turmas, self.alunos_por_turma)
                messagebox.showinfo("Sucesso", f"{novos_alunos} alunos foram importados para a turma '{turma}'.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao importar alunos: {e}")
        else:
            messagebox.showwarning("Aviso", "Nenhum arquivo foi selecionado.")

    def visualizar_alunos(self):
        turma = self.turma_selecionada.get()
        if turma:
            self.visualizar_alunos_window = tk.Toplevel(self.root)
            self.visualizar_alunos_window.title(f"Alunos da Turma {turma}")
            self.visualizar_alunos_window.geometry("600x400")

            label_title = ttk.Label(self.visualizar_alunos_window, text=f"Alunos da Turma {turma}",
                                    style="Custom.TLabel")
            label_title.pack(pady=20)

            self.alunos_listbox = tk.Listbox(self.visualizar_alunos_window, width=50, height=15)
            self.alunos_listbox.pack(padx=10, pady=10)

            for aluno in self.alunos_por_turma.get(turma, []):
                self.alunos_listbox.insert(tk.END, aluno)
        else:
            messagebox.showwarning("Erro", "Por favor, selecione uma turma.")

    def limpar_dados(self):
        confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja limpar todos os dados?")
        if confirm:
            self.alunos_por_turma.clear()
            salvar_dados(self.turmas, self.alunos_por_turma)
            messagebox.showinfo("Sucesso", "Todos os dados foram limpos.")

    def excluir_aluno(self):
        turma = self.turma_selecionada.get()
        if turma:
            nome = self.entry_nome.get()
            if nome in self.alunos_por_turma.get(turma, []):
                self.alunos_por_turma[turma].remove(nome)
                salvar_dados(self.turmas, self.alunos_por_turma)
                messagebox.showinfo("Sucesso", f"Aluno '{nome}' removido com sucesso.")
                self.entry_nome.delete(0, tk.END)
            else:
                messagebox.showwarning("Erro", "Aluno não encontrado na turma selecionada.")
        else:
            messagebox.showwarning("Erro", "Por favor, selecione uma turma.")
