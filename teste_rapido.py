#!/usr/bin/env python3
"""
🧪 TESTE RÁPIDO - Sistema CM Premium

Script para testar rapidamente todas as funcionalidades principais.
Execute: python teste_rapido.py
"""

import os
import sys
import subprocess
from pathlib import Path

def print_section(title):
    """Imprime seção formatada"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print('='*60)

def check_file_exists(file_path, description):
    """Verifica se arquivo existe"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NÃO ENCONTRADO")
        return False

def check_directory_exists(dir_path, description):
    """Verifica se diretório existe"""
    if Path(dir_path).exists():
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"⚠️  {description}: {dir_path} - SERÁ CRIADO")
        Path(dir_path).mkdir(exist_ok=True)
        return True

def test_imports():
    """Testa importações essenciais"""
    print_section("TESTANDO IMPORTAÇÕES")
    
    modules_to_test = [
        ('tkinter', 'Interface gráfica'),
        ('PIL', 'Processamento de imagens'),
        ('matplotlib', 'Gráficos'),
        ('numpy', 'Cálculos numéricos'),
        ('sqlite3', 'Banco de dados')
    ]
    
    all_ok = True
    for module, desc in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {desc}: {module}")
        except ImportError:
            print(f"❌ {desc}: {module} - NÃO INSTALADO")
            all_ok = False
    
    return all_ok

def test_file_structure():
    """Testa estrutura de arquivos"""
    print_section("TESTANDO ESTRUTURA DE ARQUIVOS")
    
    files_to_check = [
        ('decorar_sistema.py', 'Decorador de temas'),
        ('src/premium_app.py', 'App premium'),
        ('src/premium_login.py', 'Login premium'),
        ('src/premium_main_window.py', 'Janela principal'),
        ('src/premium_theme.py', 'Tema premium'),
        ('src/db.py', 'Banco de dados'),
        ('requirements.txt', 'Dependências'),
        ('GUIA_COMPLETO_TESTES.md', 'Guia de testes')
    ]
    
    all_ok = True
    for file_path, desc in files_to_check:
        if not check_file_exists(file_path, desc):
            all_ok = False
    
    # Verificar diretórios
    dirs_to_check = [
        ('user_photos', 'Fotos de usuários'),
        ('client_photos', 'Fotos de clientes'),
        ('src', 'Código fonte')
    ]
    
    for dir_path, desc in dirs_to_check:
        check_directory_exists(dir_path, desc)
    
    return all_ok

def test_database():
    """Testa conexão com banco de dados"""
    print_section("TESTANDO BANCO DE DADOS")
    
    try:
        # Tentar importar e inicializar DB
        sys.path.insert(0, 'src')
        from db import inicializar_banco
        
        inicializar_banco()
        print("✅ Banco de dados inicializado com sucesso")
        
        # Verificar se arquivo foi criado
        if Path('sistema.db').exists():
            print("✅ Arquivo sistema.db criado")
            return True
        else:
            print("❌ Arquivo sistema.db não foi criado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return False

def test_premium_imports():
    """Testa importações do sistema premium"""
    print_section("TESTANDO SISTEMA PREMIUM")
    
    try:
        sys.path.insert(0, 'src')
        
        # Testar imports principais
        from premium_theme import PremiumTheme
        print("✅ PremiumTheme importado")
        
        from premium_login import PremiumLoginWindow
        print("✅ PremiumLoginWindow importado")
        
        from premium_main_window import PremiumMainWindow
        print("✅ PremiumMainWindow importado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao importar sistema premium: {e}")
        return False

def run_quick_tests():
    """Executa testes rápidos"""
    print("🧪 INICIANDO TESTES RÁPIDOS DO SISTEMA CM")
    print(f"Diretório atual: {os.getcwd()}")
    
    results = []
    
    # Teste 1: Importações
    results.append(test_imports())
    
    # Teste 2: Estrutura de arquivos
    results.append(test_file_structure())
    
    # Teste 3: Banco de dados
    results.append(test_database())
    
    # Teste 4: Sistema premium
    results.append(test_premium_imports())
    
    # Resultado final
    print_section("RESULTADO FINAL")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Execute: python decorar_sistema.py")
        print("2. Execute: cd src && python premium_app.py")
        print("3. Teste login: admin / 1234")
        print("4. Navegue pelas funcionalidades")
        print("5. Consulte: GUIA_COMPLETO_TESTES.md")
    else:
        print(f"⚠️  {passed}/{total} TESTES PASSARAM")
        print("\n🔧 CORREÇÕES NECESSÁRIAS:")
        if not results[0]:
            print("- Instale dependências: pip install -r requirements.txt")
        if not results[1]:
            print("- Verifique estrutura de arquivos")
        if not results[2]:
            print("- Corrija problemas do banco de dados")
        if not results[3]:
            print("- Corrija imports do sistema premium")
    
    return passed == total

def main():
    """Função principal"""
    try:
        success = run_quick_tests()
        
        if success:
            print("\n🚀 SISTEMA PRONTO PARA USO!")
            
            # Perguntar se quer executar sistema
            try:
                resposta = input("\n❓ Deseja executar o sistema premium agora? (s/n): ").lower()
                if resposta in ['s', 'sim', 'y', 'yes']:
                    print("\n🚀 Executando sistema premium...")
                    os.chdir('src')
                    subprocess.run([sys.executable, 'premium_app.py'])
            except KeyboardInterrupt:
                print("\n👋 Teste cancelado pelo usuário")
        else:
            print("\n❌ CORRIJA OS PROBLEMAS ANTES DE CONTINUAR")
            
    except Exception as e:
        print(f"\n💥 ERRO DURANTE TESTE: {e}")
        return False
    
    return success

if __name__ == "__main__":
    main()
