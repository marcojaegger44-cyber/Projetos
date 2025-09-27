#!/usr/bin/env python3
"""
📷 DEMONSTRAÇÃO - CENTRALIZAÇÃO AUTOMÁTICA DE FOTOS

Este arquivo demonstra como as fotos agora são automaticamente centralizadas
antes de serem salvas no Sistema CM Premium.

FUNCIONALIDADE IMPLEMENTADA:
✅ Redimensiona mantendo proporção
✅ Centraliza em quadrado perfeito
✅ Alta qualidade (LANCZOS)  
✅ Salva como PNG com transparência
✅ Aplica suavização nas bordas
✅ Preview em tempo real

ONDE FUNCIONA:
• Tela de Login - Upload de foto do usuário
• Cadastro de Usuários - Upload de foto 
• Cadastro de Clientes - Upload de foto

COMO TESTAR:
1. Execute o sistema premium
2. Faça upload de qualquer foto (qualquer tamanho/formato)
3. A foto será automaticamente centralizada e salva

EXEMPLO DE PROCESSAMENTO:
Original: 1920x1080 -> Final: 400x400 (centralizada)
Original: 800x600   -> Final: 400x400 (centralizada)  
Original: 300x500   -> Final: 400x400 (centralizada)
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from pathlib import Path
import time

class DemoCentralizacaoFotos:
    """Demo da funcionalidade de centralização de fotos"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📷 Demo - Centralização Automática de Fotos")
        self.root.geometry("800x600")
        self.root.configure(bg='#2C3E50')
        
        # Criar interface
        self._criar_interface()
        
    def _criar_interface(self):
        """Cria interface de demonstração"""
        
        # Título
        titulo = tk.Label(self.root, 
                         text="📷 DEMONSTRAÇÃO - CENTRALIZAÇÃO DE FOTOS",
                         font=("Arial", 16, "bold"),
                         bg='#2C3E50', fg='#ECF0F1')
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = tk.Label(self.root,
                           text="Teste a nova funcionalidade de centralização automática",
                           font=("Arial", 12),
                           bg='#2C3E50', fg='#BDC3C7')
        subtitulo.pack(pady=5)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#34495E', relief='ridge', bd=2)
        main_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Frame de controles
        control_frame = tk.Frame(main_frame, bg='#34495E')
        control_frame.pack(pady=20)
        
        # Botão de upload
        upload_btn = tk.Button(control_frame,
                              text="📁 SELECIONAR FOTO PARA TESTE",
                              command=self._upload_teste,
                              font=("Arial", 12, "bold"),
                              bg='#3498DB', fg='white',
                              activebackground='#2980B9',
                              cursor='hand2',
                              width=30, height=2)
        upload_btn.pack(pady=10)
        
        # Frame de preview
        preview_frame = tk.Frame(main_frame, bg='#34495E')
        preview_frame.pack(pady=20, fill='both', expand=True)
        
        # Labels de preview
        tk.Label(preview_frame, text="ANTES (Original)", 
                font=("Arial", 12, "bold"), 
                bg='#34495E', fg='#E74C3C').pack(side='left', padx=20)
        
        tk.Label(preview_frame, text="DEPOIS (Centralizada)", 
                font=("Arial", 12, "bold"), 
                bg='#34495E', fg='#27AE60').pack(side='right', padx=20)
        
        # Containers das imagens
        images_frame = tk.Frame(main_frame, bg='#34495E')
        images_frame.pack(pady=10, fill='both', expand=True)
        
        # Label para foto original
        self.original_label = tk.Label(images_frame,
                                      text="📷\nImagem Original\n(Qualquer tamanho)",
                                      font=("Arial", 10),
                                      bg='#ECF0F1', fg='#2C3E50',
                                      relief='sunken', bd=2,
                                      width=25, height=15)
        self.original_label.pack(side='left', padx=20, pady=10)
        
        # Label para foto processada
        self.processed_label = tk.Label(images_frame,
                                       text="✨\nImagem Processada\n(400x400 centralizada)",
                                       font=("Arial", 10),
                                       bg='#ECF0F1', fg='#2C3E50',
                                       relief='sunken', bd=2,
                                       width=25, height=15)
        self.processed_label.pack(side='right', padx=20, pady=10)
        
        # Status
        self.status_label = tk.Label(main_frame,
                                    text="💡 Selecione uma foto para ver a demonstração",
                                    font=("Arial", 11),
                                    bg='#34495E', fg='#F39C12')
        self.status_label.pack(pady=20)
        
        # Informações
        info_text = """
ℹ️  INFORMAÇÕES:
• Aceita: PNG, JPG, JPEG, BMP, GIF
• Mantém proporção original
• Centraliza automaticamente
• Alta qualidade (LANCZOS)
• Salva como PNG transparente
• Suavização nas bordas
        """
        
        info_label = tk.Label(main_frame, text=info_text,
                             font=("Arial", 9),
                             bg='#34495E', fg='#95A5A6',
                             justify='left')
        info_label.pack(pady=10)
    
    def _upload_teste(self):
        """Upload de foto para teste"""
        filepath = filedialog.askopenfilename(
            title="Selecione uma foto para testar",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("BMP", "*.bmp"),
                ("GIF", "*.gif")
            ]
        )
        
        if filepath:
            try:
                self._processar_foto_demo(filepath)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar foto: {e}")
    
    def _processar_foto_demo(self, filepath):
        """Processa foto para demonstração"""
        
        # Atualizar status
        self.status_label.configure(text="⏳ Processando foto...", fg='#F39C12')
        self.root.update()
        
        # Carregar imagem original
        img_original = Image.open(filepath).convert('RGBA')
        width_orig, height_orig = img_original.size
        
        # Mostrar original (redimensionada para preview)
        img_preview = img_original.copy()
        img_preview.thumbnail((200, 200), Image.Resampling.LANCZOS)
        photo_orig = ImageTk.PhotoImage(img_preview)
        self.original_label.configure(image=photo_orig, text="")
        self.original_label.image = photo_orig  # Manter referência
        
        # Processar foto (centralizar)
        img_processada = self._centralizar_foto(img_original)
        
        # Mostrar processada
        img_proc_preview = img_processada.copy()
        img_proc_preview.thumbnail((200, 200), Image.Resampling.LANCZOS)
        photo_proc = ImageTk.PhotoImage(img_proc_preview)
        self.processed_label.configure(image=photo_proc, text="")
        self.processed_label.image = photo_proc  # Manter referência
        
        # Salvar exemplo
        demo_dir = Path("demo_fotos")
        demo_dir.mkdir(exist_ok=True)
        
        timestamp = int(time.time())
        save_path = demo_dir / f"foto_centralizada_{timestamp}.png"
        img_processada.save(save_path, 'PNG', quality=95)
        
        # Atualizar status
        status_text = f"✅ Processado! Original: {width_orig}x{height_orig} -> Final: 400x400"
        self.status_label.configure(text=status_text, fg='#27AE60')
        
        # Mostrar informação adicional
        messagebox.showinfo("Sucesso!", 
                           f"Foto processada com sucesso!\n\n"
                           f"📏 Dimensões originais: {width_orig}x{height_orig}\n"
                           f"📐 Dimensões finais: 400x400 (centralizada)\n"
                           f"💾 Salva em: {save_path}\n\n"
                           f"🎯 Esta mesma funcionalidade está ativa em:\n"
                           f"• Tela de Login (usuários)\n"
                           f"• Cadastro de Usuários\n"
                           f"• Cadastro de Clientes")
    
    def _centralizar_foto(self, img, size=400):
        """Centraliza foto mantendo proporção"""
        
        # Obter dimensões originais
        width, height = img.size
        
        # Calcular nova dimensão mantendo proporção
        if width > height:
            new_width = size
            new_height = int((height * size) / width)
        else:
            new_height = size
            new_width = int((width * size) / height)
        
        # Redimensionar com alta qualidade
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Criar imagem de fundo quadrada (transparente)
        final_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # Centralizar imagem na nova imagem quadrada
        x = (size - new_width) // 2
        y = (size - new_height) // 2
        final_img.paste(img_resized, (x, y), img_resized)
        
        # Aplicar suavização nas bordas
        try:
            final_img = final_img.filter(ImageFilter.SMOOTH_MORE)
        except:
            pass  # Se não conseguir aplicar filtro, continuar
        
        return final_img
    
    def executar(self):
        """Executa a demonstração"""
        self.root.mainloop()

def main():
    """Função principal"""
    print("📷 INICIANDO DEMO DE CENTRALIZAÇÃO DE FOTOS")
    print("=" * 60)
    print()
    print("🎯 FUNCIONALIDADE IMPLEMENTADA:")
    print("• Upload de fotos com centralização automática")
    print("• Mantém proporção original da imagem")
    print("• Centraliza em quadrado perfeito (400x400)")
    print("• Alta qualidade de redimensionamento")
    print("• Salva como PNG com transparência")
    print("• Suavização nas bordas")
    print()
    print("📍 ONDE ESTÁ ATIVO:")
    print("• Tela de Login Premium - Upload usuário")
    print("• Cadastros -> Usuários - Upload foto")
    print("• Cadastros -> Clientes - Upload foto")
    print()
    print("🧪 TESTANDO INTERFACE DE DEMONSTRAÇÃO...")
    print("   (Selecione uma foto qualquer para ver o resultado)")
    print()
    
    try:
        demo = DemoCentralizacaoFotos()
        demo.executar()
    except Exception as e:
        print(f"❌ Erro ao executar demo: {e}")
    
    print("\n✅ Demo concluída!")
    print("\n💡 Para usar no sistema real:")
    print("   cd src && python premium_app.py")

if __name__ == "__main__":
    main()
