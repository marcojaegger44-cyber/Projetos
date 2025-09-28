#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpeza COMPLETA do banco de dados
Remove TODOS os dados, mantendo apenas estruturas e dados básicos de cadastro
"""

import sqlite3
from pathlib import Path
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from db import get_connection, init_db

def limpar_banco_completo():
    """Limpeza COMPLETA do banco - remove TODOS os dados"""
    
    print("INICIANDO LIMPEZA COMPLETA DO BANCO...")
    
    try:
        # Conectar ao banco
        conn = get_connection()
        cur = conn.cursor()
        
        # Lista COMPLETA de todas as tabelas com dados
        todas_tabelas = [
            'lancamento_receita',
            'lancamento_despesa', 
            'contrato_curso',
            'parcela_contrato',
            'cashback_cliente',
            'historico_transacoes',
            'venda_curso',
            'parcela_curso',
            'venda_imovel',
            'imovel_vendido',
            'receita_diversa',
            'despesa_diversa',
            'receita',
            'despesa',
            'auditoria',
            'tipo_receita',
            'tipo_despesa',
            'metas'
        ]
        
        # LIMPAR TODAS as tabelas
        for tabela in todas_tabelas:
            try:
                cur.execute(f"DELETE FROM {tabela}")
                print(f"Tabela '{tabela}' LIMPA")
            except Exception as e:
                print(f"Aviso: {tabela} - {e}")
        
        # Manter APENAS usuário admin
        cur.execute("DELETE FROM usuario WHERE username != 'admin'")
        print("Usuarios: APENAS admin mantido")
        
        # Manter APENAS loja básica
        cur.execute("DELETE FROM loja")
        print("Lojas: TODAS removidas")
        
        # Manter APENAS cliente admin
        cur.execute("DELETE FROM cliente WHERE nome != 'admin'")
        print("Clientes: APENAS admin mantido")
        
        # Manter APENAS curso básico
        cur.execute("DELETE FROM curso")
        print("Cursos: TODOS removidos")
        
        # Manter APENAS imóvel básico
        cur.execute("DELETE FROM imovel")
        print("Imoveis: TODOS removidos")
        
        # Inserir dados MÍNIMOS essenciais
        inserir_dados_minimos(cur)
        
        # Commit das alterações
        conn.commit()
        print("ALTERACOES SALVAS")
        
        # Verificar limpeza
        verificar_limpeza_completa(cur)
        
        conn.close()
        print("LIMPEZA COMPLETA CONCLUIDA!")
        
    except Exception as e:
        print(f"ERRO: {e}")
        return False
    
    return True

def inserir_dados_minimos(cur):
    """Insere apenas dados MÍNIMOS para funcionamento"""
    
    print("Inserindo dados MINIMOS...")
    
    # Apenas loja básica
    cur.execute("""
        INSERT INTO loja (nome, tipo, ativo) 
        VALUES ('Loja Principal', 'Mista', 1)
    """)
    print("Loja basica criada")
    
    # Apenas cliente admin
    cur.execute("""
        INSERT OR IGNORE INTO cliente (nome, telefone, email) 
        VALUES ('admin', '11999999999', 'admin@sistema.com')
    """)
    print("Cliente admin mantido")
    
    # Apenas curso básico
    cur.execute("""
        INSERT INTO curso (nome, valor_base, ativo) 
        VALUES ('Curso Basico', 1000.00, 1)
    """)
    print("Curso basico criado")
    
    # Apenas imóvel básico
    cur.execute("""
        INSERT INTO imovel (descricao, valor, localizacao) 
        VALUES ('Imovel Basico', 500000.00, 'Sao Paulo')
    """)
    print("Imovel basico criado")
    
    # Metas zeradas
    cur.execute("""
        INSERT INTO metas (id, cashback_meta, comissao_meta) 
        VALUES (1, 0, 0)
    """)
    print("Metas zeradas")

def verificar_limpeza_completa(cur):
    """Verifica se a limpeza foi completa"""
    
    print("VERIFICANDO LIMPEZA COMPLETA...")
    
    # Verificar tabelas principais (devem ter apenas 1 registro cada)
    tabelas_principais = ['usuario', 'loja', 'cliente', 'curso', 'imovel']
    
    for tabela in tabelas_principais:
        cur.execute(f"SELECT COUNT(*) FROM {tabela}")
        count = cur.fetchone()[0]
        print(f"{tabela}: {count} registros")
    
    # Verificar tabelas de lançamentos (devem estar VAZIAS)
    tabelas_lancamentos = [
        'lancamento_receita', 'lancamento_despesa', 'contrato_curso',
        'parcela_contrato', 'cashback_cliente', 'historico_transacoes',
        'venda_curso', 'parcela_curso', 'venda_imovel', 'imovel_vendido',
        'receita_diversa', 'despesa_diversa', 'receita', 'despesa',
        'auditoria', 'tipo_receita', 'tipo_despesa'
    ]
    
    for tabela in tabelas_lancamentos:
        cur.execute(f"SELECT COUNT(*) FROM {tabela}")
        count = cur.fetchone()[0]
        if count == 0:
            print(f"{tabela}: VAZIA (correto)")
        else:
            print(f"{tabela}: {count} registros (AINDA TEM DADOS!)")

if __name__ == "__main__":
    print("=" * 70)
    print("LIMPEZA COMPLETA DO BANCO DE DADOS")
    print("REMOVENDO TODOS OS DADOS - MANTENDO APENAS ESTRUTURAS")
    print("=" * 70)
    
    sucesso = limpar_banco_completo()
    
    if sucesso:
        print("\nBANCO COMPLETAMENTE LIMPO!")
        print("DASHBOARD VAZIO - APENAS CADASTROS BASICOS")
        print("PRONTO PARA TESTES DE INTEGRACAO")
    else:
        print("\nERRO NA LIMPEZA!")
    
    print("=" * 70)
