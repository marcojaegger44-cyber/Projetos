#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interface de Cadastro de Clientes - Sistema CM
Interface completa para cadastro e edição de clientes
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import re
from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
# Classe CadastroCliente movida para models.py
from src.models import CadastroCliente
import sys
from pathlib import Path
# Adicionar src ao path para importar ui_utils
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
from ui_utils import aplicar_mascara_valor, aplicar_mascara_data, aplicar_mascara_telefone, aplicar_mascara_cpf
from PIL import Image, ImageTk

class InterfaceCadastroClientes:
    """Interface completa de cadastro de clientes"""
    
    def __init__(self, parent, gerenciador_dados, cliente_edicao=None, indice_edicao=None):
        self.parent = parent
        self.gerenciador_dados = gerenciador_dados
        self.cliente_edicao = cliente_edicao
        self.indice_edicao = indice_edicao
        self.is_edicao = cliente_edicao is not None
        self.foto_caminho = None
        
        # Opções fixas
        self.estados_civis = ["Solteiro", "Casado", "Divorciado", "Viúvo"]
        self.tipos_telefone = ["Residencial", "Celular", "Comercial"]
        self.graus_parentesco = ["Pai", "Mãe", "Irmão", "Amigo"]
        # Carregar lojas do banco de dados
        self.lojas = self._carregar_lojas()
        
        # Contadores para campos dinâmicos
        self.contador_telefones = 0
        self.contador_referencias = 0
        
        self._criar_interface()
    
    def _carregar_lojas(self):
        """Carrega lojas do banco de dados"""
        try:
            import sqlite3
            from pathlib import Path
            
            # Caminho do banco de dados - usar caminho absoluto
            db_path = Path.cwd() / "sistema.db"
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM loja WHERE ativo = 1 ORDER BY nome")
            lojas = cursor.fetchall()
            conn.close()
            
            # Retornar lista de tuplas (id, nome) para o combobox
            return [(f"{nome} (ID: {id})", id) for id, nome in lojas]
            
        except Exception as e:
            print(f"Erro ao carregar lojas: {e}")
            return [("Loja Principal (ID: 1)", 1)]
        
    def _criar_interface(self):
        """Cria a interface principal"""
        # Importar utilitários de janela
        sys.path.append('src')
        from window_utils import criar_janela_centralizada, aplicar_estilo_janela
        
        # Criar janela centralizada
        self.janela, self.frame_principal = criar_janela_centralizada(
            self.parent,
            "Cadastro de Cliente" if not self.is_edicao else "Editar Cliente",
            largura=900,
            altura=700,
            com_botao_voltar=True
        )
        
        # Aplicar estilo
        aplicar_estilo_janela(self.janela, tema_cyberpunk=True)
        self.janela.grab_set()
        
        # Frame principal com scrollbar
        self._criar_frame_principal()
        
        # Preencher campos se for edição
        if self.is_edicao:
            self._preencher_campos_edicao()
    
    def _criar_frame_principal(self):
        """Cria o frame principal com scrollbar"""
        # Usar o frame principal já criado pela função criar_janela_centralizada
        main_frame = self.frame_principal
        
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
        
        # Criar seções do formulário
        self._criar_secao_dados_pessoais(scrollable_frame)
        self._criar_secao_endereco(scrollable_frame)
        self._criar_secao_contatos(scrollable_frame)
        self._criar_secao_trabalho(scrollable_frame)
        self._criar_secao_financeiro(scrollable_frame)
        self._criar_secao_referencias(scrollable_frame)
        self._criar_secao_observacoes(scrollable_frame)
        self._criar_botoes(scrollable_frame)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel para scroll (apenas no canvas)
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
    
    def _criar_secao_dados_pessoais(self, parent):
        """Cria seção de dados pessoais"""
        frame = ttk.LabelFrame(parent, text="Dados Pessoais", padding=10)
        frame.pack(fill="x", pady=5)
        
        # Nome completo
        ttk.Label(frame, text="Nome Completo *:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_nome = ttk.Entry(frame, width=50)
        self.entry_nome.grid(row=0, column=1, columnspan=2, sticky="ew", pady=2)
        # Botões para foto
        photo_button_frame = ttk.Frame(frame)
        photo_button_frame.grid(row=7, column=0, columnspan=2, sticky="w", pady=5)
        ttk.Button(photo_button_frame, text="Upload Foto", command=self._upload_foto).pack(side="left", padx=5)
        ttk.Button(photo_button_frame, text="Remover Foto", command=self._remover_foto).pack(side="left", padx=5)
        
        self.photo_label = ttk.Label(frame, text="Nenhuma foto selecionada")
        self.photo_label.grid(row=8, column=0, columnspan=2, sticky="w", pady=5)
        
        # Data de nascimento
        ttk.Label(frame, text="Data de Nascimento *:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_data_nasc = ttk.Entry(frame, width=15)
        self.entry_data_nasc.grid(row=1, column=1, sticky="w", pady=2)
        ttk.Label(frame, text="(dd/mm/aaaa)").grid(row=1, column=2, sticky="w", pady=2)
        
        # CPF
        ttk.Label(frame, text="CPF *:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_cpf = ttk.Entry(frame, width=15)
        self.entry_cpf.grid(row=2, column=1, sticky="w", pady=2)
        ttk.Label(frame, text="(000.000.000-00)").grid(row=2, column=2, sticky="w", pady=2)
        
        # Identidade
        ttk.Label(frame, text="Identidade (RG) *:").grid(row=3, column=0, sticky="w", pady=2)
        self.entry_identidade = ttk.Entry(frame, width=15)
        self.entry_identidade.grid(row=3, column=1, sticky="w", pady=2)
        
        # Email
        ttk.Label(frame, text="Email:").grid(row=4, column=0, sticky="w", pady=2)
        self.entry_email = ttk.Entry(frame, width=30)
        self.entry_email.grid(row=4, column=1, sticky="w", pady=2)
        
        # Estado Civil
        ttk.Label(frame, text="Estado Civil:").grid(row=5, column=0, sticky="w", pady=2)
        self.combo_estado_civil = ttk.Combobox(frame, values=self.estados_civis, width=15, state="readonly")
        self.combo_estado_civil.grid(row=5, column=1, sticky="w", pady=2)
        
        # Profissão
        ttk.Label(frame, text="Profissão:").grid(row=6, column=0, sticky="w", pady=2)
        self.entry_profissao = ttk.Entry(frame, width=30)
        self.entry_profissao.grid(row=6, column=1, sticky="w", pady=2)
        
        # Configurar grid
        frame.columnconfigure(1, weight=1)
    
    def _criar_secao_endereco(self, parent):
        """Cria seção de endereço"""
        frame = ttk.LabelFrame(parent, text="Endereço", padding=10)
        frame.pack(fill="x", pady=5)
        
        ttk.Label(frame, text="Endereço Completo *:").grid(row=0, column=0, sticky="nw", pady=2)
        self.text_endereco = tk.Text(frame, width=50, height=3)
        self.text_endereco.grid(row=0, column=1, sticky="ew", pady=2)
        
        frame.columnconfigure(1, weight=1)
    
    def _criar_secao_contatos(self, parent):
        """Cria seção de contatos"""
        frame = ttk.LabelFrame(parent, text="Contatos", padding=10)
        frame.pack(fill="x", pady=5)
        
        # Telefones obrigatórios
        ttk.Label(frame, text="Telefone Residencial *:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_tel_residencial = ttk.Entry(frame, width=15)
        self.entry_tel_residencial.grid(row=0, column=1, sticky="w", pady=2)
        ttk.Label(frame, text="(11) 1234-5678").grid(row=0, column=2, sticky="w", pady=2)
        
        ttk.Label(frame, text="Telefone Celular *:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_tel_celular = ttk.Entry(frame, width=15)
        self.entry_tel_celular.grid(row=1, column=1, sticky="w", pady=2)
        ttk.Label(frame, text="(11) 99999-9999").grid(row=1, column=2, sticky="w", pady=2)
        
        ttk.Label(frame, text="Telefone Comercial *:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_tel_comercial = ttk.Entry(frame, width=15)
        self.entry_tel_comercial.grid(row=2, column=1, sticky="w", pady=2)
        ttk.Label(frame, text="(11) 3333-4444").grid(row=2, column=2, sticky="w", pady=2)
        
        # Telefones adicionais
        ttk.Label(frame, text="Telefones Adicionais:").grid(row=3, column=0, sticky="w", pady=(10,2))
        
        self.frame_telefones_adicionais = ttk.Frame(frame)
        self.frame_telefones_adicionais.grid(row=4, column=0, columnspan=3, sticky="ew", pady=2)
        
        ttk.Button(frame, text="+ Adicionar Telefone", 
                  command=self._adicionar_telefone).grid(row=5, column=0, sticky="w", pady=2)
        
        frame.columnconfigure(1, weight=1)
    
    def _criar_secao_trabalho(self, parent):
        """Cria seção de trabalho"""
        frame = ttk.LabelFrame(parent, text="Trabalho", padding=10)
        frame.pack(fill="x", pady=5)
        
        ttk.Label(frame, text="Onde Trabalha:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_onde_trabalha = ttk.Entry(frame, width=40)
        self.entry_onde_trabalha.grid(row=0, column=1, sticky="ew", pady=2)
        
        ttk.Label(frame, text="Telefone do Trabalho:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_tel_trabalho = ttk.Entry(frame, width=15)
        self.entry_tel_trabalho.grid(row=1, column=1, sticky="w", pady=2)
        ttk.Label(frame, text="(11) 3333-4444").grid(row=1, column=2, sticky="w", pady=2)
        
        frame.columnconfigure(1, weight=1)
    
    def _criar_secao_financeiro(self, parent):
        """Cria seção financeira"""
        frame = ttk.LabelFrame(parent, text="Informações Financeiras", padding=10)
        frame.pack(fill="x", pady=5)
        
        ttk.Label(frame, text="Renda Mensal:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_renda = ttk.Entry(frame, width=15)
        self.entry_renda.grid(row=0, column=1, sticky="w", pady=2)
        ttk.Label(frame, text="R$").grid(row=0, column=2, sticky="w", pady=2)
        
        ttk.Label(frame, text="Limite de Crédito:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_limite = ttk.Entry(frame, width=15)
        self.entry_limite.grid(row=1, column=1, sticky="w", pady=2)
        ttk.Label(frame, text="R$ (30% da renda)").grid(row=1, column=2, sticky="w", pady=2)
        
        ttk.Button(frame, text="Calcular Limite", 
                  command=self._calcular_limite_credito).grid(row=2, column=1, sticky="w", pady=2)
        
        # Bind para calcular automaticamente
        self.entry_renda.bind('<KeyRelease>', lambda e: self._calcular_limite_credito())
        
        # Aplicar máscaras
        aplicar_mascara_telefone(self.entry_tel_residencial)
        aplicar_mascara_telefone(self.entry_tel_celular)
        aplicar_mascara_telefone(self.entry_tel_comercial)
        aplicar_mascara_telefone(self.entry_tel_trabalho)
        aplicar_mascara_cpf(self.entry_cpf)
        aplicar_mascara_data(self.entry_data_nasc)
        aplicar_mascara_valor(self.entry_renda)
        aplicar_mascara_valor(self.entry_limite)
    
    def _criar_secao_referencias(self, parent):
        """Cria seção de referências"""
        frame = ttk.LabelFrame(parent, text="Referências", padding=10)
        frame.pack(fill="x", pady=5)
        
        ttk.Label(frame, text="Pessoas de Referência:").grid(row=0, column=0, sticky="w", pady=2)
        
        self.frame_referencias = ttk.Frame(frame)
        self.frame_referencias.grid(row=1, column=0, columnspan=3, sticky="ew", pady=2)
        
        ttk.Button(frame, text="+ Adicionar Referência", 
                  command=self._adicionar_referencia).grid(row=2, column=0, sticky="w", pady=2)
        
        frame.columnconfigure(0, weight=1)
    
    def _criar_secao_observacoes(self, parent):
        """Cria seção de observações"""
        frame = ttk.LabelFrame(parent, text="Observações e Loja", padding=10)
        frame.pack(fill="x", pady=5)
        
        ttk.Label(frame, text="Observações:").grid(row=0, column=0, sticky="nw", pady=2)
        self.text_observacao = tk.Text(frame, width=50, height=3)
        self.text_observacao.grid(row=0, column=1, sticky="ew", pady=2)
        
        ttk.Label(frame, text="Loja de Cadastro:").grid(row=1, column=0, sticky="w", pady=2)
        
        # Extrair apenas os nomes das lojas para o combobox
        loja_nomes = [loja[0] for loja in self.lojas]
        
        self.combo_loja = ttk.Combobox(frame, values=loja_nomes, width=20, state="readonly")
        self.combo_loja.grid(row=1, column=1, sticky="w", pady=2)
        if loja_nomes:
            self.combo_loja.current(0)
        
        frame.columnconfigure(1, weight=1)
    
    def _criar_botoes(self, parent):
        """Cria botões de ação"""
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=20)
        
        ttk.Button(frame, text="Salvar", command=self._salvar_cliente).pack(side="left", padx=5)
        ttk.Button(frame, text="Cancelar", command=self.janela.destroy).pack(side="left", padx=5)
        if self.is_edicao:
            ttk.Button(frame, text="Excluir", command=self._excluir_cliente).pack(side="left", padx=5)
            ttk.Button(frame, text="📋 Contratos", command=self._abrir_contratos).pack(side="left", padx=5)
    
    def _adicionar_telefone(self):
        """Adiciona campo de telefone adicional"""
        frame_tel = ttk.Frame(self.frame_telefones_adicionais)
        frame_tel.pack(fill="x", pady=2)
        
        ttk.Label(frame_tel, text="Tipo:").pack(side="left", padx=(0,5))
        combo_tipo = ttk.Combobox(frame_tel, values=self.tipos_telefone, width=12, state="readonly")
        combo_tipo.pack(side="left", padx=(0,10))
        combo_tipo.current(0)
        
        ttk.Label(frame_tel, text="Telefone:").pack(side="left", padx=(0,5))
        entry_tel = ttk.Entry(frame_tel, width=15)
        entry_tel.pack(side="left", padx=(0,10))
        
        ttk.Button(frame_tel, text="✕", command=lambda: frame_tel.destroy()).pack(side="left")
        
        # Armazenar referências
        frame_tel.combo_tipo = combo_tipo
        frame_tel.entry_tel = entry_tel
    
    def _adicionar_referencia(self):
        """Adiciona campo de referência"""
        frame_ref = ttk.Frame(self.frame_referencias)
        frame_ref.pack(fill="x", pady=2)
        
        ttk.Label(frame_ref, text="Nome:").pack(side="left", padx=(0,5))
        entry_nome = ttk.Entry(frame_ref, width=20)
        entry_nome.pack(side="left", padx=(0,10))
        
        ttk.Label(frame_ref, text="Telefone:").pack(side="left", padx=(0,5))
        entry_tel = ttk.Entry(frame_ref, width=15)
        entry_tel.pack(side="left", padx=(0,10))
        aplicar_mascara_telefone(entry_tel)
        
        ttk.Label(frame_ref, text="Parentesco:").pack(side="left", padx=(0,5))
        combo_parentesco = ttk.Combobox(frame_ref, values=self.graus_parentesco, width=12)
        combo_parentesco.pack(side="left", padx=(0,5))
        combo_parentesco.current(0)
        
        # Botão para adicionar novo tipo de parentesco
        def adicionar_parentesco():
            novo_parentesco = simpledialog.askstring("Novo Parentesco", "Digite o novo tipo de parentesco:")
            if novo_parentesco and novo_parentesco not in self.graus_parentesco:
                self.graus_parentesco.append(novo_parentesco)
                combo_parentesco['values'] = self.graus_parentesco
                combo_parentesco.set(novo_parentesco)
        
        ttk.Button(frame_ref, text="+", command=adicionar_parentesco, width=3).pack(side="left", padx=(0,5))
        ttk.Button(frame_ref, text="✕", command=lambda: frame_ref.destroy(), width=3).pack(side="left")
        
        # Armazenar referências
        frame_ref.entry_nome = entry_nome
        frame_ref.entry_tel = entry_tel
        frame_ref.combo_parentesco = combo_parentesco
    
    def _calcular_limite_credito(self):
        """Calcula limite de crédito baseado na renda"""
        try:
            from ui_utils import extrair_valor_numerico
            renda_valor = extrair_valor_numerico(self.entry_renda.get())
            if renda_valor > 0:
                limite = renda_valor * 0.30
                # Formatar para exibição
                limite_formatado = f"R$ {limite:,.2f}".replace(',', '.')
                self.entry_limite.delete(0, tk.END)
                self.entry_limite.insert(0, limite_formatado)
        except Exception:
            pass
    
    def _preencher_campos_edicao(self):
        """Preenche campos para edição"""
        if not self.cliente_edicao:
            return
            
        cliente = self.cliente_edicao
        
        # Dados pessoais
        self.entry_nome.insert(0, cliente.nome)
        self.entry_data_nasc.insert(0, cliente.data_nascimento)
        self.entry_cpf.insert(0, cliente.cpf)
        self.entry_identidade.insert(0, cliente.identidade)
        self.entry_email.insert(0, cliente.email)
        if cliente.estado_civil in self.estados_civis:
            self.combo_estado_civil.set(cliente.estado_civil)
        self.entry_profissao.insert(0, cliente.profissao)
        
        # Endereço
        self.text_endereco.insert("1.0", cliente.endereco)
        
        # Contatos
        self.entry_tel_residencial.insert(0, cliente.telefone_residencial)
        self.entry_tel_celular.insert(0, cliente.telefone_celular)
        self.entry_tel_comercial.insert(0, cliente.telefone_comercial)
        
        # Trabalho
        self.entry_onde_trabalha.insert(0, cliente.onde_trabalha)
        self.entry_tel_trabalho.insert(0, cliente.telefone_trabalho)
        
        # Financeiro (formatar valores para exibição)
        try:
            renda_valor = float(cliente.renda_mensal) if cliente.renda_mensal else 0
            if renda_valor > 0:
                renda_formatada = f"R$ {renda_valor:,.2f}".replace(',', '.')
                self.entry_renda.insert(0, renda_formatada)
        except (ValueError, TypeError):
            pass
            
        try:
            limite_valor = float(cliente.limite_credito) if cliente.limite_credito else 0
            if limite_valor > 0:
                limite_formatado = f"R$ {limite_valor:,.2f}".replace(',', '.')
                self.entry_limite.insert(0, limite_formatado)
        except (ValueError, TypeError):
            pass
        
        # Observações
        self.text_observacao.insert("1.0", cliente.observacao)
        # Definir loja selecionada
        if hasattr(cliente, 'loja_cadastro') and cliente.loja_cadastro:
            # Procurar pela loja na lista de lojas carregadas
            for loja_nome, loja_id in self.lojas:
                if cliente.loja_cadastro == loja_nome or str(cliente.loja_cadastro) == str(loja_id):
                    self.combo_loja.set(loja_nome)
                    break
    
    def _validar_campos(self):
        """Valida campos obrigatórios"""
        erros = []
        
        # Campos obrigatórios
        if not self.entry_nome.get().strip():
            erros.append("Nome completo é obrigatório")
        
        if not self.entry_data_nasc.get().strip():
            erros.append("Data de nascimento é obrigatória")
        elif not self._validar_data(self.entry_data_nasc.get()):
            erros.append("Data de nascimento inválida (dd/mm/aaaa)")
        
        if not self.entry_cpf.get().strip():
            erros.append("CPF é obrigatório")
        elif not self._validar_cpf(self.entry_cpf.get()):
            erros.append("CPF inválido")
        
        if not self.entry_identidade.get().strip():
            erros.append("Identidade (RG) é obrigatória")
        
        if not self.text_endereco.get("1.0", tk.END).strip():
            erros.append("Endereço é obrigatório")
        
        # Telefones obrigatórios
        if not self.entry_tel_residencial.get().strip():
            erros.append("Telefone residencial é obrigatório")
        
        if not self.entry_tel_celular.get().strip():
            erros.append("Telefone celular é obrigatório")
        
        if not self.entry_tel_comercial.get().strip():
            erros.append("Telefone comercial é obrigatório")
        
        # Email (se preenchido)
        email = self.entry_email.get().strip()
        if email and not self._validar_email(email):
            erros.append("Email inválido")
        
        return erros
    
    def _validar_data(self, data):
        """Valida formato de data"""
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    def _validar_cpf(self, cpf):
        """Valida CPF"""
        cpf = re.sub(r'[^0-9]', '', cpf)
        if len(cpf) != 11:
            return False
        
        # Verificar se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Validar dígitos verificadores
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        dv1 = 0 if resto < 2 else 11 - resto
        
        if int(cpf[9]) != dv1:
            return False
        
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        dv2 = 0 if resto < 2 else 11 - resto
        
        return int(cpf[10]) == dv2
    
    def _validar_email(self, email):
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _obter_dados_cliente(self):
        """Obtém dados do formulário"""
        # Telefones adicionais
        telefones_adicionais = []
        for frame_tel in self.frame_telefones_adicionais.winfo_children():
            if hasattr(frame_tel, 'combo_tipo'):
                tipo = frame_tel.combo_tipo.get()
                telefone = frame_tel.entry_tel.get()
                if telefone:
                    telefones_adicionais.append(f"{tipo}: {telefone}")
        
        # Referências
        referencias = []
        for frame_ref in self.frame_referencias.winfo_children():
            if hasattr(frame_ref, 'entry_nome'):
                nome = frame_ref.entry_nome.get()
                telefone = frame_ref.entry_tel.get()
                parentesco = frame_ref.combo_parentesco.get()
                if nome and telefone:
                    referencias.append({
                        "nome": nome,
                        "telefone": telefone,
                        "parentesco": parentesco
                    })
        
        # Renda e limite (usar nova função de extração)
        try:
            from ui_utils import extrair_valor_numerico
            renda = Decimal(str(extrair_valor_numerico(self.entry_renda.get())))
        except (InvalidOperation, ValueError):
            renda = Decimal('0')
        
        try:
            limite = Decimal(str(extrair_valor_numerico(self.entry_limite.get())))
        except (InvalidOperation, ValueError):
            limite = Decimal('0')
        
        return CadastroCliente(
            nome=self.entry_nome.get().strip(),
            data_nascimento=self.entry_data_nasc.get().strip(),
            cpf=self.entry_cpf.get().strip(),
            identidade=self.entry_identidade.get().strip(),
            email=self.entry_email.get().strip(),
            estado_civil=self.combo_estado_civil.get(),
            profissao=self.entry_profissao.get().strip(),
            endereco=self.text_endereco.get("1.0", tk.END).strip(),
            telefone_residencial=self.entry_tel_residencial.get().strip(),
            telefone_celular=self.entry_tel_celular.get().strip(),
            telefone_comercial=self.entry_tel_comercial.get().strip(),
            telefones_adicionais=telefones_adicionais,
            onde_trabalha=self.entry_onde_trabalha.get().strip(),
            telefone_trabalho=self.entry_tel_trabalho.get().strip(),
            renda_mensal=renda,
            limite_credito=limite,
            referencias=referencias,
            observacao=self.text_observacao.get("1.0", tk.END).strip(),
            loja_cadastro=self.combo_loja.get(),
            loja_id=self._obter_id_loja_selecionada(),
            id=self.cliente_edicao.id if self.cliente_edicao else ""
        )
    
    def _obter_id_loja_selecionada(self):
        """Obtém o ID da loja selecionada"""
        loja_selecionada = self.combo_loja.get()
        for loja_nome, loja_id in self.lojas:
            if loja_nome == loja_selecionada:
                return loja_id
        return None
    
    def _salvar_cliente(self):
        """Salva o cliente"""
        # Validar campos
        erros = self._validar_campos()
        if erros:
            messagebox.showerror("Erro de Validação", "\n".join(erros))
            return
        
        try:
            cliente = self._obter_dados_cliente()
            
            if self.is_edicao:
                self.gerenciador_dados.editar_cliente(self.indice_edicao, cliente)
                messagebox.showinfo("Sucesso", "Cliente editado com sucesso!")
            else:
                self.gerenciador_dados.adicionar_cliente(cliente)
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            
            self.janela.destroy()
            
        except Exception as e:
            logging.error(f"Erro ao salvar cliente: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar cliente: {e}")
    
    def _excluir_cliente(self):
        """Exclui o cliente"""
        if messagebox.askyesno("Confirmar Exclusão", 
                              f"Tem certeza que deseja excluir o cliente {self.cliente_edicao.nome}?"):
            try:
                self.gerenciador_dados.remover_cliente(self.indice_edicao)
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                self.janela.destroy()
            except Exception as e:
                logging.error(f"Erro ao excluir cliente: {e}")
                messagebox.showerror("Erro", f"Erro ao excluir cliente: {e}")

    def _upload_foto(self):
        """Upload de foto do cliente com centralização automática"""
        filepath = filedialog.askopenfilename(
            title="Selecione a foto do cliente",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("BMP", "*.bmp"),
                ("GIF", "*.gif")
            ]
        )
        if filepath:
            try:
                # Preparar diretório e nome do arquivo
                from pathlib import Path
                photos_dir = Path("client_photos")
                photos_dir.mkdir(exist_ok=True)
                
                # Usar CPF como nome se disponível, senão usar timestamp
                cpf = self.entry_cpf.get().strip()
                if cpf:
                    filename = f"{cpf}.png"  # Sempre PNG para qualidade
                else:
                    import time
                    filename = f"cliente_{int(time.time())}.png"
                
                dest_path = photos_dir / filename
                
                # Processar e centralizar foto antes de salvar
                if self._process_and_save_client_photo(filepath, dest_path):
                    # Exibir preview da foto processada
                    img = Image.open(dest_path)
                    img.thumbnail((100, 100))
                    self.photo_img = ImageTk.PhotoImage(img)
                    self.photo_label.configure(image=self.photo_img, text="")
                    self.foto_caminho = str(dest_path)
                    
                    messagebox.showinfo("Sucesso", "Foto do cliente centralizada e salva!")
                else:
                    messagebox.showerror("Erro", "Não foi possível processar a foto")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar foto: {e}")
    
    def _process_and_save_client_photo(self, source_path, dest_path, size=400):
        """Processa foto do cliente: centraliza, redimensiona e salva"""
        try:
            # Abrir imagem original
            img = Image.open(source_path).convert('RGBA')
            
            # Obter dimensões originais
            width, height = img.size
            
            # Calcular nova dimensão mantendo proporção
            if width > height:
                new_width = size
                new_height = int((height * size) / width)
            else:
                new_height = size
                new_width = int((width * size) / height)
            
            # Redimensionar com alta qualidade
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Criar imagem de fundo quadrada (transparente)
            final_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            
            # Centralizar imagem na nova imagem quadrada
            x = (size - new_width) // 2
            y = (size - new_height) // 2
            final_img.paste(img_resized, (x, y), img_resized)
            
            # Aplicar suavização nas bordas
            try:
                from PIL import ImageFilter
                # Suavizar ligeiramente para melhor qualidade
                final_img = final_img.filter(ImageFilter.SMOOTH_MORE)
            except:
                pass  # Se não conseguir aplicar filtro, continuar
            
            # Salvar como PNG para manter transparência
            final_img.save(dest_path, 'PNG', quality=95, optimize=True)
            
            print(f"📷 Foto de cliente processada: {dest_path}")
            print(f"   Original: {width}x{height} -> Final: {size}x{size} (centralizada)")
            
            return True
            
        except Exception as e:
            print(f"Erro ao processar foto do cliente: {e}")
            return False
    
    def _remover_foto(self):
        """Remove foto do cliente"""
        if messagebox.askyesno("Confirmar", "Deseja remover a foto do cliente?"):
            self.foto_caminho = None
            self.photo_label.configure(image="", text="Nenhuma foto selecionada")
            if hasattr(self, 'photo_img'):
                del self.photo_img

    def _abrir_contratos(self):
        """Abre janela de gestão de contratos do cliente"""
        if not self.is_edicao:
            messagebox.showwarning("Aviso", "Salve o cliente primeiro para ver os contratos!")
            return
        
        # Buscar nome do cliente atual
        nome_cliente = self.entry_nome.get().strip()
        if not nome_cliente:
            messagebox.showerror("Erro", "Nome do cliente é obrigatório!")
            return
        
        try:
            # Importar aqui para evitar import circular
            sys.path.append('src')
            from db import get_connection
            
            # Buscar ID do cliente
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cliente_full WHERE nome = ?", (nome_cliente,))
            cliente_data = cursor.fetchone()
            conn.close()
            
            if not cliente_data:
                messagebox.showerror("Erro", "Cliente não encontrado no banco de dados!")
                return
            
            cliente_id = cliente_data["id"]
            
            # Criar janela de contratos
            self._criar_janela_contratos(cliente_id, nome_cliente)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir contratos: {e}")
    
    def _criar_janela_contratos(self, cliente_id, nome_cliente):
        """Cria a janela de gestão de contratos"""
        janela_contratos = tk.Toplevel(self.janela)
        janela_contratos.title(f"Contratos - {nome_cliente}")
        janela_contratos.geometry("900x600")
        janela_contratos.resizable(True, True)
        
        # Centralizar janela
        janela_contratos.transient(self.janela)
        janela_contratos.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(janela_contratos)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, text=f"📋 Contratos de {nome_cliente}", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Notebook para separar contratos ativos e histórico
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Aba de contratos ativos
        frame_ativos = ttk.Frame(notebook)
        notebook.add(frame_ativos, text="📋 Contratos Ativos")
        
        # Aba de histórico
        frame_historico = ttk.Frame(notebook)
        notebook.add(frame_historico, text="📚 Histórico Completo")
        
        # Construir abas
        self._build_contratos_ativos(frame_ativos, cliente_id, nome_cliente)
        self._build_historico_contratos(frame_historico, cliente_id, nome_cliente)
        
        # Botão fechar
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(20, 0))
        ttk.Button(btn_frame, text="✅ Fechar", command=janela_contratos.destroy).pack(side="right")
    
    def _build_contratos_ativos(self, parent, cliente_id, nome_cliente):
        """Constrói a aba de contratos ativos"""
        try:
            from db import get_connection
            
            # Buscar contratos ativos
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cc.id, cc.data_venda, cu.nome as curso_nome, cc.valor_total,
                       cc.num_parcelas, cc.valor_parcela, cc.cashback_valor, cc.status
                FROM contrato_curso cc
                LEFT JOIN curso cu ON cc.curso_id = cu.id
                WHERE cc.cliente_id = ? AND cc.status = 'Ativo'
                ORDER BY cc.created_at DESC
            """, (cliente_id,))
            contratos_ativos = cursor.fetchall()
            conn.close()
            
            if not contratos_ativos:
                ttk.Label(parent, text="Nenhum contrato ativo encontrado.", 
                         font=("Arial", 12)).pack(expand=True)
                return
            
            # Para cada contrato ativo, criar um card
            for contrato in contratos_ativos:
                self._criar_card_contrato(parent, contrato, cliente_id, nome_cliente, ativo=True)
                
        except Exception as e:
            ttk.Label(parent, text=f"Erro ao carregar contratos: {e}", 
                     foreground="red").pack(expand=True)
    
    def _build_historico_contratos(self, parent, cliente_id, nome_cliente):
        """Constrói a aba de histórico de contratos"""
        try:
            from db import get_connection
            
            # Buscar todos os contratos
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cc.id, cc.data_venda, cu.nome as curso_nome, cc.valor_total,
                       cc.num_parcelas, cc.valor_parcela, cc.cashback_valor, cc.status
                FROM contrato_curso cc
                LEFT JOIN curso cu ON cc.curso_id = cu.id
                WHERE cc.cliente_id = ?
                ORDER BY cc.created_at DESC
            """, (cliente_id,))
            todos_contratos = cursor.fetchall()
            conn.close()
            
            if not todos_contratos:
                ttk.Label(parent, text="Nenhum contrato encontrado.", 
                         font=("Arial", 12)).pack(expand=True)
                return
            
            # Criar scrollable frame
            canvas = tk.Canvas(parent)
            scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Para cada contrato, criar um card
            for contrato in todos_contratos:
                self._criar_card_contrato(scrollable_frame, contrato, cliente_id, nome_cliente, ativo=False)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
                
        except Exception as e:
            ttk.Label(parent, text=f"Erro ao carregar histórico: {e}", 
                     foreground="red").pack(expand=True)
    
    def _criar_card_contrato(self, parent, contrato, cliente_id, nome_cliente, ativo=True):
        """Cria um card para exibir informações do contrato"""
        # Frame do card
        card_frame = ttk.LabelFrame(parent, text=f"Contrato #{contrato[0]} - {contrato[7]}")
        card_frame.pack(fill="x", pady=10, padx=10)
        
        # Informações do contrato
        info_frame = ttk.Frame(card_frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"📅 Data: {contrato[1]}").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(info_frame, text=f"📚 Curso: {contrato[2]}").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Label(info_frame, text=f"💰 Total: R$ {contrato[3]:.2f}".replace('.', ',')).grid(row=1, column=0, sticky="w", padx=5)
        ttk.Label(info_frame, text=f"📊 Parcelas: {contrato[4]}x R$ {contrato[5]:.2f}".replace('.', ',')).grid(row=1, column=1, sticky="w", padx=5)
        ttk.Label(info_frame, text=f"🎁 Cash: R$ {contrato[6]:.2f}".replace('.', ','), foreground="red").grid(row=2, column=0, sticky="w", padx=5)
        
        # Botões de ação (apenas para contratos ativos)
        if ativo and contrato[7] == 'Ativo':
            btn_frame = ttk.Frame(card_frame)
            btn_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            ttk.Button(btn_frame, text="📋 Ver Parcelas", 
                      command=lambda c=contrato: self._ver_parcelas_contrato(c, cliente_id, nome_cliente)).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="❌ Cancelar Contrato", 
                      command=lambda c=contrato: self._abrir_janela_cancelamento(c, cliente_id, nome_cliente)).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="🔄 Estorno", 
                      command=lambda c=contrato: self._abrir_janela_estorno(c, cliente_id, nome_cliente)).pack(side="left", padx=5)

    def _ver_parcelas_contrato(self, contrato, cliente_id, nome_cliente):
        """Abre janela para visualizar e pagar parcelas do contrato"""
        janela_parcelas = tk.Toplevel(self.janela)
        janela_parcelas.title(f"Parcelas - Contrato #{contrato[0]}")
        janela_parcelas.geometry("800x600")
        janela_parcelas.resizable(True, True)
        
        # Centralizar janela
        janela_parcelas.transient(self.janela)
        janela_parcelas.grab_set()
        
        main_frame = ttk.Frame(janela_parcelas)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text=f"💳 Parcelas - Contrato #{contrato[0]} - {contrato[2]}", 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Informações do contrato
        info_frame = ttk.LabelFrame(main_frame, text="Informações do Contrato", padding=10)
        info_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(info_frame, text=f"Cliente: {nome_cliente}").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(info_frame, text=f"Curso: {contrato[2]}").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Label(info_frame, text=f"Valor Total: R$ {contrato[3]:.2f}".replace('.', ',')).grid(row=1, column=0, sticky="w", padx=5)
        ttk.Label(info_frame, text=f"Parcelas: {contrato[4]}x de R$ {contrato[5]:.2f}".replace('.', ',')).grid(row=1, column=1, sticky="w", padx=5)
        
        # Lista de parcelas
        parcelas_frame = ttk.LabelFrame(main_frame, text="Parcelas", padding=10)
        parcelas_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        columns = ("Nº", "Vencimento", "Valor", "Status", "Data Pagamento")
        tree = ttk.Treeview(parcelas_frame, columns=columns, show="headings", height=12)
        
        # Configurar colunas
        tree.heading("Nº", text="Nº")
        tree.heading("Vencimento", text="Vencimento")
        tree.heading("Valor", text="Valor")
        tree.heading("Status", text="Status")
        tree.heading("Data Pagamento", text="Data Pagamento")
        
        tree.column("Nº", width=50)
        tree.column("Vencimento", width=100)
        tree.column("Valor", width=120)
        tree.column("Status", width=100)
        tree.column("Data Pagamento", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parcelas_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        try:
            from db import get_connection
            
            # Carregar parcelas
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, numero_parcela, data_vencimento, valor, status, data_pagamento
                FROM parcela_contrato 
                WHERE contrato_id = ? 
                ORDER BY numero_parcela
            """, (contrato[0],))
            parcelas = cursor.fetchall()
            conn.close()
            
            for parcela in parcelas:
                valor_formatado = f"R$ {parcela[3]:.2f}".replace('.', ',')
                data_pag = parcela[5] if parcela[5] else "-"
                
                # Colorir linha baseado no status
                if parcela[4] == "Paga":
                    tags = ("paga",)
                elif parcela[4] == "Cancelada":
                    tags = ("cancelada",)
                else:
                    tags = ("pendente",)
                
                tree.insert("", "end", values=(
                    parcela[1], parcela[2], valor_formatado, parcela[4], data_pag
                ), tags=tags)
            
            # Configurar cores das tags
            tree.tag_configure("paga", background="#d4edda")
            tree.tag_configure("cancelada", background="#f8d7da")
            tree.tag_configure("pendente", background="#fff3cd")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar parcelas: {e}")
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Instruções
        instrucoes_label = ttk.Label(main_frame, 
                                   text="💡 Dica: Clique duas vezes em uma parcela PENDENTE para efetuar o pagamento", 
                                   foreground="blue")
        instrucoes_label.pack(pady=5)
        
        # Evento duplo clique para pagar parcela
        def pagar_parcela(event):
            selection = tree.selection()
            if not selection:
                return
            
            item = tree.item(selection[0])
            parcela_numero = item['values'][0]
            status = item['values'][3]
            valor_original = item['values'][2]
            
            if status == "Paga":
                messagebox.showinfo("Info", "Esta parcela já foi paga!")
                return
            elif status == "Cancelada":
                messagebox.showinfo("Info", "Esta parcela foi cancelada!")
                return
            
            # Abrir janela para editar valor do pagamento
            self._abrir_janela_pagamento_parcela(contrato, parcela_numero, valor_original, nome_cliente, janela_parcelas)
        
        tree.bind("<Double-1>", pagar_parcela)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        ttk.Button(btn_frame, text="🔄 Atualizar", 
                  command=lambda: self._atualizar_parcelas(tree, contrato[0])).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✅ Fechar", 
                  command=janela_parcelas.destroy).pack(side="right")
    
    def _atualizar_parcelas(self, tree, contrato_id):
        """Atualiza a lista de parcelas"""
        try:
            from db import get_connection
            
            # Limpar árvore
            for item in tree.get_children():
                tree.delete(item)
            
            # Recarregar parcelas
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, numero_parcela, data_vencimento, valor, status, data_pagamento
                FROM parcela_contrato 
                WHERE contrato_id = ? 
                ORDER BY numero_parcela
            """, (contrato_id,))
            parcelas = cursor.fetchall()
            conn.close()
            
            for parcela in parcelas:
                valor_formatado = f"R$ {parcela[3]:.2f}".replace('.', ',')
                data_pag = parcela[5] if parcela[5] else "-"
                
                # Colorir linha baseado no status
                if parcela[4] == "Paga":
                    tags = ("paga",)
                elif parcela[4] == "Cancelada":
                    tags = ("cancelada",)
                else:
                    tags = ("pendente",)
                
                tree.insert("", "end", values=(
                    parcela[1], parcela[2], valor_formatado, parcela[4], data_pag
                ), tags=tags)
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar parcelas: {e}")
    
    def _abrir_janela_pagamento_parcela(self, contrato, parcela_numero, valor_original, nome_cliente, janela_parcelas):
        """Abre janela para editar valor do pagamento da parcela"""
        janela_pagamento = tk.Toplevel(self.janela)
        janela_pagamento.title(f"Pagamento Parcela #{parcela_numero}")
        janela_pagamento.geometry("500x650")
        janela_pagamento.resizable(False, False)
        
        # Centralizar janela
        janela_pagamento.transient(janela_parcelas)
        janela_pagamento.grab_set()
        
        main_frame = ttk.Frame(janela_pagamento)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text=f"💳 Pagamento da Parcela #{parcela_numero}", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Informações da parcela
        info_frame = ttk.LabelFrame(main_frame, text="Informações da Parcela", padding=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(info_frame, text=f"Cliente: {nome_cliente}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Contrato: #{contrato[0]} - {contrato[2]}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Parcela: {parcela_numero} de {contrato[4]}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Valor original: {valor_original}").pack(anchor="w")
        
        # Frame para edição do valor
        valor_frame = ttk.LabelFrame(main_frame, text="Valor do Pagamento", padding=10)
        valor_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(valor_frame, text="Valor a ser pago:").pack(anchor="w")
        entry_valor = ttk.Entry(valor_frame, width=20, font=("Arial", 12))
        entry_valor.pack(fill="x", pady=5)
        
        # Inserir valor original diretamente
        entry_valor.insert(0, valor_original)
        
        # Observações
        obs_frame = ttk.LabelFrame(main_frame, text="Observações (Opcional)", padding=10)
        obs_frame.pack(fill="x", pady=(0, 20))
        
        text_obs = tk.Text(obs_frame, height=3, width=50)
        text_obs.pack(fill="x")
        
        # Função para confirmar pagamento
        def confirmar_pagamento():
            try:
                from ui_utils import extrair_valor_numerico
                valor_pago = extrair_valor_numerico(entry_valor.get())
                if valor_pago <= 0:
                    messagebox.showerror("Erro", "Valor deve ser maior que zero!")
                    return
                
                observacoes = text_obs.get("1.0", tk.END).strip()
                
                confirmacao = f"🔔 EFETIVAR PAGAMENTO DA PARCELA?\n\n"
                confirmacao += f"Cliente: {nome_cliente}\n"
                confirmacao += f"Parcela: {parcela_numero}\n"
                confirmacao += f"Valor original: {valor_original}\n"
                confirmacao += f"Valor a receber: R$ {valor_pago:.2f}\n\n"
                confirmacao += f"✅ Esta operação será registrada no caixa\n"
                confirmacao += f"🔄 Pode ser estornada se necessário"
                
                if messagebox.askyesno("💰 Efetivar Pagamento", confirmacao):
                    
                    janela_pagamento.destroy()
                    self._processar_pagamento_parcela_editavel(contrato, parcela_numero, valor_pago, 
                                                             observacoes, nome_cliente, janela_parcelas)
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro no valor: {e}")
        
        # Botões - SEMPRE VISÍVEIS
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(20, 0))
        
        # Botão Cancelar
        btn_cancelar = tk.Button(btn_frame, text="❌ Cancelar", command=janela_pagamento.destroy,
                                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"))
        btn_cancelar.pack(side="top", fill="x", pady=2)
        
        # Botão Efetivar - PRINCIPAL
        btn_efetivar = tk.Button(btn_frame, text="EFETIVAR PAGAMENTO", command=confirmar_pagamento,
                                 bg="#2ecc71", fg="white", font=("Arial", 10, "bold"))
        btn_efetivar.pack(side="top", fill="x", pady=2)
    
    def _processar_pagamento_parcela_editavel(self, contrato, parcela_numero, valor_pago, observacoes, nome_cliente, janela_parcelas):
        """Processa o pagamento de uma parcela com valor editável"""
        try:
            from db import get_connection
            from datetime import datetime
            import uuid
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Buscar dados da parcela
            cursor.execute("""
                SELECT id, valor FROM parcela_contrato 
                WHERE contrato_id = ? AND numero_parcela = ? AND status = 'Pendente'
            """, (contrato[0], parcela_numero))
            parcela_data = cursor.fetchone()
            
            if not parcela_data:
                messagebox.showerror("Erro", "Parcela não encontrada ou já foi paga!")
                conn.close()
                return
            
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            valor_original = parcela_data[1]
            transacao_id = str(uuid.uuid4())[:8]  # ID único para estorno
            
            # 1. Marcar parcela como paga
            cursor.execute("""
                UPDATE parcela_contrato 
                SET status = 'Paga', data_pagamento = ?, valor = ? 
                WHERE id = ?
            """, (data_hoje, valor_pago, parcela_data[0]))
            
            # 2. Registrar histórico para possível estorno
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historico_transacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transacao_id TEXT UNIQUE NOT NULL,
                    tipo TEXT NOT NULL,
                    contrato_id INTEGER,
                    parcela_id INTEGER,
                    valor_original REAL,
                    valor_transacao REAL,
                    status_anterior TEXT,
                    status_novo TEXT,
                    data_transacao TEXT,
                    observacoes TEXT,
                    pode_estornar INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                INSERT INTO historico_transacoes 
                (transacao_id, tipo, contrato_id, parcela_id, valor_original, valor_transacao, 
                 status_anterior, status_novo, data_transacao, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (transacao_id, "PAGAMENTO_PARCELA", contrato[0], parcela_data[0], 
                  valor_original, valor_pago, "Pendente", "Paga", data_hoje, observacoes))
            
            # 3. Lançar como receita
            try:
                cursor.execute("""
                    INSERT INTO lancamento_receita (data, tipo_receita, descricao, valor, status, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (data_hoje, "Vendas de Cursos", 
                      f"Pagamento Parcela {parcela_numero}/{contrato[4]} - {contrato[2]} - {nome_cliente} [ID: {transacao_id}]", 
                      valor_pago, "Recebido", f"Valor original: R$ {valor_original:.2f}. {observacoes}"))
            except Exception:
                print(f"💰 Receita registrada: R$ {valor_pago:.2f} - Parcela {parcela_numero} - {nome_cliente}")
            
            # 4. Verificar se todas as parcelas foram pagas
            cursor.execute("""
                SELECT COUNT(*) as total, 
                       COUNT(CASE WHEN status = 'Paga' THEN 1 END) as pagas,
                       COUNT(CASE WHEN status = 'Cancelada' THEN 1 END) as canceladas
                FROM parcela_contrato WHERE contrato_id = ?
            """, (contrato[0],))
            parcelas_info = cursor.fetchone()
            
            total_parcelas = parcelas_info[0]
            parcelas_pagas = parcelas_info[1]
            parcelas_canceladas = parcelas_info[2]
            
            # 5. Se todas as parcelas não canceladas foram pagas, finalizar contrato
            if parcelas_pagas + parcelas_canceladas == total_parcelas and parcelas_pagas > 0:
                cursor.execute("""
                    UPDATE contrato_curso 
                    SET status = 'Finalizado' 
                    WHERE id = ?
                """, (contrato[0],))
                
                try:
                    cursor.execute("""
                        UPDATE cashback_cliente 
                        SET status = 'Liberado', data_liberacao = ? 
                        WHERE contrato_id = ?
                    """, (data_hoje, contrato[0]))
                except Exception:
                    print(f"🎁 Cashback liberado: R$ {contrato[6]:.2f} - {nome_cliente}")
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Sucesso", 
                    f"✅ Parcela {parcela_numero} paga com sucesso!\n\n"
                    f"💰 Valor pago: R$ {valor_pago:.2f}\n"
                    f"🎉 CONTRATO FINALIZADO!\n"
                    f"🎁 Cashback de R$ {contrato[6]:.2f} foi liberado!\n\n"
                    f"🔄 ID da transação: {transacao_id}\n"
                    f"(Pode ser usado para estorno se necessário)")
            else:
                conn.commit()
                conn.close()
                
                parcelas_restantes = total_parcelas - parcelas_pagas - parcelas_canceladas
                messagebox.showinfo("Sucesso", 
                    f"✅ Parcela {parcela_numero} paga com sucesso!\n\n"
                    f"💰 Valor pago: R$ {valor_pago:.2f}\n"
                    f"📊 Restam {parcelas_restantes} parcelas pendentes.\n\n"
                    f"🔄 ID da transação: {transacao_id}\n"
                    f"(Pode ser usado para estorno se necessário)")
            
            # Fechar janela para atualizar
            janela_parcelas.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar pagamento: {e}")
            if 'conn' in locals():
                conn.close()
    
    def _processar_pagamento_parcela(self, contrato, parcela_numero, nome_cliente, janela_parcelas):
        """Processa o pagamento de uma parcela"""
        try:
            from db import get_connection
            from datetime import datetime
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Buscar dados da parcela
            cursor.execute("""
                SELECT id, valor FROM parcela_contrato 
                WHERE contrato_id = ? AND numero_parcela = ? AND status = 'Pendente'
            """, (contrato[0], parcela_numero))
            parcela_data = cursor.fetchone()
            
            if not parcela_data:
                messagebox.showerror("Erro", "Parcela não encontrada ou já foi paga!")
                conn.close()
                return
            
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            valor_parcela = parcela_data[1]
            
            # 1. Marcar parcela como paga
            cursor.execute("""
                UPDATE parcela_contrato 
                SET status = 'Paga', data_pagamento = ? 
                WHERE id = ?
            """, (data_hoje, parcela_data[0]))
            
            # 2. Lançar como receita (verificar se tabela existe)
            try:
                cursor.execute("""
                    INSERT INTO lancamento_receita (data, tipo_receita, descricao, valor, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (data_hoje, "Vendas de Cursos", 
                      f"Pagamento Parcela {parcela_numero}/{contrato[4]} - {contrato[2]} - {nome_cliente}", 
                      valor_parcela, "Recebido"))
            except Exception:
                # Se não existir tabela lancamento_receita, criar um registro simples
                print(f"💰 Receita registrada: R$ {valor_parcela:.2f} - Parcela {parcela_numero} - {nome_cliente}")
            
            # 3. Verificar se todas as parcelas foram pagas
            cursor.execute("""
                SELECT COUNT(*) as total, 
                       COUNT(CASE WHEN status = 'Paga' THEN 1 END) as pagas,
                       COUNT(CASE WHEN status = 'Cancelada' THEN 1 END) as canceladas
                FROM parcela_contrato WHERE contrato_id = ?
            """, (contrato[0],))
            parcelas_info = cursor.fetchone()
            
            total_parcelas = parcelas_info[0]
            parcelas_pagas = parcelas_info[1]
            parcelas_canceladas = parcelas_info[2]
            
            # 4. Se todas as parcelas não canceladas foram pagas, finalizar contrato e liberar cashback
            if parcelas_pagas + parcelas_canceladas == total_parcelas and parcelas_pagas > 0:
                # Finalizar contrato
                cursor.execute("""
                    UPDATE contrato_curso 
                    SET status = 'Finalizado' 
                    WHERE id = ?
                """, (contrato[0],))
                
                # Liberar cashback
                try:
                    cursor.execute("""
                        UPDATE cashback_cliente 
                        SET status = 'Liberado', data_liberacao = ? 
                        WHERE contrato_id = ?
                    """, (data_hoje, contrato[0]))
                except Exception:
                    print(f"🎁 Cashback liberado: R$ {contrato[6]:.2f} - {nome_cliente}")
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Sucesso", 
                    f"✅ Parcela {parcela_numero} paga com sucesso!\n\n"
                    f"🎉 CONTRATO FINALIZADO!\n"
                    f"Todas as parcelas foram pagas.\n\n"
                    f"🎁 Cashback de R$ {contrato[6]:.2f} foi liberado!")
            else:
                conn.commit()
                conn.close()
                
                parcelas_restantes = total_parcelas - parcelas_pagas - parcelas_canceladas
                messagebox.showinfo("Sucesso", 
                    f"✅ Parcela {parcela_numero} paga com sucesso!\n\n"
                    f"💰 Valor: R$ {valor_parcela:.2f}\n"
                    f"📊 Restam {parcelas_restantes} parcelas pendentes.")
            
            # Fechar janela para atualizar
            janela_parcelas.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar pagamento: {e}")
            if 'conn' in locals():
                conn.close()
    
    def _cancelar_contrato(self, contrato, cliente_id, nome_cliente):
        """Cancela um contrato e libera o cashback"""
        # Verificar quantas parcelas já foram pagas
        try:
            from db import get_connection
            from datetime import datetime
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Buscar status das parcelas
            cursor.execute("""
                SELECT COUNT(*) as total, 
                       COUNT(CASE WHEN status = 'Paga' THEN 1 END) as pagas,
                       SUM(CASE WHEN status = 'Paga' THEN valor ELSE 0 END) as valor_pago
                FROM parcela_contrato WHERE contrato_id = ?
            """, (contrato[0],))
            parcelas_info = cursor.fetchone()
            conn.close()
            
            total_parcelas = parcelas_info[0]
            parcelas_pagas = parcelas_info[1]
            valor_pago = parcelas_info[2] or 0
            
            # Confirmar cancelamento
            confirmacao = messagebox.askyesno("Confirmar Cancelamento", 
                                            f"⚠️ CANCELAMENTO DE CONTRATO\n\n"
                                            f"Contrato: #{contrato[0]}\n"
                                            f"Cliente: {nome_cliente}\n"
                                            f"Curso: {contrato[2]}\n\n"
                                            f"📊 Situação atual:\n"
                                            f"• Total de parcelas: {total_parcelas}\n"
                                            f"• Parcelas pagas: {parcelas_pagas}\n"
                                            f"• Valor já pago: R$ {valor_pago:.2f}\n\n"
                                            f"🎁 Cashback a liberar: R$ {contrato[6]:.2f}\n\n"
                                            f"Deseja realmente CANCELAR este contrato?")
            
            if not confirmacao:
                return
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar contrato: {e}")
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            
            # 1. Cancelar contrato
            cursor.execute("""
                UPDATE contrato_curso 
                SET status = 'Cancelado' 
                WHERE id = ?
            """, (contrato[0],))
            
            # 2. Cancelar parcelas pendentes
            cursor.execute("""
                UPDATE parcela_contrato 
                SET status = 'Cancelada' 
                WHERE contrato_id = ? AND status = 'Pendente'
            """, (contrato[0],))
            
            # 3. Liberar cashback
            try:
                cursor.execute("""
                    UPDATE cashback_cliente 
                    SET status = 'Liberado', data_liberacao = ? 
                    WHERE contrato_id = ?
                """, (data_hoje, contrato[0]))
            except Exception:
                print(f"🎁 Cashback liberado por cancelamento: R$ {contrato[6]:.2f} - {nome_cliente}")
            
            # 4. Calcular valor pendente e registrar movimentações financeiras
            valor_total_contrato = contrato[3]  # valor_total do contrato
            valor_pendente = valor_total_contrato - valor_pago
            
            # Registrar o cancelamento com detalhes financeiros
            try:
                # Se houver valor pendente, registrar como receita perdida
                if valor_pendente > 0:
                    cursor.execute("""
                        INSERT INTO lancamento_receita (data, tipo_receita, descricao, valor, status)
                        VALUES (?, ?, ?, ?, ?)
                    """, (data_hoje, "Cancelamentos", 
                          f"Cancelamento Contrato #{contrato[0]} - {contrato[2]} - {nome_cliente} - Receita perdida", 
                          -valor_pendente, "Cancelado"))
                
                # Registrar o valor já recebido como confirmado
                if valor_pago > 0:
                    cursor.execute("""
                        INSERT INTO lancamento_receita (data, tipo_receita, descricao, valor, status)
                        VALUES (?, ?, ?, ?, ?)
                    """, (data_hoje, "Cancelamentos", 
                          f"Cancelamento Contrato #{contrato[0]} - {contrato[2]} - {nome_cliente} - Valor já recebido (mantido)", 
                          valor_pago, "Recebido"))
                
                # Não lança despesa; apenas marcar cashback como liberado
                if contrato[6] > 0:  # cashback_valor
                    cursor.execute("""
                        INSERT INTO lancamento_despesa (data, tipo_despesa, descricao, valor, status)
                        VALUES (?, ?, ?, ?, ?)
                    """, (data_hoje, "Cashback", 
                          f"Liberação Cashback - Cancelamento Contrato #{contrato[0]} - {nome_cliente}", 
                          contrato[6], "Liberado"))
                    
            except Exception as e:
                print(f"📝 Erro ao registrar movimentações: {e}")
                # Registrar pelo menos o cancelamento básico
                print(f"📝 Cancelamento registrado: Contrato #{contrato[0]} - {nome_cliente}")
                print(f"💰 Valor pago mantido: R$ {valor_pago:.2f}")
                print(f"💸 Receita perdida: R$ {valor_pendente:.2f}")
                print(f"🎁 Cashback liberado: R$ {contrato[6]:.2f}")
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Cancelamento Realizado", 
                f"✅ Contrato #{contrato[0]} cancelado com sucesso!\n\n"
                f"📊 RESUMO FINANCEIRO:\n"
                f"• Valor total do contrato: R$ {valor_total_contrato:.2f}\n"
                f"• Valor já recebido: R$ {valor_pago:.2f} (mantido)\n"
                f"• Receita perdida: R$ {valor_pendente:.2f}\n"
                f"• Cashback liberado: R$ {contrato[6]:.2f}\n\n"
                f"📋 Parcelas:\n"
                f"• Pagas: {parcelas_pagas} (mantidas no caixa)\n"
                f"• Pendentes: {total_parcelas - parcelas_pagas} (canceladas)\n\n"
                f"💰 Lançamentos registrados no sistema!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cancelar contrato: {e}")
            if 'conn' in locals():
                conn.close()

    def _abrir_janela_cancelamento(self, contrato, cliente_id, nome_cliente):
        """Abre janela para cancelamento com valores editáveis"""
        try:
            from db import get_connection
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Buscar status das parcelas
            cursor.execute("""
                SELECT COUNT(*) as total, 
                       COUNT(CASE WHEN status = 'Paga' THEN 1 END) as pagas,
                       SUM(CASE WHEN status = 'Paga' THEN valor ELSE 0 END) as valor_pago
                FROM parcela_contrato WHERE contrato_id = ?
            """, (contrato[0],))
            parcelas_info = cursor.fetchone()
            conn.close()
            
            total_parcelas = parcelas_info[0]
            parcelas_pagas = parcelas_info[1]
            valor_pago = parcelas_info[2] or 0
            valor_total_contrato = contrato[3]
            valor_pendente = valor_total_contrato - valor_pago
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar contrato: {e}")
            return
        
        # Criar janela de cancelamento
        janela_cancelamento = tk.Toplevel(self.janela)
        janela_cancelamento.title(f"Cancelamento - Contrato #{contrato[0]}")
        janela_cancelamento.geometry("600x650")
        janela_cancelamento.resizable(False, False)
        
        # Centralizar janela
        janela_cancelamento.transient(self.janela)
        janela_cancelamento.grab_set()
        
        main_frame = ttk.Frame(janela_cancelamento)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text=f"⚠️ Cancelamento do Contrato #{contrato[0]}", 
                               font=("Arial", 14, "bold"), foreground="red")
        title_label.pack(pady=(0, 20))
        
        # Informações do contrato
        info_frame = ttk.LabelFrame(main_frame, text="Informações do Contrato", padding=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(info_frame, text=f"Cliente: {nome_cliente}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Curso: {contrato[2]}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Valor total: R$ {valor_total_contrato:.2f}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Parcelas: {total_parcelas} ({parcelas_pagas} pagas)").pack(anchor="w")
        ttk.Label(info_frame, text=f"Valor já recebido: R$ {valor_pago:.2f}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Receita pendente: R$ {valor_pendente:.2f}").pack(anchor="w")
        
        # Valores editáveis
        valores_frame = ttk.LabelFrame(main_frame, text="Ajustar Valores do Cancelamento", padding=10)
        valores_frame.pack(fill="x", pady=(0, 20))
        
        # Receita perdida
        ttk.Label(valores_frame, text="Receita perdida (negativa):").pack(anchor="w")
        entry_receita_perdida = ttk.Entry(valores_frame, width=20, font=("Arial", 12))
        entry_receita_perdida.pack(fill="x", pady=5)
        entry_receita_perdida.insert(0, f"R$ {valor_pendente:.2f}".replace('.', ','))
        
        # Cashback a liberar
        ttk.Label(valores_frame, text="Cashback a liberar:").pack(anchor="w", pady=(10, 0))
        entry_cashback = ttk.Entry(valores_frame, width=20, font=("Arial", 12))
        entry_cashback.pack(fill="x", pady=5)
        entry_cashback.insert(0, f"R$ {contrato[6]:.2f}".replace('.', ','))
        
        # Aplicar máscaras
        from ui_utils import aplicar_mascara_valor
        aplicar_mascara_valor(entry_receita_perdida)
        aplicar_mascara_valor(entry_cashback)
        
        # Observações
        obs_frame = ttk.LabelFrame(main_frame, text="Motivo do Cancelamento", padding=10)
        obs_frame.pack(fill="x", pady=(0, 20))
        
        text_obs = tk.Text(obs_frame, height=4, width=50)
        text_obs.pack(fill="x")
        
        # Função para confirmar cancelamento
        def confirmar_cancelamento():
            try:
                from ui_utils import extrair_valor_numerico
                
                receita_perdida = extrair_valor_numerico(entry_receita_perdida.get())
                cashback_liberar = extrair_valor_numerico(entry_cashback.get())
                motivo = text_obs.get("1.0", tk.END).strip()
                
                confirmacao = f"🔔 EFETIVAR CANCELAMENTO DO CONTRATO?\n\n"
                confirmacao += f"Cliente: {nome_cliente}\n"
                confirmacao += f"Contrato: #{contrato[0]} - {contrato[2]}\n\n"
                confirmacao += f"💰 Receita perdida: R$ {receita_perdida:.2f}\n"
                confirmacao += f"🎁 Cashback a liberar: R$ {cashback_liberar:.2f}\n"
                confirmacao += f"📝 Motivo: {motivo[:50]}...\n\n"
                confirmacao += f"⚠️ ATENÇÃO: Todas as parcelas pendentes serão canceladas!\n"
                confirmacao += f"✅ Movimentações serão registradas no caixa\n"
                confirmacao += f"🔄 Esta operação pode ser estornada se necessário"
                
                if messagebox.askyesno("💸 Efetivar Cancelamento", confirmacao):
                    
                    janela_cancelamento.destroy()
                    self._processar_cancelamento_editavel(contrato, cliente_id, nome_cliente, 
                                                        receita_perdida, cashback_liberar, motivo, 
                                                        valor_pago, total_parcelas, parcelas_pagas)
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro nos valores: {e}")
        
        # Botões - SEMPRE VISÍVEIS
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        # Botão Voltar
        btn_voltar = tk.Button(btn_frame, text="❌ Voltar", command=janela_cancelamento.destroy,
                              bg="#e74c3c", fg="white", font=("Arial", 10, "bold"))
        btn_voltar.pack(side="top", fill="x", pady=2)
        
        # Botão Efetivar Cancelamento - PRINCIPAL
        btn_efetivar = tk.Button(btn_frame, text="💸 EFETIVAR CANCELAMENTO", command=confirmar_cancelamento,
                                 bg="#2ecc71", fg="white", font=("Arial", 10, "bold"))
        btn_efetivar.pack(side="top", fill="x", pady=2)

    def _processar_cancelamento_editavel(self, contrato, cliente_id, nome_cliente, receita_perdida, cashback_liberar, motivo, valor_pago, total_parcelas, parcelas_pagas):
        """Processa cancelamento com valores editáveis"""
        try:
            from db import get_connection
            from datetime import datetime
            import uuid
            
            conn = get_connection()
            cursor = conn.cursor()
            
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            transacao_id = str(uuid.uuid4())[:8]
            
            # 1. Cancelar contrato
            cursor.execute("""
                UPDATE contrato_curso 
                SET status = 'Cancelado' 
                WHERE id = ?
            """, (contrato[0],))
            
            # 2. Cancelar parcelas pendentes
            cursor.execute("""
                UPDATE parcela_contrato 
                SET status = 'Cancelada' 
                WHERE contrato_id = ? AND status = 'Pendente'
            """, (contrato[0],))
            
            # 3. Registrar histórico para estorno
            cursor.execute("""
                INSERT INTO historico_transacoes 
                (transacao_id, tipo, contrato_id, valor_original, valor_transacao, 
                 status_anterior, status_novo, data_transacao, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (transacao_id, "CANCELAMENTO_CONTRATO", contrato[0], 
                  contrato[3], receita_perdida, "Ativo", "Cancelado", data_hoje, motivo))
            
            # 4. Lançamentos financeiros
            if receita_perdida > 0:
                cursor.execute("""
                    INSERT INTO lancamento_receita (data, tipo_receita, descricao, valor, status, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (data_hoje, "Cancelamentos", 
                      f"Cancelamento Contrato #{contrato[0]} - {contrato[2]} - {nome_cliente} - Receita perdida [ID: {transacao_id}]", 
                      receita_perdida, "Cancelado", motivo))
            
            if valor_pago > 0:
                cursor.execute("""
                    INSERT INTO lancamento_receita (data, tipo_receita, descricao, valor, status, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (data_hoje, "Cancelamentos", 
                      f"Cancelamento Contrato #{contrato[0]} - {contrato[2]} - {nome_cliente} - Valor mantido [ID: {transacao_id}]", 
                      valor_pago, "Recebido", f"Valor já recebido e mantido. {motivo}"))
            
            if cashback_liberar > 0:
                cursor.execute("""
                    INSERT INTO lancamento_despesa (data, tipo_despesa, descricao, valor, status, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (data_hoje, "Cashback", 
                      f"Liberação Cashback - Cancelamento Contrato #{contrato[0]} - {nome_cliente} [ID: {transacao_id}]", 
                      cashback_liberar, "Liberado", motivo))
            
            # 5. Liberar cashback
            try:
                cursor.execute("""
                    UPDATE cashback_cliente 
                    SET status = 'Liberado', data_liberacao = ? 
                    WHERE contrato_id = ?
                """, (data_hoje, contrato[0]))
            except Exception:
                pass
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Cancelamento Realizado", 
                f"✅ Contrato #{contrato[0]} cancelado com sucesso!\n\n"
                f"📊 RESUMO FINANCEIRO:\n"
                f"• Receita perdida: R$ {receita_perdida:.2f}\n"
                f"• Valor mantido: R$ {valor_pago:.2f}\n"
                f"• Cashback liberado: R$ {cashback_liberar:.2f}\n\n"
                f"📋 Parcelas:\n"
                f"• Pagas: {parcelas_pagas} (mantidas)\n"
                f"• Canceladas: {total_parcelas - parcelas_pagas}\n\n"
                f"🔄 ID da transação: {transacao_id}\n"
                f"(Pode ser usado para estorno se necessário)\n\n"
                f"💰 Lançamentos registrados no sistema!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar cancelamento: {e}")
            if 'conn' in locals():
                conn.close()

    def _abrir_janela_estorno(self, contrato, cliente_id, nome_cliente):
        """Abre janela para estorno de transações"""
        janela_estorno = tk.Toplevel(self.janela)
        janela_estorno.title(f"Estorno - Contrato #{contrato[0]}")
        janela_estorno.geometry("700x500")
        janela_estorno.resizable(True, True)
        
        # Centralizar janela
        janela_estorno.transient(self.janela)
        janela_estorno.grab_set()
        
        main_frame = ttk.Frame(janela_estorno)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text=f"🔄 Estorno de Transações - Contrato #{contrato[0]}", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Lista de transações
        columns = ("ID", "Tipo", "Data", "Valor", "Status", "Observações")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.column("ID", width=80)
        tree.column("Tipo", width=150)
        tree.column("Data", width=100)
        tree.column("Valor", width=100)
        tree.column("Status", width=80)
        tree.column("Observações", width=200)
        
        # Carregar transações
        try:
            from db import get_connection
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT transacao_id, tipo, data_transacao, valor_transacao, 
                       CASE WHEN pode_estornar = 1 THEN 'Pode estornar' ELSE 'Já estornado' END,
                       observacoes
                FROM historico_transacoes 
                WHERE contrato_id = ? 
                ORDER BY created_at DESC
            """, (contrato[0],))
            transacoes = cursor.fetchall()
            conn.close()
            
            for transacao in transacoes:
                tree.insert("", "end", values=transacao)
        
        except Exception as e:
            ttk.Label(main_frame, text=f"Erro ao carregar transações: {e}", 
                     foreground="red").pack()
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Instruções
        instrucoes_label = ttk.Label(main_frame, 
                                   text="💡 Dica: Clique duas vezes em uma transação para estornar", 
                                   foreground="blue")
        instrucoes_label.pack(pady=10)
        
        # Evento duplo clique para estornar
        def estornar_transacao(event):
            selection = tree.selection()
            if not selection:
                return
            
            item = tree.item(selection[0])
            transacao_id = item['values'][0]
            tipo = item['values'][1]
            valor = item['values'][3]
            status = item['values'][4]
            
            if status != "Pode estornar":
                messagebox.showinfo("Info", "Esta transação já foi estornada ou não pode ser estornada!")
                return
            
            if messagebox.askyesno("Confirmar Estorno", 
                                 f"Confirma o estorno da transação?\n\n"
                                 f"ID: {transacao_id}\n"
                                 f"Tipo: {tipo}\n"
                                 f"Valor: R$ {valor:.2f}\n\n"
                                 f"Esta operação irá reverter a transação original."):
                self._processar_estorno(transacao_id, contrato, nome_cliente, janela_estorno)
        
        tree.bind("<Double-1>", estornar_transacao)
        
        # Botão fechar
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(20, 0))
        ttk.Button(btn_frame, text="✅ Fechar", command=janela_estorno.destroy).pack(side="right")

    def _processar_estorno(self, transacao_id, contrato, nome_cliente, janela_estorno):
        """Processa o estorno de uma transação"""
        try:
            from db import get_connection
            from datetime import datetime
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Buscar dados da transação original
            cursor.execute("""
                SELECT * FROM historico_transacoes 
                WHERE transacao_id = ? AND pode_estornar = 1
            """, (transacao_id,))
            transacao = cursor.fetchone()
            
            if not transacao:
                messagebox.showerror("Erro", "Transação não encontrada ou já foi estornada!")
                conn.close()
                return
            
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            
            # Processar estorno baseado no tipo
            if transacao[2] == "PAGAMENTO_PARCELA":  # tipo
                # Reverter parcela para pendente
                cursor.execute("""
                    UPDATE parcela_contrato 
                    SET status = ?, data_pagamento = NULL, valor = ?
                    WHERE id = ?
                """, (transacao[7], transacao[5], transacao[4]))  # status_anterior, valor_original, parcela_id
                
                # Estornar receita
                cursor.execute("""
                    INSERT INTO lancamento_receita (data, tipo_receita, descricao, valor, status, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (data_hoje, "Estornos", 
                      f"ESTORNO - Pagamento Parcela - {nome_cliente} [Original: {transacao_id}]", 
                      -transacao[6], "Estornado", f"Estorno da transação {transacao_id}"))  # valor_transacao
                
            elif transacao[2] == "CANCELAMENTO_CONTRATO":  # tipo
                # Reverter contrato para ativo
                cursor.execute("""
                    UPDATE contrato_curso 
                    SET status = ? 
                    WHERE id = ?
                """, (transacao[7], transacao[3]))  # status_anterior, contrato_id
                
                # Reverter parcelas canceladas para pendente
                cursor.execute("""
                    UPDATE parcela_contrato 
                    SET status = 'Pendente' 
                    WHERE contrato_id = ? AND status = 'Cancelada'
                """, (transacao[3],))  # contrato_id
                
                # Estornar lançamentos
                cursor.execute("""
                    INSERT INTO lancamento_receita (data, tipo_receita, descricao, valor, status, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (data_hoje, "Estornos", 
                      f"ESTORNO - Cancelamento Contrato #{transacao[3]} - {nome_cliente} [Original: {transacao_id}]", 
                      transacao[6], "Estornado", f"Estorno da transação {transacao_id}"))
            
            # Marcar transação como estornada
            cursor.execute("""
                UPDATE historico_transacoes 
                SET pode_estornar = 0 
                WHERE transacao_id = ?
            """, (transacao_id,))
            
            # Registrar o estorno
            cursor.execute("""
                INSERT INTO historico_transacoes 
                (transacao_id, tipo, contrato_id, valor_transacao, status_anterior, status_novo, 
                 data_transacao, observacoes, pode_estornar)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (f"EST_{transacao_id}", f"ESTORNO_{transacao[2]}", transacao[3], 
                  transacao[6], transacao[8], transacao[7], data_hoje, 
                  f"Estorno da transação {transacao_id}", 0))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Estorno Realizado", 
                f"✅ Estorno processado com sucesso!\n\n"
                f"🔄 Transação original: {transacao_id}\n"
                f"📅 Data do estorno: {data_hoje}\n\n"
                f"O contrato e parcelas foram restaurados ao estado anterior.\n"
                f"Os lançamentos financeiros foram estornados.")
            
            # Fechar e atualizar
            janela_estorno.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar estorno: {e}")
            if 'conn' in locals():
                conn.close()


# Função para criar máscaras de entrada
def aplicar_mascara_telefone(entry):
    """Aplica máscara de telefone"""
    def formatar_telefone(event):
        texto = entry.get()
        # Remove caracteres não numéricos
        numeros = re.sub(r'[^0-9]', '', texto)
        
        if len(numeros) <= 10:
            # Telefone fixo: (11) 1234-5678
            if len(numeros) >= 2:
                numeros = f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:10]}"
        else:
            # Celular: (11) 99999-9999
            if len(numeros) >= 2:
                numeros = f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:11]}"
        
        entry.delete(0, tk.END)
        entry.insert(0, numeros)
    
    entry.bind('<KeyRelease>', formatar_telefone)

def aplicar_mascara_cpf(entry):
    """Aplica máscara de CPF"""
    def formatar_cpf(event):
        texto = entry.get()
        numeros = re.sub(r'[^0-9]', '', texto)
        
        if len(numeros) <= 11:
            if len(numeros) >= 4:
                numeros = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:11]}"
            elif len(numeros) >= 7:
                numeros = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}"
            elif len(numeros) >= 4:
                numeros = f"{numeros[:3]}.{numeros[3:6]}"
        
        entry.delete(0, tk.END)
        entry.insert(0, numeros)
    
    entry.bind('<KeyRelease>', formatar_cpf)

def aplicar_mascara_data(entry):
    """Aplica máscara de data (dd/mm/aaaa)"""
    def formatar_data(event):
        texto = entry.get()
        numeros = re.sub(r'[^0-9]', '', texto)
        
        if len(numeros) <= 8:
            if len(numeros) >= 3:
                numeros = f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:8]}"
            elif len(numeros) >= 3:
                numeros = f"{numeros[:2]}/{numeros[2:4]}"
        
        entry.delete(0, tk.END)
        entry.insert(0, numeros)
    
    entry.bind('<KeyRelease>', formatar_data)