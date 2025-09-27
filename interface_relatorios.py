#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema CM - Módulo de Relatórios
Interface para geração e visualização de relatórios
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import json
import logging
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import calendar
from typing import Dict, List, Any, Optional, Tuple
from decimal import Decimal

# Garantir que os módulos no mesmo diretório possam ser importados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class InterfaceRelatorios:
    """Interface para geração e visualização de relatórios"""
    
    def __init__(self, parent, gerenciador_dados, tipo_relatorio="vendas"):
        self.parent = parent
        self.gerenciador_dados = gerenciador_dados
        self.tipo_relatorio = tipo_relatorio  # "vendas" ou "clientes"
        
        # Criar janela
        self.janela = tk.Toplevel(parent)
        self.janela.title(f"Relatório de {tipo_relatorio.capitalize()} - Sistema CM")
        self.janela.geometry("1000x700")
        self.janela.minsize(900, 600)
        
        # Variáveis de controle
        self.var_periodo = tk.StringVar(value="mes")
        self.var_agrupamento = tk.StringVar(value="diario")
        self.var_tipo_grafico = tk.StringVar(value="barras")
        
        # Datas de filtro
        self.data_inicio = datetime.now().replace(day=1)  # Primeiro dia do mês atual
        self.data_fim = datetime.now()  # Hoje
        
        # Criar interface
        self._criar_interface()
        
        # Gerar relatório inicial
        self._gerar_relatorio()
    
    def _criar_interface(self):
        """Cria a interface da janela"""
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Frame superior - Filtros e ações
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Título
        ttk.Label(top_frame, text=f"Relatório de {self.tipo_relatorio.capitalize()}", 
                 font=("Arial", 14, "bold")).pack(side="left", padx=(0, 20))
        
        # Frame de filtros
        filtros_frame = ttk.LabelFrame(top_frame, text="Filtros")
        filtros_frame.pack(side="left", fill="x", expand=True)
        
        # Layout de filtros em grid
        filtro_grid = ttk.Frame(filtros_frame, padding=5)
        filtro_grid.pack(fill="x")
        
        # Período
        ttk.Label(filtro_grid, text="Período:").grid(row=0, column=0, padx=5, pady=5)
        
        periodos = [("Hoje", "hoje"), ("Esta Semana", "semana"), 
                   ("Este Mês", "mes"), ("Este Ano", "ano"), 
                   ("Personalizado", "personalizado")]
        
        periodo_frame = ttk.Frame(filtro_grid)
        periodo_frame.grid(row=0, column=1, padx=5, pady=5)
        
        for i, (texto, valor) in enumerate(periodos):
            ttk.Radiobutton(periodo_frame, text=texto, value=valor, 
                           variable=self.var_periodo, 
                           command=self._atualizar_periodo).pack(side="left", padx=5)
        
        # Datas (inicialmente ocultas, aparecem quando "Personalizado" é selecionado)
        self.datas_frame = ttk.Frame(filtro_grid)
        self.datas_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        
        ttk.Label(self.datas_frame, text="De:").grid(row=0, column=0, padx=5, pady=5)
        self.data_inicio_entry = ttk.Entry(self.datas_frame, width=12)
        self.data_inicio_entry.grid(row=0, column=1, padx=5, pady=5)
        self.data_inicio_entry.insert(0, self.data_inicio.strftime("%d/%m/%Y"))
        
        ttk.Label(self.datas_frame, text="Até:").grid(row=0, column=2, padx=5, pady=5)
        self.data_fim_entry = ttk.Entry(self.datas_frame, width=12)
        self.data_fim_entry.grid(row=0, column=3, padx=5, pady=5)
        self.data_fim_entry.insert(0, self.data_fim.strftime("%d/%m/%Y"))
        
        # Botão para aplicar datas
        ttk.Button(self.datas_frame, text="Aplicar", 
                  command=self._aplicar_datas_personalizadas).grid(row=0, column=4, padx=5, pady=5)
        
        # Ocultar frame de datas inicialmente
        self.datas_frame.grid_remove()
        
        # Agrupamento
        ttk.Label(filtro_grid, text="Agrupar por:").grid(row=0, column=2, padx=5, pady=5)
        
        agrupamentos = [("Diário", "diario"), ("Semanal", "semanal"), 
                       ("Mensal", "mensal"), ("Anual", "anual")]
        
        agrupamento_frame = ttk.Frame(filtro_grid)
        agrupamento_frame.grid(row=0, column=3, padx=5, pady=5)
        
        for i, (texto, valor) in enumerate(agrupamentos):
            ttk.Radiobutton(agrupamento_frame, text=texto, value=valor, 
                           variable=self.var_agrupamento).pack(side="left", padx=5)
        
        # Botão para gerar relatório
        ttk.Button(filtro_grid, text="Gerar Relatório", 
                  command=self._gerar_relatorio).grid(row=2, column=0, columnspan=4, padx=5, pady=10)
        
        # Frame de ações
        acoes_frame = ttk.Frame(top_frame)
        acoes_frame.pack(side="right", padx=(10, 0))
        
        # Tipo de gráfico
        ttk.Label(acoes_frame, text="Gráfico:").pack(side="left", padx=5)
        
        graficos = [("Barras", "barras"), ("Linhas", "linhas"), ("Pizza", "pizza")]
        
        for texto, valor in graficos:
            ttk.Radiobutton(acoes_frame, text=texto, value=valor, 
                           variable=self.var_tipo_grafico, 
                           command=self._atualizar_grafico).pack(side="left", padx=5)
        
        # Botão de exportação
        ttk.Button(acoes_frame, text="Exportar", 
                  command=lambda: self._exportar_dados()).pack(side="left", padx=5)
        
        # Frame central - Notebook com abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Aba de gráfico
        self.frame_grafico = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_grafico, text="Gráfico")
        
        # Aba de tabela
        self.frame_tabela = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_tabela, text="Tabela")
        
        # Aba de resumo
        self.frame_resumo = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_resumo, text="Resumo")
        
        # Frame inferior - Estatísticas e status
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill="x", pady=(10, 0))
        
        # Estatísticas
        self.lbl_estatisticas = ttk.Label(bottom_frame, text="")
        self.lbl_estatisticas.pack(side="left")
        
        # Status da operação
        self.lbl_status = ttk.Label(bottom_frame, text="")
        self.lbl_status.pack(side="right")
    
    def _atualizar_periodo(self):
        """Atualiza o período selecionado"""
        periodo = self.var_periodo.get()
        
        # Ocultar/mostrar frame de datas
        if periodo == "personalizado":
            self.datas_frame.grid()
        else:
            self.datas_frame.grid_remove()
            
            # Definir datas com base no período selecionado
            hoje = datetime.now()
            
            if periodo == "hoje":
                self.data_inicio = hoje
                self.data_fim = hoje
            elif periodo == "semana":
                # Segunda-feira desta semana
                self.data_inicio = hoje - timedelta(days=hoje.weekday())
                self.data_fim = hoje
            elif periodo == "mes":
                # Primeiro dia do mês atual
                self.data_inicio = hoje.replace(day=1)
                self.data_fim = hoje
            elif periodo == "ano":
                # Primeiro dia do ano atual
                self.data_inicio = hoje.replace(month=1, day=1)
                self.data_fim = hoje
            
            # Atualizar entradas de data
            self.data_inicio_entry.delete(0, tk.END)
            self.data_inicio_entry.insert(0, self.data_inicio.strftime("%d/%m/%Y"))
            
            self.data_fim_entry.delete(0, tk.END)
            self.data_fim_entry.insert(0, self.data_fim.strftime("%d/%m/%Y"))
            
            # Gerar relatório com novo período
            self._gerar_relatorio()
    
    def _aplicar_datas_personalizadas(self):
        """Aplica as datas personalizadas"""
        try:
            # Converter strings para objetos datetime
            data_inicio_str = self.data_inicio_entry.get()
            data_fim_str = self.data_fim_entry.get()
            
            self.data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
            self.data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
            
            # Verificar se a data inicial é anterior à final
            if self.data_inicio > self.data_fim:
                messagebox.showerror("Erro", "A data inicial deve ser anterior à data final!")
                return
            
            # Gerar relatório com novas datas
            self._gerar_relatorio()
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA.")
    
    def _gerar_relatorio(self):
        """Gera o relatório com base nos filtros selecionados"""
        try:
            # Obter dados conforme o tipo de relatório
            if self.tipo_relatorio == "vendas":
                dados = self._obter_dados_vendas()
            else:  # clientes
                dados = self._obter_dados_clientes()
            
            # Agrupar dados
            dados_agrupados = self._agrupar_dados(dados)
            
            # Atualizar visualizações
            self._atualizar_grafico(dados_agrupados)
            self._atualizar_tabela(dados_agrupados)
            self._atualizar_resumo(dados_agrupados)
            
            # Atualizar estatísticas
            self._atualizar_estatisticas(dados_agrupados)
            
            # Atualizar status
            periodo_str = f"{self.data_inicio.strftime('%d/%m/%Y')} a {self.data_fim.strftime('%d/%m/%Y')}"
            self.lbl_status.config(text=f"Período: {periodo_str} | Agrupamento: {self.var_agrupamento.get()}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
            logging.error(f"Erro ao gerar relatório: {e}", exc_info=True)
    
    def _obter_dados_vendas(self):
        """Obtém dados de vendas do período selecionado"""
        # Obter vendas do gerenciador de dados
        vendas = self.gerenciador_dados.dados.get('historico_vendas', [])
        
        # Filtrar por período
        dados_filtrados = []
        for venda in vendas:
            try:
                # Converter timestamp para datetime
                data_venda = datetime.strptime(venda.timestamp, "%Y-%m-%d %H:%M:%S")
                
                # Verificar se está no período
                if self.data_inicio.date() <= data_venda.date() <= self.data_fim.date():
                    dados_filtrados.append({
                        'data': data_venda,
                        'valor': float(venda.total),
                        'produto': venda.produto,
                        'quantidade': venda.quantidade,
                        'loja': venda.codigo_loja
                    })
            except (ValueError, AttributeError) as e:
                logging.warning(f"Erro ao processar venda: {e}")
        
        return dados_filtrados
    
    def _obter_dados_clientes(self):
        """Obtém dados de clientes do período selecionado"""
        # Para este exemplo, vamos simular dados de clientes
        # Em um sistema real, isso seria baseado em dados reais de cadastro/atividade
        
        # Obter clientes do gerenciador de dados
        clientes = self.gerenciador_dados.dados.get('cadastros', [])
        
        # Simular dados de atividade para cada cliente
        import random
        dados_filtrados = []
        
        for cliente in clientes:
            # Gerar uma data aleatória dentro do período para simular cadastro/atividade
            dias_periodo = (self.data_fim - self.data_inicio).days
            if dias_periodo <= 0:
                dias_periodo = 1
            
            dias_aleatorios = random.randint(0, dias_periodo)
            data_atividade = self.data_inicio + timedelta(days=dias_aleatorios)
            
            # Verificar se está no período (sempre estará neste caso, mas mantemos para consistência)
            if self.data_inicio.date() <= data_atividade.date() <= self.data_fim.date():
                dados_filtrados.append({
                    'data': data_atividade,
                    'valor': float(cliente.limite_credito) if hasattr(cliente, 'limite_credito') else 0,
                    'nome': cliente.nome,
                    'id': cliente.id,
                    'cidade': cliente.cidade
                })
        
        return dados_filtrados
    
    def _agrupar_dados(self, dados):
        """Agrupa os dados conforme selecionado"""
        agrupamento = self.var_agrupamento.get()
        dados_agrupados = {}
        
        for item in dados:
            data = item['data']
            
            # Determinar chave de agrupamento
            if agrupamento == "diario":
                chave = data.strftime("%d/%m/%Y")
            elif agrupamento == "semanal":
                # Número da semana no ano
                semana = data.isocalendar()[1]
                chave = f"Semana {semana}/{data.year}"
            elif agrupamento == "mensal":
                chave = data.strftime("%m/%Y")
            else:  # anual
                chave = str(data.year)
            
            # Inicializar grupo se não existir
            if chave not in dados_agrupados:
                dados_agrupados[chave] = {
                    'valor_total': 0,
                    'quantidade': 0,
                    'itens': []
                }
            
            # Adicionar dados ao grupo
            dados_agrupados[chave]['valor_total'] += item['valor']
            dados_agrupados[chave]['quantidade'] += 1
            dados_agrupados[chave]['itens'].append(item)
        
        # Ordenar por chave (data)
        return dict(sorted(dados_agrupados.items()))
    
    def _atualizar_grafico(self, dados_agrupados=None):
        """Atualiza o gráfico com os dados"""
        if dados_agrupados is None:
            # Se não recebeu dados, tenta gerar o relatório novamente
            self._gerar_relatorio()
            return
        
        # Limpar frame do gráfico
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
        
        # Verificar se há dados para mostrar
        if not dados_agrupados:
            ttk.Label(self.frame_grafico, text="Sem dados para exibir no período selecionado").pack(pady=20)
            return
        
        # Criar figura do matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Preparar dados
        labels = list(dados_agrupados.keys())
        valores = [dados['valor_total'] for dados in dados_agrupados.values()]
        
        # Tipo de gráfico
        tipo_grafico = self.var_tipo_grafico.get()
        
        if tipo_grafico == "barras":
            ax.bar(labels, valores)
            plt.xticks(rotation=45)
            
        elif tipo_grafico == "linhas":
            ax.plot(labels, valores, marker='o')
            plt.xticks(rotation=45)
            
        elif tipo_grafico == "pizza":
            # Para gráfico de pizza, limitamos a 10 itens para legibilidade
            if len(labels) > 10:
                # Pegar os 9 maiores valores e agrupar o resto
                indices_ordenados = sorted(range(len(valores)), key=lambda i: valores[i], reverse=True)
                top_indices = indices_ordenados[:9]
                outros_indices = indices_ordenados[9:]
                
                labels_top = [labels[i] for i in top_indices]
                valores_top = [valores[i] for i in top_indices]
                
                # Adicionar "Outros"
                if outros_indices:
                    labels_top.append("Outros")
                    valores_top.append(sum(valores[i] for i in outros_indices))
                
                labels = labels_top
                valores = valores_top
            
            ax.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Título e labels
        titulo = f"Relatório de {self.tipo_relatorio.capitalize()} - {self.var_agrupamento.get().capitalize()}"
        ax.set_title(titulo)
        
        if tipo_grafico != "pizza":
            if self.tipo_relatorio == "vendas":
                ax.set_ylabel("Valor Total (R$)")
            else:
                ax.set_ylabel("Valor (R$)")
            
            ax.set_xlabel("Período")
        
        # Ajustar layout
        plt.tight_layout()
        
        # Criar canvas do Matplotlib
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _atualizar_tabela(self, dados_agrupados):
        """Atualiza a tabela com os dados"""
        # Limpar frame da tabela
        for widget in self.frame_tabela.winfo_children():
            widget.destroy()
        
        # Verificar se há dados para mostrar
        if not dados_agrupados:
            ttk.Label(self.frame_tabela, text="Sem dados para exibir no período selecionado").pack(pady=20)
            return
        
        # Criar tabela
        colunas = ("Período", "Quantidade", "Valor Total", "Ticket Médio")
        
        # Frame para a tabela com scrollbar
        table_frame = ttk.Frame(self.frame_tabela)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar Treeview
        self.tree = ttk.Treeview(table_frame, columns=colunas, show="headings")
        
        # Configurar cabeçalhos
        for col in colunas:
            self.tree.heading(col, text=col)
            if col == "Período":
                self.tree.column(col, width=150, anchor="w")
            else:
                self.tree.column(col, width=100, anchor="e")
        
        # Adicionar dados à tabela
        for periodo, dados in dados_agrupados.items():
            valor_total = dados['valor_total']
            quantidade = dados['quantidade']
            ticket_medio = valor_total / quantidade if quantidade > 0 else 0
            
            self.tree.insert("", "end", values=(
                periodo,
                quantidade,
                f"R$ {valor_total:.2f}".replace('.', ','),
                f"R$ {ticket_medio:.2f}".replace('.', ',')
            ))
        
        # Scrollbars
        scrolly = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollx = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        # Layout
        scrolly.pack(side="right", fill="y")
        scrollx.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)
    
    def _atualizar_resumo(self, dados_agrupados):
        """Atualiza a aba de resumo com estatísticas e gráficos adicionais"""
        # Limpar frame do resumo
        for widget in self.frame_resumo.winfo_children():
            widget.destroy()
        
        # Verificar se há dados para mostrar
        if not dados_agrupados:
            ttk.Label(self.frame_resumo, text="Sem dados para exibir no período selecionado").pack(pady=20)
            return
        
        # Calcular estatísticas
        total_registros = sum(dados['quantidade'] for dados in dados_agrupados.values())
        valor_total = sum(dados['valor_total'] for dados in dados_agrupados.values())
        ticket_medio = valor_total / total_registros if total_registros > 0 else 0
        
        # Encontrar maior e menor valor
        if dados_agrupados:
            maior_valor = max(dados['valor_total'] for dados in dados_agrupados.values())
            menor_valor = min(dados['valor_total'] for dados in dados_agrupados.values())
            
            # Períodos correspondentes
            maior_periodo = next(periodo for periodo, dados in dados_agrupados.items() if dados['valor_total'] == maior_valor)
            menor_periodo = next(periodo for periodo, dados in dados_agrupados.items() if dados['valor_total'] == menor_valor)
        else:
            maior_valor = menor_valor = 0
            maior_periodo = menor_periodo = "N/A"
        
        # Frame para informações gerais
        info_frame = ttk.LabelFrame(self.frame_resumo, text="Informações Gerais")
        info_frame.pack(fill="x", pady=(0, 20))
        
        # Grid para organizar as informações
        info_grid = ttk.Frame(info_frame, padding=10)
        info_grid.pack(fill="x")
        
        # Tipo de relatório
        ttk.Label(info_grid, text="Tipo de Relatório:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(info_grid, text=f"Relatório de {self.tipo_relatorio.capitalize()}").grid(
            row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Agrupamento
        ttk.Label(info_grid, text="Agrupamento:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(info_grid, text=self.var_agrupamento.get().capitalize()).grid(
            row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Frame para estatísticas
        stats_frame = ttk.LabelFrame(self.frame_resumo, text="Estatísticas")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Grid para organizar as estatísticas
        stats_grid = ttk.Frame(stats_frame, padding=10)
        stats_grid.pack(fill="x")
        
        # Total de registros
        ttk.Label(stats_grid, text="Total de registros:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(stats_grid, text=str(total_registros)).grid(
            row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Valor total
        ttk.Label(stats_grid, text="Valor total:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(stats_grid, text=f"R$ {valor_total:.2f}".replace('.', ',')).grid(
            row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Ticket médio
        ttk.Label(stats_grid, text="Ticket médio:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(stats_grid, text=f"R$ {ticket_medio:.2f}".replace('.', ',')).grid(
            row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Maior valor
        ttk.Label(stats_grid, text="Maior valor:", font=("Arial", 10, "bold")).grid(
            row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(stats_grid, text=f"R$ {maior_valor:.2f}".replace('.', ',')).grid(
            row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Período do maior valor
        ttk.Label(stats_grid, text="Período:", font=("Arial", 10, "bold")).grid(
            row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(stats_grid, text=maior_periodo).grid(
            row=1, column=3, sticky="w", padx=5, pady=5)
        
        # Menor valor
        ttk.Label(stats_grid, text="Menor valor:", font=("Arial", 10, "bold")).grid(
            row=2, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(stats_grid, text=f"R$ {menor_valor:.2f}".replace('.', ',')).grid(
            row=2, column=3, sticky="w", padx=5, pady=5)
        
        # Período do menor valor
        ttk.Label(stats_grid, text="Período:", font=("Arial", 10, "bold")).grid(
            row=3, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(stats_grid, text=menor_periodo).grid(
            row=3, column=3, sticky="w", padx=5, pady=5)
        
        # Média diária (se aplicável)
        if self.var_agrupamento.get() == "diario":
            dias_periodo = (self.data_fim - self.data_inicio).days + 1
            media_diaria = valor_total / dias_periodo if dias_periodo > 0 else 0
            
            ttk.Label(stats_grid, text="Média diária:", font=("Arial", 10, "bold")).grid(
                row=3, column=0, sticky="w", padx=5, pady=5)
            ttk.Label(stats_grid, text=f"R$ {media_diaria:.2f}".replace('.', ',')).grid(
                row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Frame para distribuição
        dist_frame = ttk.LabelFrame(self.frame_resumo, text="Distribuição")
        dist_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Criar mini gráfico de distribuição
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Preparar dados
        labels = list(dados_agrupados.keys())
        valores = [float(dados['valor_total']) for dados in dados_agrupados.values()]
        
        # Gráfico de barras horizontal
        y_pos = range(len(labels))
        ax.barh(y_pos, valores, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Valor (R$)')
        ax.set_title('Distribuição de Valores')
        
        # Ajustar layout
        plt.tight_layout()
        
        # Criar canvas do Matplotlib
        canvas = FigureCanvasTkAgg(fig, master=dist_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _atualizar_estatisticas(self, dados_agrupados: Dict[str, Dict[str, Any]]):
        """Atualiza as estatísticas na parte inferior da janela"""
        # Calcular estatísticas básicas
        total_registros = sum(dados['quantidade'] for dados in dados_agrupados.values())
        valor_total = sum(float(dados['valor_total']) for dados in dados_agrupados.values())
        
        # Atualizar label de estatísticas
        self.lbl_estatisticas.config(
            text=f"Total: {total_registros} registros | Valor: R$ {valor_total:.2f}".replace('.', ','))
        
        # Atualizar status
        periodo_str = f"{self.data_inicio.strftime('%d/%m/%Y')} a {self.data_fim.strftime('%d/%m/%Y')}"
        self.lbl_status.config(text=f"Período: {periodo_str} | Agrupamento: {self.var_agrupamento.get()}")
    
    def _exportar_dados(self, formato="excel"):
        """Exporta os dados do relatório para Excel ou PDF"""
        # Verificar se há dados na tabela
        if not hasattr(self, 'tree') or not self.tree.get_children():
            messagebox.showinfo("Aviso", "Não há dados para exportar.")
            return
        
        # Definir tipos de arquivo e extensão padrão
        if formato == "excel":
            filetypes = [('Arquivo Excel', '*.xlsx'), ('Todos os arquivos', '*.*')]
            defaultextension = ".xlsx"
        else:  # PDF
            filetypes = [('Arquivo PDF', '*.pdf'), ('Todos os arquivos', '*.*')]
            defaultextension = ".pdf"
        
        # Perguntar onde salvar
        filename = filedialog.asksaveasfilename(
            title=f"Exportar Relatório de {self.tipo_relatorio.capitalize()}",
            filetypes=filetypes,
            defaultextension=defaultextension
        )
        
        if not filename:
            return
        
        try:
            # Coletar dados da tabela
            dados = []
            colunas = ["Período", "Quantidade", "Valor Total", "Ticket Médio"]
            
            for item_id in self.tree.get_children():
                valores = self.tree.item(item_id, "values")
                dados.append(dict(zip(colunas, valores)))
            
            if formato == "excel":
                # Exportar para Excel
                df = pd.DataFrame(dados)
                
                # Adicionar informações do relatório
                info = {
                    "Tipo de Relatório": [f"Relatório de {self.tipo_relatorio.capitalize()}"],
                    "Período": [f"{self.data_inicio.strftime('%d/%m/%Y')} a {self.data_fim.strftime('%d/%m/%Y')}"],
                    "Agrupamento": [self.var_agrupamento.get().capitalize()],
                    "Data de Geração": [datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
                }
                
                df_info = pd.DataFrame(info)
                
                # Criar um arquivo Excel com várias planilhas
                with pd.ExcelWriter(filename) as writer:
                    df_info.to_excel(writer, sheet_name='Informações', index=False)
                    df.to_excel(writer, sheet_name='Dados', index=False)
                
                messagebox.showinfo("Exportação", f"Dados exportados com sucesso para:\n{filename}")
                
            else:  # PDF
                # Aqui implementaríamos a exportação para PDF
                # Por enquanto, apenas um placeholder
                messagebox.showinfo("Exportação", 
                                   f"Exportando para PDF...\n"
                                   f"Funcionalidade em implementação.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar dados: {e}")
            logging.error(f"Erro ao exportar dados: {e}", exc_info=True)