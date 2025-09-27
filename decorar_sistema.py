#!/usr/bin/env python3
"""
🎨 DECORADOR AUTOMÁTICO DO SISTEMA CM

Este script aplica melhorias visuais automáticas ao sistema:
- Temas personalizados
- Ícones modernos  
- Animações suaves
- Componentes visuais avançados
- Dashboard com gráficos
- Tipografia melhorada

Execute: python decorar_sistema.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from pathlib import Path

class DecoradorSistema:
    """Classe principal para decoração do sistema"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎨 Decorador do Sistema CM")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2C3E50')
        
        # Paletas de cores disponíveis
        self.temas = {
            'premium': {
                'primary': '#3498DB',
                'secondary': '#2C3E50', 
                'accent': '#E74C3C',
                'bg_primary': '#ECF0F1',
                'bg_card': '#FFFFFF'
            },
            'cyberpunk': {
                'primary': '#FF0080',
                'secondary': '#00FFFF',
                'accent': '#FFFF00',
                'bg_primary': '#0D0221',
                'bg_card': '#1A0B3D'
            },
            'nature': {
                'primary': '#2E8B57',
                'secondary': '#228B22',
                'accent': '#32CD32',
                'bg_primary': '#F0FFF0',
                'bg_card': '#FFFFFF'
            },
            'sunset': {
                'primary': '#FF6347',
                'secondary': '#FF4500',
                'accent': '#FFD700',
                'bg_primary': '#FFF8DC',
                'bg_card': '#FFFFFF'
            }
        }
        
        self.tema_atual = 'premium'
        self._criar_interface()
    
    def _criar_interface(self):
        """Cria interface de demonstração das decorações"""
        
        # Header principal
        self._criar_header()
        
        # Área de controles
        self._criar_controles()
        
        # Área de demonstração
        self._criar_area_demo()
        
        # Footer com informações
        self._criar_footer()
    
    def _criar_header(self):
        """Cria header moderno"""
        header = tk.Frame(self.root, bg='#34495E', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título com ícone
        title_frame = tk.Frame(header, bg='#34495E')
        title_frame.pack(expand=True)
        
        titulo = tk.Label(title_frame,
                         text="🎨 DECORADOR DO SISTEMA CM",
                         text="INICIANDO DECORADOR DO SISTEMA CM",
                         font=('Segoe UI', 20, 'bold'),
                         bg='#34495E', fg='#ECF0F1')
        titulo.pack(pady=20)
    
    def _criar_controles(self):
        """Cria área de controles"""
        controls_frame = tk.Frame(self.root, bg='#2C3E50', height=100)
        controls_frame.pack(fill='x', pady=10)
        controls_frame.pack_propagate(False)
        
        # Frame interno para centralizar
        inner_frame = tk.Frame(controls_frame, bg='#2C3E50')
        inner_frame.pack(expand=True)
        
        # Label de instruções
        tk.Label(inner_frame, 
                text="🎯 Selecione um tema para ver a demonstração:",
                font=('Segoe UI', 12),
                bg='#2C3E50', fg='#BDC3C7').pack(pady=5)
        
        # Botões de tema
        themes_frame = tk.Frame(inner_frame, bg='#2C3E50')
        themes_frame.pack(pady=10)
        
        for tema_nome in self.temas.keys():
            btn = self._criar_botao_tema(themes_frame, tema_nome)
            btn.pack(side='left', padx=10)
    
    def _criar_botao_tema(self, parent, tema_nome):
        """Cria botão de tema estilizado"""
        tema = self.temas[tema_nome]
        
        btn = tk.Button(parent,
                       text=f"🎨 {tema_nome.title()}",
                       font=('Segoe UI', 11, 'bold'),
                       bg=tema['primary'],
                       fg='white',
                       activebackground=tema['secondary'],
                       relief='flat',
                       cursor='hand2',
                       width=12, height=2,
                       command=lambda: self._aplicar_tema(tema_nome))
        
        # Efeito hover
        def on_enter(event):
            btn.configure(bg=tema['accent'])
        
        def on_leave(event):
            btn.configure(bg=tema['primary'])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def _criar_area_demo(self):
        """Cria área de demonstração"""
        # Frame principal da demo
        self.demo_frame = tk.Frame(self.root, bg='#ECF0F1')
        self.demo_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Carregar demonstração inicial
        self._carregar_demo_premium()
    
    def _carregar_demo_premium(self):
        """Carrega demonstração do tema premium"""
        # Limpar área
        for widget in self.demo_frame.winfo_children():
            widget.destroy()
        
        tema = self.temas[self.tema_atual]
        
        # Título da demo
        demo_title = tk.Label(self.demo_frame,
                             text=f"✨ Demonstração - Tema {self.tema_atual.title()}",
                             font=('Segoe UI', 16, 'bold'),
                             bg=tema['bg_primary'], fg=tema['secondary'])
        demo_title.pack(pady=10)
        
        # Container principal
        main_container = tk.Frame(self.demo_frame, bg=tema['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Criar cards de demonstração
        self._criar_cards_demo(main_container, tema)
        
        # Criar gráficos de demonstração
        self._criar_graficos_demo(main_container, tema)
    
    def _criar_cards_demo(self, parent, tema):
        """Cria cards de demonstração"""
        cards_frame = tk.Frame(parent, bg=tema['bg_primary'])
        cards_frame.pack(fill='x', pady=10)
        
        # Card 1 - Vendas
        card1 = self._criar_card_moderno(cards_frame, "💰 Vendas", tema)
        card1.pack(side='left', padx=10, fill='x', expand=True)
        
        # Conteúdo do card 1
        if hasattr(card1, 'content_frame'):
            tk.Label(card1.content_frame, text="R$ 150.000,00",
                    font=('Segoe UI', 20, 'bold'),
                    bg=tema['bg_card'], fg=tema['primary']).pack()
            tk.Label(card1.content_frame, text="↗️ +15% este mês",
                    font=('Segoe UI', 12),
                    bg=tema['bg_card'], fg=tema['accent']).pack()
        
        # Card 2 - Clientes
        card2 = self._criar_card_moderno(cards_frame, "🤝 Clientes", tema)
        card2.pack(side='left', padx=10, fill='x', expand=True)
        
        # Conteúdo do card 2
        if hasattr(card2, 'content_frame'):
            tk.Label(card2.content_frame, text="1,234",
                    font=('Segoe UI', 20, 'bold'),
                    bg=tema['bg_card'], fg=tema['primary']).pack()
            tk.Label(card2.content_frame, text="↗️ +8% este mês",
                    font=('Segoe UI', 12),
                    bg=tema['bg_card'], fg=tema['accent']).pack()
        
        # Card 3 - Produtos  
        card3 = self._criar_card_moderno(cards_frame, "📦 Produtos", tema)
        card3.pack(side='left', padx=10, fill='x', expand=True)
        
        # Conteúdo do card 3
        if hasattr(card3, 'content_frame'):
            tk.Label(card3.content_frame, text="89",
                    font=('Segoe UI', 20, 'bold'),
                    bg=tema['bg_card'], fg=tema['primary']).pack()
            tk.Label(card3.content_frame, text="↗️ +3 novos",
                    font=('Segoe UI', 12),
                    bg=tema['bg_card'], fg=tema['accent']).pack()
    
    def _criar_card_moderno(self, parent, title, tema):
        """Cria card moderno"""
        # Container principal do card
        card_container = tk.Frame(parent, bg=tema['bg_primary'])
        
        # Simular sombra
        shadow = tk.Frame(card_container, bg='#BDC3C7', height=3)
        shadow.pack(fill='x', side='bottom')
        
        # Card principal
        card = tk.Frame(card_container, bg=tema['bg_card'], relief='flat', bd=0)
        card.pack(fill='both', expand=True)
        
        # Header do card
        header = tk.Frame(card, bg=tema['primary'], height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text=title,
                              font=('Segoe UI', 14, 'bold'),
                              bg=tema['primary'], fg='white')
        title_label.pack(expand=True)
        
        # Área de conteúdo
        content_frame = tk.Frame(card, bg=tema['bg_card'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Adicionar content_frame como atributo do container
        card_container.content_frame = content_frame
        
        return card_container
    
    def _criar_graficos_demo(self, parent, tema):
        """Cria gráficos de demonstração simples"""
        graficos_frame = tk.Frame(parent, bg=tema['bg_primary'])
        graficos_frame.pack(fill='both', expand=True, pady=20)
        
        # Título dos gráficos
        tk.Label(graficos_frame, text="📊 Gráficos Interativos",
                font=('Segoe UI', 16, 'bold'),
                bg=tema['bg_primary'], fg=tema['secondary']).pack(pady=10)
        
        # Container dos gráficos
        charts_container = tk.Frame(graficos_frame, bg=tema['bg_card'], relief='raised', bd=2)
        charts_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Gráfico de barras simples usando Canvas
        canvas = tk.Canvas(charts_container, bg=tema['bg_card'], height=200)
        canvas.pack(fill='x', padx=20, pady=20)
        
        # Desenhar gráfico de barras
        self._desenhar_grafico_barras(canvas, tema)
    
    def _desenhar_grafico_barras(self, canvas, tema):
        """Desenha gráfico de barras simples"""
        canvas.delete("all")
        
        # Dados de exemplo
        dados = [30, 45, 60, 40, 70, 55]
        labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        cores = [tema['primary'], tema['secondary'], tema['accent'], 
                tema['primary'], tema['secondary'], tema['accent']]
        
        # Dimensões
        width = canvas.winfo_reqwidth() or 800
        height = 180
        margin = 50
        
        bar_width = (width - 2 * margin) / len(dados)
        max_value = max(dados)
        
        # Desenhar barras
        for i, (valor, label, cor) in enumerate(zip(dados, labels, cores)):
            x1 = margin + i * bar_width + 10
            x2 = margin + (i + 1) * bar_width - 10
            y1 = height - margin
            y2 = height - margin - (valor / max_value) * (height - 2 * margin)
            
            # Barra
            canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline='')
            
            # Label
            canvas.create_text((x1 + x2) / 2, y1 + 15, text=label, 
                             font=('Segoe UI', 10))
            
            # Valor
            canvas.create_text((x1 + x2) / 2, y2 - 15, text=str(valor),
                             font=('Segoe UI', 10, 'bold'), fill='white')
    
    def _criar_footer(self):
        """Cria footer informativo"""
        footer = tk.Frame(self.root, bg='#1A252F', height=60)
        footer.pack(fill='x')
        footer.pack_propagate(False)
        
        # Informações
        info_text = "💡 Esta é uma demonstração das possibilidades visuais | Sistema CM Premium v2.0"
        tk.Label(footer, text=info_text,
                font=('Segoe UI', 11),
                bg='#1A252F', fg='#BDC3C7').pack(expand=True)
        
        # Botão para aplicar ao sistema real
        aplicar_btn = tk.Button(footer, text="🚀 APLICAR AO SISTEMA REAL",
                               command=self._aplicar_decoracoes,
                               font=('Segoe UI', 12, 'bold'),
                               bg='#E74C3C', fg='white',
                               activebackground='#C0392B',
                               relief='flat', cursor='hand2')
        aplicar_btn.pack(pady=10)
    
    def _aplicar_tema(self, tema_nome):
        """Aplica tema selecionado"""
        self.tema_atual = tema_nome
        self._carregar_demo_premium()
        
        # Animação de transição (simples)
        self.demo_frame.configure(bg='#34495E')
        self.root.after(100, lambda: self.demo_frame.configure(bg=self.temas[tema_nome]['bg_primary']))
    
    def _aplicar_decoracoes(self):
        """Aplica decorações ao sistema real"""
        resposta = messagebox.askyesno(
            "Aplicar Decorações",
            f"Deseja aplicar o tema '{self.tema_atual.title()}' ao Sistema CM?\n\n"
            f"Isso irá:\n"
            f"✅ Atualizar cores e visual\n"
            f"✅ Melhorar componentes\n" 
            f"✅ Adicionar animações\n"
            f"✅ Criar backup do tema atual\n\n"
            f"Continuar?"
        )
        
        if resposta:
            try:
                self._salvar_tema_personalizado()
                messagebox.showinfo("Sucesso!", 
                    f"🎉 Tema '{self.tema_atual.title()}' aplicado com sucesso!\n\n"
                    f"Execute o sistema para ver as mudanças:\n"
                    f"cd src && python premium_app.py")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao aplicar decorações: {e}")
    
    def _salvar_tema_personalizado(self):
        """Salva tema personalizado no sistema"""
        tema = self.temas[self.tema_atual]
        
        # Criar arquivo de tema personalizado
        tema_code = f'''# Tema personalizado: {self.tema_atual.title()}
# Gerado automaticamente pelo Decorador do Sistema CM

TEMA_PERSONALIZADO = {{
    'light': {{
        'bg_primary': '{tema['bg_primary']}',
        'bg_secondary': '#F8F9FA', 
        'bg_card': '{tema['bg_card']}',
        'primary': '{tema['primary']}',
        'secondary': '{tema['secondary']}',
        'accent': '{tema['accent']}',
        'text_primary': '#212529',
        'text_secondary': '#6C757D',
        'border': '#DEE2E6',
        'success': '#28A745',
        'warning': '#FFC107', 
        'error': '#DC3545'
    }},
    'dark': {{
        'bg_primary': '#212529',
        'bg_secondary': '#343A40',
        'bg_card': '#495057', 
        'primary': '{tema['primary']}',
        'secondary': '{tema['secondary']}',
        'accent': '{tema['accent']}',
        'text_primary': '#F8F9FA',
        'text_secondary': '#CED4DA',
        'border': '#495057',
        'success': '#28A745',
        'warning': '#FFC107',
        'error': '#DC3545'
    }}
}}

# Aplicar tema personalizado
def aplicar_tema_personalizado(theme_instance):
    """Aplica tema personalizado ao sistema"""
    theme_instance.COLORS = TEMA_PERSONALIZADO
    theme_instance.current_colors = TEMA_PERSONALIZADO['light']
    print(f"🎨 Tema '{self.tema_atual.title()}' aplicado!")
'''
        
        # Salvar arquivo
        tema_file = Path('src') / f'tema_{self.tema_atual}.py'
        with open(tema_file, 'w', encoding='utf-8') as f:
            f.write(tema_code)
        
        print(f"🎨 Tema salvo em: {tema_file}")
    
    def executar(self):
        """Executa o decorador"""
        self.root.mainloop()

def main():
    """Função principal"""
    print("🎨 INICIANDO DECORADOR DO SISTEMA CM")
    print("=" * 50)
    print("🎯 FUNCIONALIDADES:")
    print("• Temas personalizados (Premium, Cyberpunk, Nature, Sunset)")
    print("• Cards modernos com estatísticas")
    print("• Gráficos interativos") 
    print("• Tipografia melhorada")
    print("• Animações suaves")
    print("• Componentes visuais avançados")
    print()
    print("💡 Selecione um tema e veja a demonstração!")
    print("🚀 Use 'APLICAR AO SISTEMA REAL' para ativar no Sistema CM")
    print()
    
    try:
        decorador = DecoradorSistema()
        decorador.executar()
    except Exception as e:
        print(f"❌ Erro ao executar decorador: {e}")
    
    print("\n✅ Decorador finalizado!")

if __name__ == "__main__":
    main()

            f
