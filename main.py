import tkinter as tk
from tkinter import ttk, messagebox
from models import Produto
from email_envios import enviar_email
from tkinter import font as tkfont

class ControleEstoque:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Estoque - Sistema Moderno")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        
        self.configurar_estilos()
        
        self.criar_interface()
        self.carregar_produtos()
    
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10), padding=6)
        style.configure('TEntry', padding=5)
        style.configure('Treeview', font=('Helvetica', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
        style.configure('TLabelframe', background='#f0f0f0', font=('Helvetica', 10, 'bold'))
        style.configure('TLabelframe.Label', background='#f0f0f0')
        
        style.map('TButton',
                  foreground=[('active', 'black'), ('!disabled', 'black')],
                  background=[('active', '#e1e1e1'), ('!disabled', '#d9d9d9')])
        
        style.map('Treeview',
                  background=[('selected', '#4a6984')],
                  foreground=[('selected', 'white')])
    
    def criar_interface(self):
        main_frame = ttk.Frame(self.root, padding=(15, 15, 15, 15))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_font = tkfont.Font(family='Helvetica', size=16, weight='bold')
        ttk.Label(title_frame, text="CONTROLE DE ESTOQUE", font=title_font, 
                 background='#f0f0f0').pack(side=tk.LEFT)
        
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Nome', 'Quantidade', 'Mínimo', 'Status'),
            show='headings',
            yscrollcommand=vsb.set,
            selectmode='browse'
        )
        vsb.config(command=self.tree.yview)
        
        self.tree.heading('ID', text='ID', anchor=tk.CENTER)
        self.tree.heading('Nome', text='NOME DO PRODUTO', anchor=tk.CENTER)
        self.tree.heading('Quantidade', text='QUANTIDADE', anchor=tk.CENTER)
        self.tree.heading('Mínimo', text='ESTOQUE MÍNIMO', anchor=tk.CENTER)
        self.tree.heading('Status', text='STATUS', anchor=tk.CENTER)
        
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Nome', width=250, anchor=tk.W)
        self.tree.column('Quantidade', width=100, anchor=tk.CENTER)
        self.tree.column('Mínimo', width=100, anchor=tk.CENTER)
        self.tree.column('Status', width=150, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 10))
        
        button_style = {'style': 'TButton', 'padding': (10, 5)}
        
        ttk.Button(btn_frame, text="↻ Atualizar", command=self.carregar_produtos, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✏ Editar", command=self.abrir_tela_atualizar, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑 Excluir", command=self.excluir_produto, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔍 Filtrar", command=self.abrir_filtro, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⚠ Enviar Alertas", command=self.enviar_alertas, **button_style).pack(side=tk.LEFT, padx=5)
        
        form_frame = ttk.LabelFrame(main_frame, text=" CADASTRAR NOVO PRODUTO ", padding=(15, 10, 15, 15))
        form_frame.pack(fill=tk.X, pady=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        ttk.Label(form_frame, text="Nome do Produto:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nome_entry = ttk.Entry(form_frame, font=('Helvetica', 10))
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Quantidade em Estoque:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.quantidade_entry = ttk.Entry(form_frame, font=('Helvetica', 10))
        self.quantidade_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Estoque Mínimo:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.minimo_entry = ttk.Entry(form_frame, font=('Helvetica', 10))
        self.minimo_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Button(form_frame, text="➕ Cadastrar Produto", command=self.cadastrar_produto, 
                  style='Accent.TButton').grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky=tk.EW)
        
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'), 
                       foreground='white', background='#4a6984')
        style.map('Accent.TButton',
                 background=[('active', '#5a7a94'), ('!disabled', '#4a6984')])
    
    def excluir_produto(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.", parent=self.root)
            return
            
        item = self.tree.item(item_selecionado)
        id_produto, nome, _, _, _ = item['values']
        
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o produto '{nome}'?",
            parent=self.root
        )
        
        if resposta:
            produto = Produto.get(Produto.id == id_produto)
            produto.delete_instance()
            self.carregar_produtos()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!", parent=self.root)
    
    def carregar_produtos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for produto in Produto.select():
            status = "Normal"
            tags = ()
            
            if produto.quantidade < produto.minimo:
                status = "Estoque Baixo"
                tags = ('estoque_baixo',)
            elif produto.quantidade == produto.minimo:
                status = "Atenção"
                tags = ('atencao',)
            
            self.tree.insert('', tk.END, values=(
                produto.id, 
                produto.nome, 
                produto.quantidade, 
                produto.minimo,
                status
            ), tags=tags)
        
        self.tree.tag_configure('estoque_baixo', background='#ffdddd')
        self.tree.tag_configure('atencao', background='#fff3cd')
    
    def cadastrar_produto(self):
        nome = self.nome_entry.get().strip()
        quantidade = self.quantidade_entry.get().strip()
        minimo = self.minimo_entry.get().strip()
        
        if not nome or not quantidade or not minimo:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!", parent=self.root)
            return
            
        try:
            quantidade = int(quantidade)
            minimo = int(minimo)
            
            if quantidade < 0 or minimo < 0:
                raise ValueError
                
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e mínimo devem ser números inteiros positivos!", parent=self.root)
            return
            
        Produto.create(
            nome=nome,
            quantidade=quantidade,
            minimo=minimo
        )
        
        self.nome_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.minimo_entry.delete(0, tk.END)
        
        self.carregar_produtos()
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!", parent=self.root)
    
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
                
        messagebox.showinfo("Alertas Enviados", 
                          f"{enviados} alerta(s) de estoque baixo foram enviados por email.",
                          parent=self.root)

    def abrir_tela_atualizar(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para editar.", parent=self.root)
            return
            
        item = self.tree.item(item_selecionado)
        id_produto, nome, quantidade, minimo, _ = item['values']

        update_window = tk.Toplevel(self.root)
        update_window.title(f"Editar Produto: {nome}")
        update_window.geometry("400x300")
        update_window.resizable(False, False)
        
        self.centralizar_janela(update_window)
        
        main_frame = ttk.Frame(update_window, padding=(20, 15))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Nome do Produto:").pack(pady=(0, 5))
        nome_entry = ttk.Entry(main_frame, font=('Helvetica', 10))
        nome_entry.pack(fill=tk.X, pady=(0, 15))
        nome_entry.insert(0, nome)
        
        ttk.Label(main_frame, text="Quantidade em Estoque:").pack(pady=(0, 5))
        quantidade_entry = ttk.Entry(main_frame, font=('Helvetica', 10))
        quantidade_entry.pack(fill=tk.X, pady=(0, 15))
        quantidade_entry.insert(0, quantidade)
        
        ttk.Label(main_frame, text="Estoque Mínimo:").pack(pady=(0, 5))
        minimo_entry = ttk.Entry(main_frame, font=('Helvetica', 10))
        minimo_entry.pack(fill=tk.X, pady=(0, 20))
        minimo_entry.insert(0, minimo)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        def atualizar_produto():
            novo_nome = nome_entry.get().strip()
            nova_quantidade = quantidade_entry.get().strip()
            novo_minimo = minimo_entry.get().strip()

            if not novo_nome or not nova_quantidade or not novo_minimo:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!", parent=update_window)
                return
                
            try:
                nova_quantidade = int(nova_quantidade)
                novo_minimo = int(novo_minimo)
                
                if nova_quantidade < 0 or novo_minimo < 0:
                    raise ValueError
                    
            except ValueError:
                messagebox.showerror("Erro", "Quantidade e mínimo devem ser números inteiros positivos!", 
                                   parent=update_window)
                return

            produto = Produto.get(Produto.id == id_produto)
            produto.nome = novo_nome
            produto.quantidade = nova_quantidade
            produto.minimo = novo_minimo
            produto.save()
            
            self.carregar_produtos()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!", parent=update_window)
            update_window.destroy()

        ttk.Button(btn_frame, text="Salvar Alterações", command=atualizar_produto,
                  style='Accent.TButton').pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Cancelar", command=update_window.destroy).pack(side=tk.RIGHT, padx=5)

    def abrir_filtro(self):
        filtro_window = tk.Toplevel(self.root)
        filtro_window.title("Filtrar Produtos")
        filtro_window.geometry("350x250")
        filtro_window.resizable(False, False)
        
        self.centralizar_janela(filtro_window)
        
        main_frame = ttk.Frame(filtro_window, padding=(20, 15))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Filtrar por:", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        def aplicar_filtro(tipo):
            self.tree.delete(*self.tree.get_children())
            
            if tipo == 'abaixo':
                produtos = Produto.select().where(Produto.quantidade < Produto.minimo)
                titulo = "Produtos com Estoque Abaixo do Mínimo"
            elif tipo == 'normal':
                produtos = Produto.select().where(Produto.quantidade >= Produto.minimo)
                titulo = "Produtos com Estoque Normal"
            else:  
                produtos = Produto.select()
                titulo = "Todos os Produtos"
            
            for p in produtos:
                status = "Normal"
                tags = ()
                
                if p.quantidade < p.minimo:
                    status = "Estoque Baixo"
                    tags = ('estoque_baixo',)
                elif p.quantidade == p.minimo:
                    status = "Atenção"
                    tags = ('atencao',)
                
                self.tree.insert('', tk.END, values=(
                    p.id, 
                    p.nome, 
                    p.quantidade, 
                    p.minimo,
                    status
                ), tags=tags)
            
            filtro_window.destroy()
            self.root.title(f"Controle de Estoque - {titulo}")

        ttk.Button(main_frame, text="Estoque Abaixo do Mínimo", 
                  command=lambda: aplicar_filtro('abaixo')).pack(fill=tk.X, pady=5)
        
        ttk.Button(main_frame, text="Estoque Normal", 
                  command=lambda: aplicar_filtro('normal')).pack(fill=tk.X, pady=5)
        
        ttk.Button(main_frame, text="Todos os Produtos", 
                  command=lambda: aplicar_filtro('todos')).pack(fill=tk.X, pady=5)
        
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Label(main_frame, text="Pesquisar por Nome:").pack(anchor=tk.W, pady=(0, 5))
        
        nome_frame = ttk.Frame(main_frame)
        nome_frame.pack(fill=tk.X)
        
        nome_entry = ttk.Entry(nome_frame)
        nome_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        def pesquisar():
            nome_busca = nome_entry.get().strip()
            if not nome_busca:
                return
                
            self.tree.delete(*self.tree.get_children())
            
            for p in Produto.select().where(Produto.nome.contains(nome_busca)):
                status = "Normal"
                tags = ()
                
                if p.quantidade < p.minimo:
                    status = "Estoque Baixo"
                    tags = ('estoque_baixo',)
                elif p.quantidade == p.minimo:
                    status = "Atenção"
                    tags = ('atencao',)
                
                self.tree.insert('', tk.END, values=(
                    p.id, 
                    p.nome, 
                    p.quantidade, 
                    p.minimo,
                    status
                ), tags=tags)
            
            filtro_window.destroy()
            self.root.title(f"Controle de Estoque - Pesquisa: {nome_busca}")
        
        ttk.Button(nome_frame, text="🔍", command=pesquisar, width=3).pack(side=tk.LEFT)
    
    def centralizar_janela(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = ControleEstoque(root)
    root.mainloop()