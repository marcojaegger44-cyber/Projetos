#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interface de Lista de Clientes - Sistema CM
Interface para visualizar, editar e gerenciar clientes
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Optional
import logging

class InterfaceListaClientes:
    """Interface para listar e gerenciar clientes"""
    
    def __init__(self, parent, gerenciador_dados):
        self.parent = parent
        self.gerenciador_dados = gerenciador_dados
        
        self._criar_interface()
        self._atualizar_lista()
    
    def _criar_interface(self):
        """Cria a interface principal"""
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Lista de Clientes - Sistema CM")
        self.janela.geometry("1000x600")
        self.janela.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(self.janela)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barra de ferramentas
        self._criar_barra_ferramentas(main_frame)
        
        # Lista de clientes
        self._criar_lista_clientes(main_frame)
        
        # Botões de ação
        self._criar_botoes_acao(main_frame)
    
    def _criar_barra_ferramentas(self, parent):
        """Cria barra de ferramentas com filtros"""
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=(0, 10))
        
        # Busca
        ttk.Label(frame, text="Buscar:").pack(side="left", padx=(0, 5))
        self.entry_busca = ttk.Entry(frame, width=30)
        self.entry_busca.pack(side="left", padx=(0, 10))
        self.entry_busca.bind('<KeyRelease>', lambda e: self._filtrar_clientes())
        
        # Filtro por loja
        ttk.Label(frame, text="Loja:").pack(side="left", padx=(20, 5))
        self.combo_loja = ttk.Combobox(frame, values=["Todas", "Centro", "Shopping", "Zona Sul"], 
                                      state="readonly", width=15)
        self.combo_loja.pack(side="left", padx=(0, 10))
        self.combo_loja.set("Todas")
        self.combo_loja.bind('<<ComboboxSelected>>', lambda e: self._filtrar_clientes())
        
        # Botão atualizar
        ttk.Button(frame, text="Atualizar", command=self._atualizar_lista).pack(side="right", padx=5)
    
    def _criar_lista_clientes(self, parent):
        """Cria a lista de clientes"""
        # Frame para a lista
        frame_lista = ttk.Frame(parent)
        frame_lista.pack(fill="both", expand=True, pady=(0, 10))
        
        # Colunas da tabela
        colunas = ("nome", "cpf", "telefone", "email", "loja", "renda", "limite")
        
        # Treeview
        self.tree = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=15)
        
        # Configurar cabeçalhos
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("email", text="Email")
        self.tree.heading("loja", text="Loja")
        self.tree.heading("renda", text="Renda")
        self.tree.heading("limite", text="Limite")
        
        # Configurar larguras
        self.tree.column("nome", width=200)
        self.tree.column("cpf", width=120)
        self.tree.column("telefone", width=120)
        self.tree.column("email", width=200)
        self.tree.column("loja", width=100)
        self.tree.column("renda", width=100)
        self.tree.column("limite", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind duplo clique para editar
        self.tree.bind('<Double-1>', lambda e: self._editar_cliente())
    
    def _criar_botoes_acao(self, parent):
        """Cria botões de ação"""
        frame = ttk.Frame(parent)
        frame.pack(fill="x")
        
        ttk.Button(frame, text="Novo Cliente", command=self._novo_cliente).pack(side="left", padx=5)
        ttk.Button(frame, text="Editar", command=self._editar_cliente).pack(side="left", padx=5)
        ttk.Button(frame, text="Excluir", command=self._excluir_cliente).pack(side="left", padx=5)
        ttk.Button(frame, text="Visualizar", command=self._visualizar_cliente).pack(side="left", padx=5)
        ttk.Button(frame, text="Fechar", command=self.janela.destroy).pack(side="right", padx=5)
    
    def _atualizar_lista(self):
        """Atualiza a lista de clientes"""
        # Limpar lista
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar clientes
        for i, cliente in enumerate(self.gerenciador_dados.dados['cadastros']):
            # Formatar dados
            cpf_formatado = self._formatar_cpf(cliente.cpf) if cliente.cpf else ""
            telefone_principal = cliente.telefone_celular or cliente.telefone_residencial or ""
            renda_formatada = f"R$ {cliente.renda_mensal:.2f}" if cliente.renda_mensal > 0 else ""
            limite_formatado = f"R$ {cliente.limite_credito:.2f}" if cliente.limite_credito > 0 else ""
            
            # Inserir na lista
            self.tree.insert("", "end", values=(
                cliente.nome,
                cpf_formatado,
                telefone_principal,
                cliente.email,
                cliente.loja_cadastro,
                renda_formatada,
                limite_formatado
            ), tags=(i,))
    
    def _filtrar_clientes(self):
        """Filtra clientes conforme critérios"""
        # Limpar lista
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obter filtros
        busca = self.entry_busca.get().lower()
        loja_filtro = self.combo_loja.get()
        
        # Filtrar clientes
        for i, cliente in enumerate(self.gerenciador_dados.dados['cadastros']):
            # Filtro de busca
            if busca and busca not in cliente.nome.lower() and busca not in cliente.cpf:
                continue
            
            # Filtro de loja
            if loja_filtro != "Todas" and cliente.loja_cadastro != loja_filtro:
                continue
            
            # Formatar dados
            cpf_formatado = self._formatar_cpf(cliente.cpf) if cliente.cpf else ""
            telefone_principal = cliente.telefone_celular or cliente.telefone_residencial or ""
            renda_formatada = f"R$ {cliente.renda_mensal:.2f}" if cliente.renda_mensal > 0 else ""
            limite_formatado = f"R$ {cliente.limite_credito:.2f}" if cliente.limite_credito > 0 else ""
            
            # Inserir na lista
            self.tree.insert("", "end", values=(
                cliente.nome,
                cpf_formatado,
                telefone_principal,
                cliente.email,
                cliente.loja_cadastro,
                renda_formatada,
                limite_formatado
            ), tags=(i,))
    
    def _formatar_cpf(self, cpf):
        """Formata CPF para exibição"""
        if not cpf:
            return ""
        cpf_limpo = cpf.replace(".", "").replace("-", "")
        if len(cpf_limpo) == 11:
            return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        return cpf
    
    def _novo_cliente(self):
        """Abre interface para novo cliente"""
        from interface_cadastro_clientes import InterfaceCadastroClientes
        InterfaceCadastroClientes(self.parent, self.gerenciador_dados)
        self._atualizar_lista()
    
    def _editar_cliente(self):
        """Edita cliente selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente para editar")
            return
        
        # Obter índice do cliente
        item = self.tree.item(selecionado[0])
        indice = int(item['tags'][0])
        cliente = self.gerenciador_dados.dados['cadastros'][indice]
        
        # Abrir interface de edição
        from interface_cadastro_clientes import InterfaceCadastroClientes
        InterfaceCadastroClientes(self.parent, self.gerenciador_dados, cliente, indice)
        self._atualizar_lista()
    
    def _excluir_cliente(self):
        """Exclui cliente selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente para excluir")
            return
        
        # Obter dados do cliente
        item = self.tree.item(selecionado[0])
        indice = int(item['tags'][0])
        cliente = self.gerenciador_dados.dados['cadastros'][indice]
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar Exclusão", 
                              f"Tem certeza que deseja excluir o cliente {cliente.nome}?"):
            try:
                self.gerenciador_dados.remover_cliente(indice)
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                self._atualizar_lista()
            except Exception as e:
                logging.error(f"Erro ao excluir cliente: {e}")
                messagebox.showerror("Erro", f"Erro ao excluir cliente: {e}")
    
    def _visualizar_cliente(self):
        """Visualiza detalhes do cliente"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente para visualizar")
            return
        
        # Obter dados do cliente
        item = self.tree.item(selecionado[0])
        indice = int(item['tags'][0])
        cliente = self.gerenciador_dados.dados['cadastros'][indice]
        
        # Criar janela de visualização
        self._criar_janela_visualizacao(cliente)
    
    def _criar_janela_visualizacao(self, cliente):
        """Cria janela para visualizar detalhes do cliente"""
        janela = tk.Toplevel(self.janela)
        janela.title(f"Detalhes - {cliente.nome}")
        janela.geometry("600x500")
        janela.grab_set()
        
        # Frame principal com scrollbar
        main_frame = ttk.Frame(janela)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas para scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Exibir dados do cliente
        self._exibir_dados_cliente(scrollable_frame, cliente)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botão fechar
        ttk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)
    
    def _exibir_dados_cliente(self, parent, cliente):
        """Exibe dados detalhados do cliente"""
        # Dados pessoais
        frame_pessoais = ttk.LabelFrame(parent, text="Dados Pessoais", padding=10)
        frame_pessoais.pack(fill="x", pady=5)
        
        dados_pessoais = [
            ("Nome:", cliente.nome),
            ("Data de Nascimento:", cliente.data_nascimento),
            ("CPF:", self._formatar_cpf(cliente.cpf)),
            ("Identidade:", cliente.identidade),
            ("Email:", cliente.email),
            ("Estado Civil:", cliente.estado_civil),
            ("Profissão:", cliente.profissao)
        ]
        
        for i, (label, valor) in enumerate(dados_pessoais):
            ttk.Label(frame_pessoais, text=label, font=("Arial", 9, "bold")).grid(row=i, column=0, sticky="w", pady=2)
            ttk.Label(frame_pessoais, text=valor or "Não informado").grid(row=i, column=1, sticky="w", padx=(10, 0), pady=2)
        
        # Endereço
        if cliente.endereco:
            frame_endereco = ttk.LabelFrame(parent, text="Endereço", padding=10)
            frame_endereco.pack(fill="x", pady=5)
            ttk.Label(frame_endereco, text=cliente.endereco, wraplength=500).pack(anchor="w")
        
        # Contatos
        frame_contatos = ttk.LabelFrame(parent, text="Contatos", padding=10)
        frame_contatos.pack(fill="x", pady=5)
        
        contatos = [
            ("Residencial:", cliente.telefone_residencial),
            ("Celular:", cliente.telefone_celular),
            ("Comercial:", cliente.telefone_comercial),
            ("Trabalho:", cliente.telefone_trabalho)
        ]
        
        for i, (tipo, numero) in enumerate(contatos):
            if numero:
                ttk.Label(frame_contatos, text=f"{tipo} {numero}").pack(anchor="w", pady=1)
        
        # Trabalho
        if cliente.onde_trabalha:
            frame_trabalho = ttk.LabelFrame(parent, text="Trabalho", padding=10)
            frame_trabalho.pack(fill="x", pady=5)
            ttk.Label(frame_trabalho, text=f"Onde trabalha: {cliente.onde_trabalha}").pack(anchor="w")
        
        # Financeiro
        if cliente.renda_mensal > 0 or cliente.limite_credito > 0:
            frame_financeiro = ttk.LabelFrame(parent, text="Informações Financeiras", padding=10)
            frame_financeiro.pack(fill="x", pady=5)
            
            if cliente.renda_mensal > 0:
                ttk.Label(frame_financeiro, text=f"Renda Mensal: R$ {cliente.renda_mensal:.2f}").pack(anchor="w")
            if cliente.limite_credito > 0:
                ttk.Label(frame_financeiro, text=f"Limite de Crédito: R$ {cliente.limite_credito:.2f}").pack(anchor="w")
        
        # Referências
        if cliente.referencias:
            frame_ref = ttk.LabelFrame(parent, text="Referências", padding=10)
            frame_ref.pack(fill="x", pady=5)
            
            for ref in cliente.referencias:
                ttk.Label(frame_ref, text=f"{ref['nome']} - {ref['telefone']} ({ref['parentesco']})").pack(anchor="w", pady=1)
        
        # Observações
        if cliente.observacao:
            frame_obs = ttk.LabelFrame(parent, text="Observações", padding=10)
            frame_obs.pack(fill="x", pady=5)
            ttk.Label(frame_obs, text=cliente.observacao, wraplength=500).pack(anchor="w")
