#!/usr/bin/env python3
"""
🎨 SETUP VISUAL AUTOMÁTICO - SISTEMA CM PREMIUM

Este script configura automaticamente o VS Code com:
- Temas modernos e profissionais
- Extensões visuais essenciais  
- Ícones bonitos para arquivos
- Configurações otimizadas para Python
- Cores e highlights para melhor legibilidade

Execução: python setup_visual.py
"""

import subprocess
import sys
import os
from pathlib import Path

class VisualSetup:
    def __init__(self):
        self.project_path = Path(__file__).parent
        self.vscode_path = self.project_path / '.vscode'
        
        # 🎨 Extensões visuais essenciais
        self.extensions = [
            # TEMAS E ÍCONES
            'zhuangtongfa.material-theme',          # One Dark Pro
            'pkief.material-icon-theme',            # Material Icons  
            'dracula-theme.theme-dracula',          # Dracula Theme
            
            # PYTHON
            'ms-python.python',                     # Python oficial
            'ms-python.black-formatter',            # Formatação
            'ms-python.pylint',                     # Linting
            
            # VISUAL E CORES
            'oderwat.indent-rainbow',               # Indentação colorida
            'naumovs.color-highlight',              # Destaque de cores
            'wayou.vscode-todo-highlight',          # TODOs coloridos
            'aaron-bond.better-comments',           # Comentários melhorados
            
            # PRODUTIVIDADE
            'formulahendry.auto-rename-tag',        # Renomear tags
            'streetsidesoftware.code-spell-checker', # Corretor
            'eamodio.gitlens',                      # Git avançado
            'ms-vscode.vscode-json',                # JSON melhorado
        ]
    
    def check_vscode_installed(self):
        """Verifica se VS Code está instalado"""
        try:
            result = subprocess.run(['code', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                print(f"✅ VS Code encontrado: {version}")
                return True
            else:
                print("❌ VS Code não encontrado no PATH")
                return False
        except FileNotFoundError:
            print("❌ VS Code não instalado ou não está no PATH")
            print("📥 Baixe em: https://code.visualstudio.com/")
            return False
    
    def install_extension(self, extension):
        """Instala uma extensão específica"""
        try:
            print(f"📦 Instalando: {extension}")
            result = subprocess.run(
                ['code', '--install-extension', extension, '--force'],
                capture_output=True, text=True, timeout=60
            )
            
            if result.returncode == 0:
                print(f"   ✅ {extension} instalado")
                return True
            else:
                print(f"   ❌ Erro ao instalar {extension}")
                print(f"   📝 {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timeout ao instalar {extension}")
            return False
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return False
    
    def install_all_extensions(self):
        """Instala todas as extensões visuais"""
        print("\n🎨 INSTALANDO EXTENSÕES VISUAIS...")
        print("=" * 50)
        
        success_count = 0
        total_count = len(self.extensions)
        
        for extension in self.extensions:
            if self.install_extension(extension):
                success_count += 1
        
        print("\n" + "=" * 50)
        print(f"📊 RESULTADO: {success_count}/{total_count} extensões instaladas")
        
        if success_count == total_count:
            print("🏆 TODAS AS EXTENSÕES INSTALADAS COM SUCESSO!")
        elif success_count > 0:
            print("⚠️ Algumas extensões falharam, mas o básico está funcionando")
        else:
            print("❌ Nenhuma extensão foi instalada")
        
        return success_count > 0
    
    def open_project(self):
        """Abre o projeto no VS Code"""
        try:
            print("\n🚀 Abrindo projeto no VS Code...")
            subprocess.run(['code', '.'], check=True)
            print("✅ Projeto aberto no VS Code!")
            return True
        except Exception as e:
            print(f"❌ Erro ao abrir VS Code: {e}")
            return False
    
    def show_instructions(self):
        """Mostra instruções finais"""
        print("\n" + "🎯 CONFIGURAÇÃO CONCLUÍDA!" + "\n")
        print("=" * 60)
        
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. VS Code abriu automaticamente com o projeto")
        print("2. Tema será aplicado automaticamente")
        print("3. Extensões estarão disponíveis")
        
        print("\n🎨 PARA PERSONALIZAR:")
        print("• Ctrl+Shift+P → 'Theme: Color Theme'")
        print("• Escolha: One Dark Pro, Dracula, ou Material Theme")
        print("• Ctrl+Shift+P → 'Theme: File Icon Theme'")
        print("• Escolha: Material Icon Theme")
        
        print("\n🐍 ESPECÍFICO PARA PYTHON:")
        print("• Formatação automática: Salvar (Ctrl+S)")
        print("• TODOs destacados automaticamente")
        print("• Cores de sintaxe otimizadas")
        
        print("\n📁 SEUS ARQUIVOS COM ÍCONES:")
        print("🐍 .py → Ícone Python")
        print("📋 .json → Ícone JSON")
        print("📖 .md → Ícone Markdown")
        print("⚙️ .vscode → Ícone configuração")
        
        print("\n🌈 VISUAL MELHORADO:")
        print("• Parênteses coloridos por níveis")
        print("• Indentação com cores do arco-íris")
        print("• TODOs, FIXMEs destacados")
        print("• Cores de código otimizadas")
        
        print("\n" + "=" * 60)
        print("🚀 SEU CÓDIGO AGORA TEM APARÊNCIA PROFISSIONAL!")
    
    def run(self):
        """Executa todo o setup visual"""
        print("🎨 SISTEMA CM - SETUP VISUAL AUTOMÁTICO")
        print("=" * 60)
        
        # Verificar VS Code
        if not self.check_vscode_installed():
            return False
        
        # Instalar extensões
        extensions_ok = self.install_all_extensions()
        
        if extensions_ok:
            # Abrir projeto
            self.open_project()
            
            # Instruções finais
            self.show_instructions()
            
            return True
        else:
            print("\n❌ Setup falhou. Verifique se VS Code está funcionando.")
            return False

def main():
    """Função principal"""
    setup = VisualSetup()
    success = setup.run()
    
    if success:
        print("\n🎉 SETUP VISUAL CONCLUÍDO COM SUCESSO!")
        print("💡 Reinicie o VS Code se necessário para aplicar todos os temas.")
        return 0
    else:
        print("\n💔 Setup não pôde ser concluído.")
        print("🔧 Instale manualmente as extensões:")
        for ext in setup.extensions:
            print(f"   code --install-extension {ext}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
