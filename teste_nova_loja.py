#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a criação de nova loja
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from dao_lojas import adicionar_loja, listar_lojas

def testar_nova_loja():
    print("=== TESTE DE CRIACAO DE NOVA LOJA ===")
    
    # 1. Listar lojas atuais
    print("\n1. Lojas atuais:")
    lojas = listar_lojas()
    for loja in lojas:
        print(f"   ID: {loja['id']}, Nome: {loja['nome']}, Ativo: {loja['ativo']}")
    
    # 2. Testar criação de nova loja
    print("\n2. Testando criacao de nova loja...")
    
    dados_loja = {
        "nome": "Loja Teste",
        "tipo": "Mista",
        "cidade": "São Paulo",
        "uf": "SP",
        "responsavel": "Teste",
        "telefone": "11999999999",
        "email": "teste@loja.com"
    }
    
    try:
        adicionar_loja(dados_loja)
        print("   SUCESSO: Loja criada com sucesso!")
    except Exception as e:
        print(f"   ERRO: Erro ao criar loja: {e}")
        return
    
    # 3. Verificar se foi criada
    print("\n3. Verificando criacao:")
    lojas_apos = listar_lojas()
    loja_criada = any(l['nome'] == 'Loja Teste' for l in lojas_apos)
    
    if loja_criada:
        print("   SUCESSO: Loja encontrada no banco!")
    else:
        print("   ERRO: Loja nao foi criada!")
    
    print(f"\n4. Lojas apos criacao ({len(lojas_apos)}):")
    for loja in lojas_apos:
        print(f"   ID: {loja['id']}, Nome: {loja['nome']}, Ativo: {loja['ativo']}")

if __name__ == "__main__":
    testar_nova_loja()
