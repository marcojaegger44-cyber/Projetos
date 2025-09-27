#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema CM - Integração de Relatórios ao Sistema Premium
Este módulo integra o sistema de relatórios ao sistema premium
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import logging
from datetime import datetime

# Garantir que os módulos no mesmo diretório possam ser importados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar módulo de relatórios
from interface_relatorios import InterfaceRelatorios

class IntegradorRelatorios:
    """Classe para integrar relatórios ao sistema premium"""
    
    def __init__(self, sistema_premium):
        """
        Inicializa o integrador de relatórios
        
        Args:
            sistema_premium: Instância do sistema premium
        """
        self.sistema_premium = sistema_premium
        self.gerenciador_dados = sistema_premium.gerenciador_dados
        
    def abrir_relatorio_vendas(self):
        """Abre a interface de relatórios de vendas"""
        try:
            # Verificar se o usuário tem permissão
            if not self.sistema_premium.verificar_permissao("relatorios"):
                messagebox.showwarning(
                    "Acesso Restrito", 
                    "Você não tem permissão para acessar os relatórios."
                )
                return
            
            # Abrir interface de relatórios de vendas
            relatorio = InterfaceRelatorios(
                self.sistema_premium.root,
                self.gerenciador_dados,
                tipo_relatorio="vendas"
            )
            
            # Registrar no log
            logging.info(f"Relatório de vendas aberto pelo usuário {self.sistema_premium.usuario_atual}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir relatório de vendas: {e}")
            logging.error(f"Erro ao abrir relatório de vendas: {e}", exc_info=True)
    
    def abrir_relatorio_clientes(self):
        """Abre a interface de relatórios de clientes"""
        try:
            # Verificar se o usuário tem permissão
            if not self.sistema_premium.verificar_permissao("relatorios"):
                messagebox.showwarning(
                    "Acesso Restrito", 
                    "Você não tem permissão para acessar os relatórios."
                )
                return
            
            # Abrir interface de relatórios de clientes
            relatorio = InterfaceRelatorios(
                self.sistema_premium.root,
                self.gerenciador_dados,
                tipo_relatorio="clientes"
            )
            
            # Registrar no log
            logging.info(f"Relatório de clientes aberto pelo usuário {self.sistema_premium.usuario_atual}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir relatório de clientes: {e}")
            logging.error(f"Erro ao abrir relatório de clientes: {e}", exc_info=True)
    
    def adicionar_menu_relatorios(self, menu_bar):
        """
        Adiciona o menu de relatórios à barra de menus do sistema
        
        Args:
            menu_bar: Barra de menus do sistema
        """
        # Criar menu de relatórios
        menu_relatorios = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Relatórios", menu=menu_relatorios)
        
        # Adicionar opções ao menu
        menu_relatorios.add_command(label="Relatório de Vendas", command=self.abrir_relatorio_vendas)
        menu_relatorios.add_command(label="Relatório de Clientes", command=self.abrir_relatorio_clientes)
        menu_relatorios.add_separator()
        menu_relatorios.add_command(label="Configurações de Relatórios", 
                                   command=lambda: messagebox.showinfo(
                                       "Configurações", 
                                       "Funcionalidade em implementação."
                                   ))
    
    def adicionar_botoes_dashboard(self, dashboard_frame):
        """
        Adiciona botões de relatórios ao dashboard do sistema
        
        Args:
            dashboard_frame: Frame do dashboard onde os botões serão adicionados
        """
        # Frame para botões de relatórios
        relatorios_frame = ttk.LabelFrame(dashboard_frame, text="Relatórios")
        relatorios_frame.pack(fill="x", padx=10, pady=5)
        
        # Botão para relatório de vendas
        btn_vendas = ttk.Button(
            relatorios_frame, 
            text="Relatório de Vendas", 
            command=self.abrir_relatorio_vendas
        )
        btn_vendas.pack(side="left", padx=5, pady=5)
        
        # Botão para relatório de clientes
        btn_clientes = ttk.Button(
            relatorios_frame, 
            text="Relatório de Clientes", 
            command=self.abrir_relatorio_clientes
        )
        btn_clientes.pack(side="left", padx=5, pady=5)


# Função para integrar ao sistema premium
def integrar_ao_sistema(sistema_premium):
    """
    Integra o módulo de relatórios ao sistema premium
    
    Args:
        sistema_premium: Instância do sistema premium
        
    Returns:
        IntegradorRelatorios: Instância do integrador de relatórios
    """
    integrador = IntegradorRelatorios(sistema_premium)
    
    # Adicionar menu à barra de menus
    if hasattr(sistema_premium, 'menu_bar'):
        integrador.adicionar_menu_relatorios(sistema_premium.menu_bar)
    
    # Adicionar botões ao dashboard
    if hasattr(sistema_premium, 'dashboard_frame'):
        integrador.adicionar_botoes_dashboard(sistema_premium.dashboard_frame)
    
    # Registrar no log
    logging.info("Módulo de relatórios integrado ao sistema premium")
    
    return integrador