"""
Launcher Silencioso do Sistema CM Premium
Executa o sistema sem mostrar nenhuma janela do terminal
"""

import subprocess
import sys
import os

def executar_sistema():
    """Executa o sistema premium sem mostrar o terminal"""
    try:
        # Mudar para o diretório do projeto
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Executar o sistema premium sem janela
        subprocess.Popen([
            sys.executable, 
            "src/premium_app.py"
        ], 
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
        )
        
    except Exception as e:
        # Em caso de erro, mostrar mensagem simples
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", f"Erro ao executar o sistema: {e}")
        root.destroy()

if __name__ == "__main__":
    executar_sistema()
