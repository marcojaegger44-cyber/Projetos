#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar o banco de dados do sistema
Mantém apenas as estruturas das tabelas e dados essenciais
"""

import sqlite3
from pathlib import Path
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from db import get_connection, init_db

def limpar_banco_dados():
    """Limpa o banco de dados mantendo apenas estruturas e dados essenciais"""
    
    print("Iniciando limpeza do banco de dados...")
    
    try:
        # Conectar ao banco
        conn = get_connection()
        cur = conn.cursor()
        
        # Lista de tabelas para limpar (dados, mas mantém estrutura)
        tabelas_para_limpar = [
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
            'auditoria'
        ]
        
        # Limpar dados das tabelas
        for tabela in tabelas_para_limpar:
            try:
                cur.execute(f"DELETE FROM {tabela}")
                print(f"Dados da tabela '{tabela}' removidos")
            except Exception as e:
                print(f"Aviso: Não foi possível limpar '{tabela}': {e}")
        
        # Manter apenas usuário admin
        cur.execute("DELETE FROM usuario WHERE username != 'admin'")
        print("✅ Usuários removidos (exceto admin)")
        
        # Manter apenas loja padrão
        cur.execute("DELETE FROM loja WHERE nome != 'Loja Principal'")
        print("✅ Lojas removidas (exceto Loja Principal)")
        
        # Manter apenas cliente admin
        cur.execute("DELETE FROM cliente WHERE nome != 'admin'")
        print("✅ Clientes removidos (exceto admin)")
        
        # Manter apenas curso padrão
        cur.execute("DELETE FROM curso WHERE nome != 'Curso Padrão'")
        print("✅ Cursos removidos (exceto Curso Padrão)")
        
        # Manter apenas imóvel padrão
        cur.execute("DELETE FROM imovel WHERE descricao != 'Imóvel Padrão'")
        print("✅ Imóveis removidos (exceto Imóvel Padrão)")
        
        # Limpar tipos de receita e despesa
        cur.execute("DELETE FROM tipo_receita")
        cur.execute("DELETE FROM tipo_despesa")
        print("✅ Tipos de receita e despesa removidos")
        
        # Inserir dados essenciais se não existirem
        inserir_dados_essenciais(cur)
        
        # Commit das alterações
        conn.commit()
        print("✅ Alterações salvas no banco")
        
        # Verificar integridade
        verificar_integridade(cur)
        
        conn.close()
        print("🎯 Limpeza do banco concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante a limpeza: {e}")
        return False
    
    return True

def inserir_dados_essenciais(cur):
    """Insere dados essenciais para o funcionamento do sistema"""
    
    print("📝 Inserindo dados essenciais...")
    
    # Verificar e inserir loja principal
    cur.execute("SELECT COUNT(*) FROM loja WHERE nome = 'Loja Principal'")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO loja (nome, tipo, cidade, uf, responsavel, ativo) 
            VALUES ('Loja Principal', 'Mista', 'São Paulo', 'SP', 'Administrador', 1)
        """)
        print("✅ Loja Principal criada")
    
    # Verificar e inserir cliente admin
    cur.execute("SELECT COUNT(*) FROM cliente WHERE nome = 'admin'")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO cliente (nome, telefone, email, documento) 
            VALUES ('admin', '11999999999', 'admin@sistema.com', '000.000.000-00')
        """)
        print("✅ Cliente admin criado")
    
    # Verificar e inserir curso padrão
    cur.execute("SELECT COUNT(*) FROM curso WHERE nome = 'Curso Padrão'")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO curso (nome, valor_base, cashback_pct, ativo) 
            VALUES ('Curso Padrão', 1000.00, 5.0, 1)
        """)
        print("✅ Curso Padrão criado")
    
    # Verificar e inserir imóvel padrão
    cur.execute("SELECT COUNT(*) FROM imovel WHERE descricao = 'Imóvel Padrão'")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO imovel (descricao, valor, localizacao) 
            VALUES ('Imóvel Padrão', 500000.00, 'São Paulo - SP')
        """)
        print("✅ Imóvel Padrão criado")
    
    # Inserir tipos de receita padrão
    tipos_receita = [
        ('Vendas de Cursos', 'Receitas provenientes de vendas de cursos'),
        ('Comissões de Imóveis', 'Comissões recebidas de vendas de imóveis'),
        ('Receitas Diversas', 'Outras receitas do negócio')
    ]
    
    for nome, descricao in tipos_receita:
        cur.execute("INSERT OR IGNORE INTO tipo_receita (nome, descricao) VALUES (?, ?)", 
                   (nome, descricao))
    
    print("✅ Tipos de receita inseridos")
    
    # Inserir tipos de despesa padrão
    tipos_despesa = [
        ('Despesas Operacionais', 'Despesas gerais de operação'),
        ('Marketing', 'Gastos com marketing e publicidade'),
        ('Infraestrutura', 'Gastos com infraestrutura e equipamentos'),
        ('Despesas Diversas', 'Outras despesas do negócio')
    ]
    
    for nome, descricao in tipos_despesa:
        cur.execute("INSERT OR IGNORE INTO tipo_despesa (nome, descricao) VALUES (?, ?)", 
                   (nome, descricao))
    
    print("✅ Tipos de despesa inseridos")

def verificar_integridade(cur):
    """Verifica a integridade do banco após a limpeza"""
    
    print("🔍 Verificando integridade do banco...")
    
    # Verificar tabelas principais
    tabelas_principais = ['usuario', 'loja', 'cliente', 'curso', 'imovel']
    
    for tabela in tabelas_principais:
        cur.execute(f"SELECT COUNT(*) FROM {tabela}")
        count = cur.fetchone()[0]
        print(f"📊 {tabela}: {count} registros")
    
    # Verificar tabelas de lançamentos (devem estar vazias)
    tabelas_lancamentos = ['lancamento_receita', 'lancamento_despesa', 'contrato_curso']
    
    for tabela in tabelas_lancamentos:
        cur.execute(f"SELECT COUNT(*) FROM {tabela}")
        count = cur.fetchone()[0]
        if count == 0:
            print(f"✅ {tabela}: Vazia (correto)")
        else:
            print(f"⚠️  {tabela}: {count} registros (deveria estar vazia)")

if __name__ == "__main__":
    print("=" * 60)
    print("🧹 LIMPEZA DO BANCO DE DADOS DO SISTEMA")
    print("=" * 60)
    
    # Confirmar limpeza
    resposta = input("⚠️  Tem certeza que deseja limpar o banco? (sim/não): ").lower()
    
    if resposta in ['sim', 's', 'yes', 'y']:
        sucesso = limpar_banco_dados()
        
        if sucesso:
            print("\n🎯 Banco limpo com sucesso!")
            print("📋 Próximos passos:")
            print("   1. Execute o sistema")
            print("   2. Teste as integrações de lançamentos")
            print("   3. Verifique se os dados são salvos corretamente")
        else:
            print("\n❌ Erro durante a limpeza do banco!")
    else:
        print("❌ Limpeza cancelada pelo usuário.")
    
    print("=" * 60)
