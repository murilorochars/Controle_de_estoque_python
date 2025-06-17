import tkinter as tk
from tkinter import ttk, messagebox
from models import Produto
from email_envios import enviar_email

class ControleEstoque:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Estoque")
        self.root.geometry("800x600")
        
        self.criar_interface()
        self.carregar_produtos()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabela de produtos
        self.tree = ttk.Treeview(main_frame, columns=('ID', 'Nome', 'Quantidade', 'Mínimo'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Quantidade', text='Quantidade')
        self.tree.heading('Mínimo', text='Mínimo')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame de controles
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Atualizar", command=self.carregar_produtos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Enviar Alertas", command=self.enviar_alertas).pack(side=tk.LEFT, padx=5)
        
        # Frame de cadastro
        form_frame = ttk.LabelFrame(main_frame, text="Cadastrar Produto")
        form_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nome_entry = ttk.Entry(form_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.quantidade_entry = ttk.Entry(form_frame)
        self.quantidade_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Mínimo:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.minimo_entry = ttk.Entry(form_frame)
        self.minimo_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Button(form_frame, text="Cadastrar", command=self.cadastrar_produto).grid(row=3, column=0, columnspan=2, pady=5)
    
    def carregar_produtos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for produto in Produto.select():
            self.tree.insert('', tk.END, values=(
                produto.id,
                produto.nome,
                produto.quantidade,
                produto.minimo
            ))
    
    def cadastrar_produto(self):
        nome = self.nome_entry.get()
        quantidade = self.quantidade_entry.get()
        minimo = self.minimo_entry.get()
        
        if nome and quantidade and minimo:
            try:
                Produto.create(
                    nome=nome,
                    quantidade=int(quantidade),
                    minimo=int(minimo)
                )
                self.carregar_produtos()
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade e mínimo devem ser números")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos")
    
    def enviar_alertas(self):
        enviados = 0
        for produto in Produto.select():
            if produto.quantidade < produto.minimo:
                enviar_email(
                    "ofcsmurilo@gmail.com",
                    f"Alerta: Estoque baixo - {produto.nome}",
                    f"O estoque de {produto.nome} está em {produto.quantidade} (mínimo: {produto.minimo})"
                )
                enviados += 1
        messagebox.showinfo("Alertas", f"{enviados} alerta(s) enviado(s)")

if __name__ == "__main__":
    root = tk.Tk()
    app = ControleEstoque(root)
    root.mainloop()