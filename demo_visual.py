#!/usr/bin/env python3
"""
🎨 DEMONSTRAÇÃO VISUAL - SISTEMA CM PREMIUM

Este arquivo demonstra como o código ficará bonito com as extensões visuais:
- Sintaxe colorida profissional
- TODOs e comentários destacados
- Parênteses coloridos por níveis
- Indentação com cores do arco-íris
- Ícones bonitos para arquivos
"""

import tkinter as tk
from pathlib import Path
import json
from datetime import datetime

# TODO: Implementar validação de dados
# FIXME: Corrigir bug na formatação de valores
# NOTE: Usar este padrão para todos os módulos

class VisualDemo:
    """
    🎨 Classe de demonstração visual
    
    Esta classe mostra como o código Python fica mais bonito e legível
    com as configurações visuais aplicadas no VS Code.
    """
    
    def __init__(self, tema='premium'):
        # ? Comentário de pergunta - azul
        # ! Comentário de alerta - vermelho  
        # * Comentário de destaque - verde
        # TODO: Adicionar mais temas
        
        self.tema = tema
        self.cores = {
            'primary': '#3498DB',      # 🔵 Azul principal
            'secondary': '#2C3E50',    # 🔘 Azul escuro
            'success': '#27AE60',      # 🟢 Verde sucesso
            'warning': '#F39C12',      # 🟡 Laranja aviso
            'danger': '#E74C3C',       # 🔴 Vermelho perigo
        }
        
    def processar_dados(self, dados):
        """
        🔄 Processa dados com diferentes tipos
        
        Args:
            dados: Lista de dados para processar
        
        Returns:
            dict: Dados processados com estatísticas
        """
        if not dados:  # Verificação simples
            return {"erro": "Dados vazios"}
        
        # Processamento com múltiplos níveis de parênteses (coloridos!)
        resultado = {
            'total': len(dados),
            'processados': len([
                item for item in dados 
                if (
                    isinstance(item, dict) and 
                    'valor' in item and 
                    (item['valor'] > 0)
                )
            ]),
            'timestamp': datetime.now().isoformat()
        }
        
        return resultado
    
    def aplicar_tema_visual(self, widget):
        """🎨 Aplica tema visual a um widget Tkinter"""
        
        # Diferentes tipos de dados para mostrar cores
        configuracao = {
            "background": self.cores['primary'],    # String
            "foreground": "#FFFFFF",                # String hex
            "font": ("Segoe UI", 12, "bold"),      # Tuple
            "padding": 10,                          # Número inteiro
            "opacity": 0.95,                       # Número float
            "active": True,                        # Boolean
            "items": [1, 2, 3, 4, 5],             # Lista
        }
        
        # Aplicar configurações com diferentes estruturas
        for propriedade, valor in configuracao.items():
            if hasattr(widget, 'configure'):
                try:
                    widget.configure({propriedade: valor})
                except Exception as e:
                    print(f"❌ Erro ao configurar {propriedade}: {e}")
                    # FIXME: Melhorar tratamento de erro
    
    def exemplo_formatacao_complexa(self):
        """
        💎 Exemplo de código com formatação complexa
        
        Mostra como diferentes construções Python ficam coloridas:
        - Comprehensions aninhadas
        - Múltiplos níveis de parênteses  
        - Diferentes tipos de comentários
        - Strings formatadas
        """
        
        # * Comprehension complexa com múltiplos níveis
        matriz_processada = [
            [
                f"Item_{i}_{j}" if (i % 2 == 0 and j % 2 == 0) 
                else f"Alt_{i}_{j}"
                for j in range(5)
                if (j > 0)  # ! Condição importante
            ]
            for i in range(3)
            if (i < 10)  # ? Limite necessário?
        ]
        
        # TODO: Otimizar esta função
        dados_aninhados = {
            'usuarios': [
                {
                    'id': i,
                    'nome': f'Usuario_{i}',
                    'ativo': (i % 2 == 0),
                    'configuracoes': {
                        'tema': 'dark' if (i % 3 == 0) else 'light',
                        'permissoes': [
                            'read', 'write', 'admin'
                        ][:(i % 3) + 1]
                    }
                }
                for i in range(1, 6)
            ],
            'meta': {
                'total': 5,
                'criado_em': datetime.now(),
                'versao': '2.0.0'
            }
        }
        
        return {
            'matriz': matriz_processada,
            'dados': dados_aninhados,
            'status': '✅ Processamento concluído'
        }

def main():
    """
    🚀 Função principal de demonstração
    
    Execute este arquivo no VS Code para ver:
    - Código Python com cores profissionais
    - TODOs destacados em laranja
    - Comentários categorizados por cores
    - Parênteses coloridos por níveis
    - Indentação com arco-íris lateral
    """
    
    print("🎨 DEMONSTRAÇÃO VISUAL ATIVA")
    print("=" * 50)
    
    # Criar instância da demo
    demo = VisualDemo(tema='premium')
    
    # Dados de exemplo
    dados_teste = [
        {'valor': 100, 'nome': 'Item 1'},
        {'valor': 200, 'nome': 'Item 2'},
        {'valor': -50, 'nome': 'Item 3'},  # Valor negativo
        {'nome': 'Item 4'},  # Sem valor
    ]
    
    # Processar dados
    resultado = demo.processar_dados(dados_teste)
    print(f"📊 Resultado: {resultado}")
    
    # Exemplo complexo
    complexo = demo.exemplo_formatacao_complexa()
    print(f"💎 Dados complexos processados: {len(complexo)} itens")
    
    print("\n🎯 OBSERVE NO VS CODE:")
    print("• Sintaxe colorida profissionalmente")
    print("• TODOs, FIXMEs, NOTEs destacados")
    print("• Parênteses coloridos por níveis")
    print("• Strings e números com cores específicas")
    print("• Comentários categorizados por símbolos")
    print("• Indentação lateral colorida")
    
    print("\n✨ VISUAL PREMIUM ATIVO!")

if __name__ == "__main__":
    # ! Execute no VS Code para ver o resultado visual completo
    main()
