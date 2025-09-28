#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debugar a exclusão de clientes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from dao_clientes import listar_clientes, remover_cliente
import sqlite3

def debug_exclusao():
    print("=== DEBUG EXCLUSAO DE CLIENTES ===")
    
    # 1. Verificar clientes atuais
    print("\n1. Clientes atuais no banco:")
    clientes = listar_clientes()
    for cliente in clientes:
        print(f"   ID: {cliente['id']}, Nome: {cliente['nome']}")
    
    if not clientes:
        print("   Nenhum cliente encontrado!")
        return
    
    # 2. Verificar estrutura da tabela
    print("\n2. Estrutura da tabela cliente_full:")
    conn = sqlite3.connect('sistema.db')
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(cliente_full)")
    colunas = cur.fetchall()
    for coluna in colunas:
        print(f"   {coluna[1]}: {coluna[2]}")
    conn.close()
    
    # 3. Testar exclusão com debug
    primeiro_cliente = clientes[0]
    cliente_id = primeiro_cliente['id']
    cliente_nome = primeiro_cliente['nome']
    
    print(f"\n3. Testando exclusao do cliente: {cliente_nome} (ID: {cliente_id})")
    
    # Verificar se o cliente existe antes da exclusão
    conn = sqlite3.connect('sistema.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cliente_full WHERE id = ?", (cliente_id,))
    count_antes = cur.fetchone()[0]
    print(f"   Clientes com ID {cliente_id} antes da exclusao: {count_antes}")
    conn.close()
    
    try:
        # Tentar exclusão
        remover_cliente(cliente_id)
        print(f"   Funcao remover_cliente executada sem erro")
        
        # Verificar se foi excluído
        conn = sqlite3.connect('sistema.db')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM cliente_full WHERE id = ?", (cliente_id,))
        count_depois = cur.fetchone()[0]
        print(f"   Clientes com ID {cliente_id} depois da exclusao: {count_depois}")
        conn.close()
        
        if count_depois == 0:
            print(f"   SUCESSO: Cliente excluido com sucesso!")
        else:
            print(f"   ERRO: Cliente ainda existe no banco!")
            
    except Exception as e:
        print(f"   ERRO na exclusao: {e}")
        import traceback
        traceback.print_exc()
    
    # 4. Listar clientes restantes
    print("\n4. Clientes restantes:")
    clientes_restantes = listar_clientes()
    for cliente in clientes_restantes:
        print(f"   ID: {cliente['id']}, Nome: {cliente['nome']}")

if __name__ == "__main__":
    debug_exclusao()
