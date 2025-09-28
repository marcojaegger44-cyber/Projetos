#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a interface de criação de loja
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from window_utils import criar_janela_centralizada
from dao_lojas import adicionar_loja, listar_lojas
from ui_utils import aplicar_mascaras_automaticas

def testar_interface_loja():
    print("=== TESTE DE INTERFACE DE LOJA ===")
    
    # Criar janela principal
    root = tk.Tk()
    root.title("Teste Interface Loja")
    root.geometry("400x300")
    
    def criar_nova_loja():
        print("Criando janela de nova loja...")
        
        win, frame_principal = criar_janela_centralizada(
            root, 
            "Nova Loja", 
            largura=320, 
            altura=350, 
            com_botao_voltar=True
        )
        
        if not win or not frame_principal:
            print("ERRO: Falha ao criar janela")
            return
        
        entries = {}
        campos = [
            ("Nome", "nome"),
            ("Tipo (Cursos/Corretagem/Mista)", "tipo"),
            ("Cidade", "cidade"),
            ("UF", "uf"),
            ("Responsável", "responsavel"),
            ("Telefone", "telefone"),
            ("Email", "email"),
        ]
        
        for label, key in campos:
            ttk.Label(frame_principal, text=f"{label}:").pack(anchor="w", padx=10, pady=2)
            e = ttk.Entry(frame_principal, width=30)
            e.pack(padx=10)
            entries[key] = e
        
        # Aplicar máscaras automáticas
        aplicar_mascaras_automaticas(entries)
        
        def salvar():
            print("Função salvar chamada")
            nome = entries["nome"].get().strip()
            if not nome:
                messagebox.showwarning("Atenção", "Nome da loja é obrigatório")
                return
            
            data = {k: v.get() for k, v in entries.items()}
            print(f"Dados da loja: {data}")
            
            try:
                adicionar_loja(data)
                print("Loja salva com sucesso!")
                messagebox.showinfo("Sucesso", "Loja criada com sucesso!")
                win.destroy()
            except Exception as e:
                print(f"Erro ao salvar loja: {e}")
                messagebox.showerror("Erro", f"Erro ao salvar loja: {e}")
        
        # Criar botão salvar
        btn_salvar = ttk.Button(frame_principal, text="Salvar", command=salvar)
        btn_salvar.pack(pady=10)
        print("Botão salvar criado")
        
        # Verificar se o botão foi criado
        print(f"Botão existe: {btn_salvar.winfo_exists()}")
        print(f"Botão visível: {btn_salvar.winfo_viewable()}")
    
    # Botão para testar
    btn_teste = tk.Button(root, text="Criar Nova Loja", command=criar_nova_loja)
    btn_teste.pack(pady=20)
    
    # Botão para listar lojas
    def listar_lojas_btn():
        lojas = listar_lojas()
        print(f"Lojas no banco: {len(lojas)}")
        for loja in lojas:
            print(f"  - {loja['nome']} (ID: {loja['id']})")
    
    btn_listar = tk.Button(root, text="Listar Lojas", command=listar_lojas_btn)
    btn_listar.pack(pady=10)
    
    print("Interface de teste criada. Clique em 'Criar Nova Loja' para testar.")
    root.mainloop()

if __name__ == "__main__":
    testar_interface_loja()
