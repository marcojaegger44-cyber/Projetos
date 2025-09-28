#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples para verificar se o problema está na interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from dao_lojas import adicionar_loja, listar_lojas

def testar_interface_simples():
    print("=== TESTE INTERFACE SIMPLES ===")
    
    # Criar janela principal
    root = tk.Tk()
    root.title("Teste Interface Simples")
    root.geometry("500x400")
    
    def criar_janela_loja():
        print("Criando janela de loja...")
        
        # Criar janela filha
        win = tk.Toplevel(root)
        win.title("Nova Loja")
        win.geometry("400x500")
        win.resizable(False, False)
        
        # Centralizar
        win.transient(root)
        win.grab_set()
        
        # Frame principal
        frame = ttk.Frame(win)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(frame, text="Nova Loja", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # Campos
        campos = [
            ("Nome", "nome"),
            ("Tipo", "tipo"),
            ("Cidade", "cidade"),
            ("UF", "uf"),
            ("Responsável", "responsavel"),
            ("Telefone", "telefone"),
            ("Email", "email"),
        ]
        
        entries = {}
        for label, key in campos:
            ttk.Label(frame, text=f"{label}:").pack(anchor="w", pady=(10, 2))
            e = ttk.Entry(frame, width=30)
            e.pack(fill="x", pady=(0, 5))
            entries[key] = e
        
        # Função salvar
        def salvar():
            print("Salvando loja...")
            nome = entries["nome"].get().strip()
            if not nome:
                messagebox.showwarning("Atenção", "Nome é obrigatório")
                return
            
            data = {k: v.get() for k, v in entries.items()}
            print(f"Dados: {data}")
            
            try:
                adicionar_loja(data)
                messagebox.showinfo("Sucesso", "Loja criada com sucesso!")
                win.destroy()
                print("Loja salva!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
                print(f"Erro: {e}")
        
        # Botões
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(fill="x", pady=20)
        
        btn_salvar = ttk.Button(frame_botoes, text="💾 Salvar", command=salvar)
        btn_salvar.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        btn_cancelar = ttk.Button(frame_botoes, text="❌ Cancelar", command=win.destroy)
        btn_cancelar.pack(side="right", padx=(10, 0), fill="x", expand=True)
        
        # Verificar botões
        print(f"Botão salvar existe: {btn_salvar.winfo_exists()}")
        print(f"Botão salvar visível: {btn_salvar.winfo_viewable()}")
        print(f"Botão cancelar existe: {btn_cancelar.winfo_exists()}")
        print(f"Botão cancelar visível: {btn_cancelar.winfo_viewable()}")
        
        # Forçar atualização
        win.update()
        print(f"Altura da janela: {win.winfo_height()}")
        print(f"Largura da janela: {win.winfo_width()}")
        
        # Garantir que a janela apareça
        win.lift()
        win.focus_force()
    
    # Botão para testar
    btn_teste = tk.Button(root, text="Criar Nova Loja", command=criar_janela_loja, font=('Arial', 14, 'bold'))
    btn_teste.pack(pady=50)
    
    # Botão para listar
    def listar():
        lojas = listar_lojas()
        print(f"Lojas: {len(lojas)}")
        for loja in lojas:
            print(f"  - {loja['nome']}")
        messagebox.showinfo("Lojas", f"Total: {len(lojas)}")
    
    btn_listar = tk.Button(root, text="Listar Lojas", command=listar, font=('Arial', 12))
    btn_listar.pack(pady=20)
    
    print("Interface criada. Clique em 'Criar Nova Loja' para testar.")
    root.mainloop()

if __name__ == "__main__":
    testar_interface_simples()
