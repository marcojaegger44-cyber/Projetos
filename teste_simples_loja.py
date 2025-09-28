#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples para verificar se o botão de salvar loja funciona
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from dao_lojas import adicionar_loja, listar_lojas

def testar_botao_salvar():
    print("=== TESTE SIMPLES BOTAO SALVAR ===")
    
    # Criar janela
    root = tk.Tk()
    root.title("Teste Botão Salvar")
    root.geometry("400x300")
    
    # Frame principal
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Campos
    ttk.Label(frame, text="Nome da Loja:").pack(anchor="w")
    entry_nome = ttk.Entry(frame, width=30)
    entry_nome.pack(fill="x", pady=(0, 10))
    
    ttk.Label(frame, text="Tipo:").pack(anchor="w")
    entry_tipo = ttk.Entry(frame, width=30)
    entry_tipo.pack(fill="x", pady=(0, 10))
    
    # Botão salvar
    def salvar_loja():
        print("Botão salvar clicado!")
        nome = entry_nome.get().strip()
        tipo = entry_tipo.get().strip()
        
        if not nome:
            messagebox.showwarning("Atenção", "Nome é obrigatório")
            return
        
        try:
            dados = {"nome": nome, "tipo": tipo or "Mista"}
            adicionar_loja(dados)
            messagebox.showinfo("Sucesso", "Loja criada com sucesso!")
            print("Loja salva com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")
            print(f"Erro: {e}")
    
    btn_salvar = ttk.Button(frame, text="Salvar Loja", command=salvar_loja)
    btn_salvar.pack(pady=20)
    
    # Botão para listar lojas
    def listar():
        lojas = listar_lojas()
        print(f"Lojas no banco: {len(lojas)}")
        for loja in lojas:
            print(f"  - {loja['nome']} (ID: {loja['id']})")
    
    btn_listar = ttk.Button(frame, text="Listar Lojas", command=listar)
    btn_listar.pack(pady=10)
    
    print("Interface criada. Teste o botão 'Salvar Loja'")
    root.mainloop()

if __name__ == "__main__":
    testar_botao_salvar()
