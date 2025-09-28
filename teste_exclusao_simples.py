#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a exclusão de clientes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from dao_clientes import listar_clientes, remover_cliente

def testar_exclusao():
    print("=== TESTE DE EXCLUSAO DE CLIENTES ===")
    
    # Listar clientes atuais
    print("\n1. Clientes atuais:")
    clientes = listar_clientes()
    for cliente in clientes:
        print(f"   ID: {cliente['id']}, Nome: {cliente['nome']}")
    
    if not clientes:
        print("   Nenhum cliente encontrado!")
        return
    
    # Testar exclusão do primeiro cliente
    primeiro_cliente = clientes[0]
    cliente_id = primeiro_cliente['id']
    cliente_nome = primeiro_cliente['nome']
    
    print(f"\n2. Testando exclusao do cliente: {cliente_nome} (ID: {cliente_id})")
    
    try:
        remover_cliente(cliente_id)
        print(f"   SUCESSO: Cliente '{cliente_nome}' excluido com sucesso!")
    except Exception as e:
        print(f"   ERRO: Erro ao excluir cliente: {e}")
        return
    
    # Verificar se foi realmente excluído
    print("\n3. Verificando exclusao:")
    clientes_apos = listar_clientes()
    cliente_ainda_existe = any(c['id'] == cliente_id for c in clientes_apos)
    
    if cliente_ainda_existe:
        print(f"   ERRO: Cliente '{cliente_nome}' ainda existe no banco!")
    else:
        print(f"   SUCESSO: Cliente '{cliente_nome}' foi removido com sucesso!")
    
    print(f"\n4. Clientes restantes ({len(clientes_apos)}):")
    for cliente in clientes_apos:
        print(f"   ID: {cliente['id']}, Nome: {cliente['nome']}")

if __name__ == "__main__":
    testar_exclusao()
