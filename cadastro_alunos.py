import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class CadastroAlunos:
    def __init__(self, root, turmas, alunos_por_turma):
        self.root = root
        self.root.title("Cadastro de Alunos")
        self.root.geometry("1024x768")
        
        self.turmas = turmas
        self.alunos_por_turma = alunos_por_turma

        # Estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Helvetica", 12, "bold"), padding=10)
        style.configure("Custom.TLabel", font=("Helvetica", 14))
        
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
        self.btn_salvar = ttk.Button(self.root, text="Salvar", command=self.salvar_aluno, style="Custom.TButton")
        self.btn_salvar.grid(row=2, column=2, padx=10, pady=10)

        # Botão Importar
        self.btn_importar = ttk.Button(self.root, text="Importar", command=self.importar_alunos, style="Custom.TButton")
        self.btn_importar.grid(row=3, column=0, padx=10, pady=10)
        # Tooltip ao passar o mouse
        self.btn_importar.bind("<Enter>", lambda e: self.btn_importar.config(text="Permite importar uma lista de alunos"))
        self.btn_importar.bind("<Leave>", lambda e: self.btn_importar.config(text="Importar"))

        # Botão Visualizar Alunos
        self.btn_visualizar = ttk.Button(self.root, text="Visualizar Alunos", command=self.visualizar_alunos,
                                         style="Custom.TButton")
        self.btn_visualizar.grid(row=3, column=1, padx=10, pady=10)

        # Botão Cancelar
        self.btn_cancelar = ttk.Button(self.root, text="Cancelar", command=self.root.destroy, style="Custom.TButton")
        self.btn_cancelar.grid(row=3, column=2, padx=10, pady=10)

        # Botão Limpar Todos os Dados
        self.btn_limpar = ttk.Button(self.root, text="Limpar Todos os Dados", command=self.limpar_dados, style="Custom.TButton")
        self.btn_limpar.grid(row=4, column=0, padx=10, pady=10)

        # Botão Editar/Apagar Aluno
        self.btn_editar_apagar = ttk.Button(self.root, text="Editar/Apagar Aluno", command=self.editar_apagar_aluno, style="Custom.TButton")
        self.btn_editar_apagar.grid(row=4, column=1, padx=10, pady=10)

    def salvar_aluno(self):
        turma = self.turma_selecionada.get()
        nome = self.entry_nome.get()
        if turma and nome:
            if nome not in self.alunos_por_turma.setdefault(turma, []):
                self.alunos_por_turma[turma].append(nome)
                messagebox.showinfo("Sucesso", "Aluno salvo com sucesso!")
                self.entry_nome.delete(0, tk.END)
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
            with open(file_path, 'r', encoding='utf-8') as file:
                alunos = file.readlines()
                for aluno in alunos:
                    nome_aluno = aluno.strip()
                    if nome_aluno and nome_aluno not in self.alunos_por_turma.setdefault(turma, []):
                        self.alunos_por_turma[turma].append(nome_aluno)
            messagebox.showinfo("Sucesso", "Alunos importados com sucesso!")

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
        confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar todos os dados?")
        if confirm:
            self.alunos_por_turma.clear()
            messagebox.showinfo("Sucesso", "Todos os dados foram limpos.")

    def editar_apagar_aluno(self):
        turma = self.turma_selecionada.get()
        if not turma:
            messagebox.showwarning("Erro", "Por favor, selecione uma turma.")
            return

        self.editar_apagar_window = tk.Toplevel(self.root)
        self.editar_apagar_window.title(f"Editar/Apagar Aluno - Turma {turma}")
        self.editar_apagar_window.geometry("400x300")

        label_title = ttk.Label(self.editar_apagar_window, text=f"Editar/Apagar Aluno - Turma {turma}",
                                style="Custom.TLabel")
        label_title.pack(pady=20)

        self.alunos_listbox = tk.Listbox(self.editar_apagar_window, width=50, height=10)
        self.alunos_listbox.pack(padx=10, pady=10)

        for aluno in self.alunos_por_turma.get(turma, []):
            self.alunos_listbox.insert(tk.END, aluno)

        btn_editar = ttk.Button(self.editar_apagar_window, text="Editar", command=self.editar_aluno, style="Custom.TButton")
        btn_editar.pack(side=tk.LEFT, padx=10, pady=10)

        btn_apagar = ttk.Button(self.editar_apagar_window, text="Apagar", command=self.apagar_aluno, style="Custom.TButton")
        btn_apagar.pack(side=tk.RIGHT, padx=10, pady=10)

    def editar_aluno(self):
        selected = self.alunos_listbox.curselection()
        if not selected:
            messagebox.showwarning("Erro", "Por favor, selecione um aluno para editar.")
            return

        aluno_selecionado = self.alunos_listbox.get(selected)
        novo_nome = simpledialog.askstring("Editar Aluno", "Digite o novo nome:", initialvalue=aluno_selecionado)
        if novo_nome:
            turma = self.turma_selecionada.get()
            self.alunos_por_turma[turma][selected[0]] = novo_nome
            self.alunos_listbox.delete(selected)
            self.alunos_listbox.insert(selected, novo_nome)
            messagebox.showinfo("Sucesso", "Aluno editado com sucesso!")

    def apagar_aluno(self):
        selected = self.alunos_listbox.curselection()
        if not selected:
            messagebox.showwarning("Erro", "Por favor, selecione um aluno para apagar.")
            return

        confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar este aluno?")
        if confirm:
            turma = self.turma_selecionada.get()
            aluno_selecionado = self.alunos_listbox.get(selected)
            self.alunos_por_turma[turma].remove(aluno_selecionado)
            self.alunos_listbox.delete(selected)
            messagebox.showinfo("Sucesso", "Aluno apagado com sucesso!")

# Exemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    turmas = ["Turma A", "Turma B", "Turma C"]
    alunos_por_turma = {}
    app = CadastroAlunos(root, turmas, alunos_por_turma)
    root.mainloop()