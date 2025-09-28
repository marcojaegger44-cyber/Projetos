#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar a janela de nova loja
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from window_utils import criar_janela_centralizada
from dao_lojas import adicionar_loja, listar_lojas
from ui_utils import aplicar_mascaras_automaticas

def testar_janela_loja():
    print("=== TESTE JANELA LOJA ===")
    
    # Criar janela principal
    root = tk.Tk()
    root.title("Teste Janela Loja")
    root.geometry("600x400")
    
    def criar_nova_loja():
        print("Criando janela de nova loja...")
        
        try:
            win, frame_principal = criar_janela_centralizada(
                root, 
                "Nova Loja", 
                largura=400, 
                altura=500, 
                com_botao_voltar=True
            )
            
            if not win or not frame_principal:
                print("ERRO: Falha ao criar janela")
                messagebox.showerror("Erro", "Falha ao criar janela")
                return
            
            print("Janela criada com sucesso!")
            print(f"Janela existe: {win.winfo_exists()}")
            print(f"Frame existe: {frame_principal.winfo_exists()}")
            
            # Criar campos
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
            
            # Aplicar máscaras
            aplicar_mascaras_automaticas(entries)
            
            # Função salvar
            def salvar():
                print("Função salvar chamada!")
                nome = entries["nome"].get().strip()
                if not nome:
                    messagebox.showwarning("Atenção", "Nome da loja é obrigatório")
                    return
                
                data = {k: v.get() for k, v in entries.items()}
                print(f"Dados: {data}")
                
                try:
                    adicionar_loja(data)
                    messagebox.showinfo("Sucesso", "Loja criada com sucesso!")
                    win.destroy()
                    print("Loja salva com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro: {e}")
                    print(f"Erro: {e}")
            
            # Criar botões
            print("Criando botão salvar...")
            btn_salvar = ttk.Button(frame_principal, text="💾 Salvar Loja", command=salvar)
            btn_salvar.pack(pady=20, padx=20, fill="x")
            
            btn_cancelar = ttk.Button(frame_principal, text="❌ Cancelar", command=win.destroy)
            btn_cancelar.pack(pady=(0, 20), padx=20, fill="x")
            
            # Verificar botões
            print(f"Botão salvar existe: {btn_salvar.winfo_exists()}")
            print(f"Botão salvar visível: {btn_salvar.winfo_viewable()}")
            print(f"Botão cancelar existe: {btn_cancelar.winfo_exists()}")
            print(f"Botão cancelar visível: {btn_cancelar.winfo_viewable()}")
            
            # Forçar atualização
            win.update()
            print(f"Altura da janela: {win.winfo_height()}")
            print(f"Largura da janela: {win.winfo_width()}")
            
        except Exception as e:
            print(f"Erro ao criar janela: {e}")
            messagebox.showerror("Erro", f"Erro: {e}")
    
    # Botão para testar
    btn_teste = tk.Button(root, text="Criar Nova Loja", command=criar_nova_loja, font=('Arial', 14, 'bold'))
    btn_teste.pack(pady=50)
    
    # Botão para listar lojas
    def listar_lojas():
        lojas = listar_lojas()
        print(f"Lojas no banco: {len(lojas)}")
        for loja in lojas:
            print(f"  - {loja['nome']} (ID: {loja['id']})")
        messagebox.showinfo("Lojas", f"Total de lojas: {len(lojas)}")
    
    btn_listar = tk.Button(root, text="Listar Lojas", command=listar_lojas, font=('Arial', 12))
    btn_listar.pack(pady=20)
    
    print("Interface criada. Clique em 'Criar Nova Loja' para testar.")
    root.mainloop()

if __name__ == "__main__":
    testar_janela_loja()
