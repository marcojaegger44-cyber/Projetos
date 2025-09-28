#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para integrar lançamentos com lojas e implementar fluxo de caixa
"""

import sqlite3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from db import get_connection

def adicionar_coluna_loja_id():
    """Adiciona coluna loja_id nas tabelas de lançamentos"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Adicionar loja_id em lancamento_receita
        cur.execute("ALTER TABLE lancamento_receita ADD COLUMN loja_id INTEGER")
        print("Coluna loja_id adicionada em lancamento_receita")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Coluna loja_id já existe em lancamento_receita")
        else:
            print(f"Erro ao adicionar loja_id em lancamento_receita: {e}")
    
    try:
        # Adicionar loja_id em lancamento_despesa
        cur.execute("ALTER TABLE lancamento_despesa ADD COLUMN loja_id INTEGER")
        print("Coluna loja_id adicionada em lancamento_despesa")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Coluna loja_id já existe em lancamento_despesa")
        else:
            print(f"Erro ao adicionar loja_id em lancamento_despesa: {e}")
    
    # Adicionar foreign key constraints
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS lancamento_receita_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                tipo_receita TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                status TEXT DEFAULT 'Recebido',
                observacoes TEXT,
                loja_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(loja_id) REFERENCES loja(id)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS lancamento_despesa_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                tipo_despesa TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                status TEXT DEFAULT 'Pago',
                observacoes TEXT,
                loja_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(loja_id) REFERENCES loja(id)
            )
        """)
        
        # Migrar dados existentes
        cur.execute("INSERT INTO lancamento_receita_new (id, data, tipo_receita, descricao, valor, status, observacoes, created_at, loja_id) SELECT id, data, tipo_receita, descricao, valor, status, observacoes, created_at, NULL FROM lancamento_receita")
        cur.execute("INSERT INTO lancamento_despesa_new (id, data, tipo_despesa, descricao, valor, status, observacoes, created_at, loja_id) SELECT id, data, tipo_despesa, descricao, valor, status, observacoes, created_at, NULL FROM lancamento_despesa")
        
        # Substituir tabelas
        cur.execute("DROP TABLE lancamento_receita")
        cur.execute("DROP TABLE lancamento_despesa")
        cur.execute("ALTER TABLE lancamento_receita_new RENAME TO lancamento_receita")
        cur.execute("ALTER TABLE lancamento_despesa_new RENAME TO lancamento_despesa")
        
        print("Tabelas atualizadas com foreign keys")
        
    except Exception as e:
        print(f"Erro ao criar tabelas com foreign keys: {e}")
    
    conn.commit()
    conn.close()

def criar_tabela_fluxo_caixa():
    """Cria tabela para controle de fluxo de caixa por loja"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS fluxo_caixa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loja_id INTEGER NOT NULL,
                data TEXT NOT NULL,
                saldo_inicial REAL DEFAULT 0,
                receitas REAL DEFAULT 0,
                despesas REAL DEFAULT 0,
                saldo_final REAL DEFAULT 0,
                observacoes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(loja_id) REFERENCES loja(id)
            )
        """)
        print("Tabela fluxo_caixa criada")
    except Exception as e:
        print(f"Erro ao criar tabela fluxo_caixa: {e}")
    
    conn.commit()
    conn.close()

def criar_tabela_contrato_curso():
    """Cria tabela para contratos de curso com loja"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contrato_curso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loja_id INTEGER NOT NULL,
                cliente_id INTEGER NOT NULL,
                curso_id INTEGER NOT NULL,
                data_contrato TEXT NOT NULL,
                valor_total REAL NOT NULL,
                parcelas INTEGER NOT NULL,
                status TEXT DEFAULT 'Ativo',
                observacoes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(loja_id) REFERENCES loja(id),
                FOREIGN KEY(cliente_id) REFERENCES cliente_full(id),
                FOREIGN KEY(curso_id) REFERENCES curso(id)
            )
        """)
        print("Tabela contrato_curso criada")
    except Exception as e:
        print(f"Erro ao criar tabela contrato_curso: {e}")
    
    conn.commit()
    conn.close()

def criar_tabela_contrato_imovel():
    """Cria tabela para contratos de imóvel com loja"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contrato_imovel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loja_id INTEGER NOT NULL,
                cliente_id INTEGER NOT NULL,
                imovel_id INTEGER NOT NULL,
                data_contrato TEXT NOT NULL,
                valor_venda REAL NOT NULL,
                comissao REAL NOT NULL,
                status TEXT DEFAULT 'Ativo',
                observacoes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(loja_id) REFERENCES loja(id),
                FOREIGN KEY(cliente_id) REFERENCES cliente_full(id),
                FOREIGN KEY(imovel_id) REFERENCES imovel(id)
            )
        """)
        print("Tabela contrato_imovel criada")
    except Exception as e:
        print(f"Erro ao criar tabela contrato_imovel: {e}")
    
    conn.commit()
    conn.close()

def main():
    print("=== INTEGRACAO LANÇAMENTOS COM LOJAS ===")
    
    print("\n1. Adicionando coluna loja_id...")
    adicionar_coluna_loja_id()
    
    print("\n2. Criando tabela fluxo_caixa...")
    criar_tabela_fluxo_caixa()
    
    print("\n3. Criando tabela contrato_curso...")
    criar_tabela_contrato_curso()
    
    print("\n4. Criando tabela contrato_imovel...")
    criar_tabela_contrato_imovel()
    
    print("\nIntegracao concluida!")

if __name__ == "__main__":
    main()
