#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema CM - Módulo de Interface Gráfica
Interface principal do sistema com Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import hashlib
import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import csv
import re
from decimal import Decimal, InvalidOperation
import uuid

# Garantir que os módulos no mesmo diretório possam ser importados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Regex para validações
TELEFONE_REGEX_10 = re.compile(r"^\(\d{2}\) \d{4}-\d{4}$")  # (11) 1234-5678
TELEFONE_REGEX_11 = re.compile(r"^\(\d{2}\) \d{5}-\d{4}$")  # (11) 12345-6789
DATA_NASC_REGEX = re.compile(r"^\d{2}/\d{2}/\d{4}$")  # dd/mm/aaaa

@dataclass
class CadastroCliente:
    """Classe para representar um cliente com campos expandidos"""
    # Dados pessoais básicos
    nome: str = ""
    data_nascimento: str = ""
    cpf: str = ""
    identidade: str = ""
    email: str = ""
    estado_civil: str = ""
    profissao: str = ""
    
    # Endereço
    endereco: str = ""
    cidade: str = ""
    estado: str = ""
    cep: str = ""
    
    # Contatos obrigatórios (3 tipos)
    telefone_residencial: str = ""
    telefone_celular: str = ""
    telefone_comercial: str = ""
    
    # Contatos adicionais
    telefones_adicionais: List[str] = None
    
    # Trabalho
    onde_trabalha: str = ""
    telefone_trabalho: str = ""
    
    # Financeiro
    renda_mensal: Decimal = Decimal('0')
    limite_credito: Decimal = Decimal('0')
    
    # Referências
    referencias: List[Dict[str, str]] = None  # [{"nome": "João", "telefone": "11999999999", "parentesco": "Pai"}]
    
    # Outros
    observacao: str = ""
    observacoes: str = ""  # Compatibilidade com dados existentes
    loja_cadastro: str = ""
    id: str = ""
    
    def __post_init__(self):
        if self.telefones_adicionais is None:
            self.telefones_adicionais = []
        if self.referencias is None:
            self.referencias = []
        if not isinstance(self.renda_mensal, Decimal):
            try:
                self.renda_mensal = Decimal(str(self.renda_mensal)) if self.renda_mensal else Decimal('0')
            except (InvalidOperation, ValueError):
                logging.warning(f"Valor inválido para renda_mensal: {self.renda_mensal}, usando 0")
                self.renda_mensal = Decimal('0')
        if not isinstance(self.limite_credito, Decimal):
            try:
                self.limite_credito = Decimal(str(self.limite_credito)) if self.limite_credito else Decimal('0')
            except (InvalidOperation, ValueError):
                logging.warning(f"Valor inválido para limite_credito: {self.limite_credito}, usando 0")
                self.limite_credito = Decimal('0')
        
        # Calcular limite de crédito automaticamente (30% da renda)
        if self.renda_mensal > 0 and self.limite_credito == 0:
            self.limite_credito = self.renda_mensal * Decimal('0.30')

@dataclass
class Usuario:
    """Classe para representar um usuário do sistema"""
    username: str
    password_hash: str
    is_admin: bool = False

@dataclass
class Venda:
    """Classe para representar uma venda"""
    produto: str
    quantidade: int
    total: Decimal
    timestamp: str
    codigo_loja: str = None

    def __post_init__(self):
        if not isinstance(self.total, Decimal):
            try:
                self.total = Decimal(str(self.total)) if self.total else Decimal('0')
            except (InvalidOperation, ValueError):
                logging.warning(f"Valor inválido para total: {self.total}, usando 0")
                self.total = Decimal('0')

@dataclass
class Pagamento:
    """Classe para representar um pagamento"""
    descricao: str
    valor: Decimal
    tipo: str
    timestamp: str

    def __post_init__(self):
        if not isinstance(self.valor, Decimal):
            try:
                self.valor = Decimal(str(self.valor)) if self.valor else Decimal('0')
            except (InvalidOperation, ValueError):
                logging.warning(f"Valor inválido para valor: {self.valor}, usando 0")
                self.valor = Decimal('0')

class SistemaAutenticacao:
    """Sistema de autenticação de usuários"""
    
    def __init__(self, arquivo_usuarios: str = "usuarios.json"):
        self.arquivo_usuarios = arquivo_usuarios
        self.usuarios = self._carregar_usuarios()
        self.usuario_logado = None
        
    def _carregar_usuarios(self) -> Dict[str, Usuario]:
        """Carrega usuários do arquivo JSON"""
        try:
            if Path(self.arquivo_usuarios).exists():
                with open(self.arquivo_usuarios, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        username: Usuario(
                            username=username,
                            password_hash=user_data if isinstance(user_data, str) else user_data.get('password_hash', ''),
                            is_admin=user_data.get('is_admin', False) if isinstance(user_data, dict) else False
                        ) 
                        for username, user_data in data.items()
                    }
            else:
                # Criar usuário admin padrão
                admin_user = Usuario(
                    username="admin",
                    password_hash=self._hash_password("1234"),
                    is_admin=True
                )
                usuarios = {"admin": admin_user}
                self._salvar_usuarios(usuarios)
                return usuarios
        except Exception as e:
            logging.error(f"Erro ao carregar usuários: {e}")
            return {}
    
    def _salvar_usuarios(self, usuarios: Dict[str, Usuario]):
        """Salva usuários no arquivo JSON"""
        try:
            data = {
                username: {
                    "password_hash": user.password_hash,
                    "is_admin": user.is_admin
                }
                for username, user in usuarios.items()
            }
            self._gravar_json_atomico(self.arquivo_usuarios, data)
        except Exception as e:
            logging.error(f"Erro ao salvar usuários: {e}")

    @staticmethod
    def _gravar_json_atomico(caminho: str, conteudo: Dict[str, Any]):
        """Grava JSON de forma atômica usando arquivo temporário"""
        import json, tempfile, os
        dir_path = os.path.dirname(caminho) or "."
        with tempfile.NamedTemporaryFile("w", dir=dir_path, delete=False, encoding="utf-8") as tmp:
            json.dump(conteudo, tmp, ensure_ascii=False, indent=4)
            temp_name = tmp.name
        os.replace(temp_name, caminho)
    
    def _hash_password(self, password: str) -> str:
        """Gera hash da senha usando PBKDF2"""
        import hashlib
        import secrets
        
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 200000)
        return f"{password_hash.hex()}$200000${salt}"
    
    def verificar_senha(self, password: str, stored_hash: str) -> bool:
        """Verifica se a senha está correta"""
        try:
            parts = stored_hash.split('$')
            if len(parts) != 3:
                return False
            
            stored_hash_hex, iterations, salt = parts
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), int(iterations))
            return password_hash.hex() == stored_hash_hex
        except:
            return False
    
    def login(self, username: str, password: str) -> bool:
        """Realiza login do usuário"""
        if username in self.usuarios:
            user = self.usuarios[username]
            if self.verificar_senha(password, user.password_hash):
                self.usuario_logado = user
                logging.info(f"Usuário '{username}' logou no sistema")
                return True
        return False
    
    def logout(self):
        """Realiza logout do usuário"""
        if self.usuario_logado:
            logging.info(f"Usuário '{self.usuario_logado.username}' saiu do sistema")
            self.usuario_logado = None
    
    def criar_usuario(self, username: str, password: str, is_admin: bool = False) -> bool:
        """Cria um novo usuário"""
        if username in self.usuarios:
            return False
        
        new_user = Usuario(
            username=username,
            password_hash=self._hash_password(password),
            is_admin=is_admin
        )
        self.usuarios[username] = new_user
        self._salvar_usuarios(self.usuarios)
        logging.info(f"Usuário '{username}' criado com sucesso")
        return True

class GerenciadorDados:
    """Gerenciador de dados do sistema"""
    
    def __init__(self, arquivo_dados: str = "dados_sistema.json"):
        self.arquivo_dados = arquivo_dados
        self.dados = self._carregar_dados()
        
    def _carregar_dados(self) -> Dict[str, Any]:
        """Carrega dados do arquivo JSON"""
        try:
            if Path(self.arquivo_dados).exists():
                try:
                    with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Validar estrutura básica dos dados
                        if not isinstance(data, dict):
                            logging.error(f"Formato de dados inválido: {type(data)}")
                            return self._criar_dados_iniciais()
                        
                        # Garantir que campos obrigatórios existam
                        for campo in ['versao', 'cadastros', 'lojas']:
                            if campo not in data:
                                data[campo] = [] if campo != 'versao' else 1
                        
                        # Converter listas de dicionários para objetos
                        if 'cadastros' in data:
                            clientes_convertidos = []
                            for cliente in data['cadastros']:
                                try:
                                    # Verificar se é formato antigo (com 'idade') ou novo
                                    if isinstance(cliente, dict):  # Garantir que é um dicionário
                                        if 'idade' in cliente:
                                            # Formato antigo - converter para novo
                                            cliente_novo = CadastroCliente(
                                                nome=cliente.get('nome', ''),
                                                data_nascimento=cliente.get('data_nascimento', ''),
                                                cpf=cliente.get('cpf', ''),
                                                identidade=cliente.get('identidade', ''),
                                                email=cliente.get('email', ''),
                                                estado_civil=cliente.get('estado_civil', ''),
                                                profissao=cliente.get('profissao', ''),
                                                endereco=cliente.get('endereco', ''),
                                                telefone_residencial=cliente.get('telefone_residencial', ''),
                                                telefone_celular=cliente.get('telefone_celular', ''),
                                                telefone_comercial=cliente.get('telefone_comercial', ''),
                                                telefones_adicionais=cliente.get('telefones_adicionais', []),
                                                onde_trabalha=cliente.get('onde_trabalha', ''),
                                                telefone_trabalho=cliente.get('telefone_trabalho', ''),
                                                renda_mensal=self._converter_para_decimal(cliente.get('renda_mensal', 0)),
                                                limite_credito=self._converter_para_decimal(cliente.get('limite_credito', 0)),
                                                referencias=cliente.get('referencias', []),
                                                observacao=cliente.get('observacao', ''),
                                                loja_cadastro=cliente.get('loja_cadastro', ''),
                                                id=cliente.get('id', '')
                                            )
                                        else:
                                            # Formato novo
                                            # Garantir que valores decimais são tratados corretamente
                                            if 'renda_mensal' in cliente and not isinstance(cliente['renda_mensal'], Decimal):
                                                cliente['renda_mensal'] = self._converter_para_decimal(cliente['renda_mensal'])
                                            if 'limite_credito' in cliente and not isinstance(cliente['limite_credito'], Decimal):
                                                cliente['limite_credito'] = self._converter_para_decimal(cliente['limite_credito'])
                                            cliente_novo = CadastroCliente(**cliente)
                                        clientes_convertidos.append(cliente_novo)
                                except Exception as e:
                                    logging.warning(f"Erro ao converter cliente: {e}")
                                    continue
                            data['cadastros'] = clientes_convertidos
                        
                        # Tratamento para vendas
                        if 'historico_vendas' in data:
                            vendas_convertidas = []
                            for venda in data['historico_vendas']:
                                try:
                                    if isinstance(venda, dict):
                                        # Garantir que total é Decimal
                                        if 'total' in venda and not isinstance(venda['total'], Decimal):
                                            venda['total'] = self._converter_para_decimal(venda['total'])
                                        vendas_convertidas.append(Venda(**venda))
                                except Exception as e:
                                    logging.error(f"Erro ao converter venda: {e}")
                            data['historico_vendas'] = vendas_convertidas
                        
                        # Tratamento para pagamentos
                        if 'pagamentos' in data:
                            pagamentos_convertidos = []
                            for pag in data['pagamentos']:
                                try:
                                    if isinstance(pag, dict):
                                        # Garantir que valor é Decimal
                                        if 'valor' in pag and not isinstance(pag['valor'], Decimal):
                                            pag['valor'] = self._converter_para_decimal(pag['valor'])
                                        pagamentos_convertidos.append(Pagamento(**pag))
                                except Exception as e:
                                    logging.error(f"Erro ao converter pagamento: {e}")
                            data['pagamentos'] = pagamentos_convertidos
                        
                        return data
                except json.JSONDecodeError as e:
                    logging.error(f"Arquivo JSON corrompido: {e}")
                    return self._criar_dados_iniciais()
            else:
                return self._criar_dados_iniciais()
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {e}")
            return self._criar_dados_iniciais()
    
    def _converter_para_decimal(self, valor):
        """Converte valor para Decimal de forma segura"""
        if valor is None:
            return Decimal('0')
        if isinstance(valor, Decimal):
            return valor
        try:
            # Garantir que é string e substituir vírgula por ponto
            valor_str = str(valor).replace(',', '.')
            return Decimal(valor_str)
        except (InvalidOperation, ValueError):
            logging.warning(f"Valor inválido para conversão: {valor}")
            return Decimal('0')
    
    def _criar_dados_iniciais(self) -> Dict[str, Any]:
        """Cria estrutura inicial de dados"""
        return {
            "versao": 4,
            "cadastros": [],
            "lojas": [],
            "saldo_caixa": "0.00",
            "saldo_banco": "0.00",
            "saldo_caixa_inicial": "0.00",
            "saldo_banco_inicial": "0.00",
            "historico_vendas": [],
            "pagamentos": [],
            "transferencias": [],
            "auditoria": [],
            "grupos_usuarios": {},
            "metas_loja": {},
            "metas_recebimento": {},
            "textos_contratos": {},
            "permissoes": {}
        }
    
    def salvar_dados(self):
        """Salva dados no arquivo JSON"""
        try:
            # Converter objetos para dicionários
            dados_para_salvar = self.dados.copy()
            if 'cadastros' in dados_para_salvar:
                dados_para_salvar['cadastros'] = [asdict(cliente) for cliente in dados_para_salvar['cadastros']]
            if 'historico_vendas' in dados_para_salvar:
                dados_para_salvar['historico_vendas'] = [asdict(venda) for venda in dados_para_salvar['historico_vendas']]
            if 'pagamentos' in dados_para_salvar:
                dados_para_salvar['pagamentos'] = [asdict(pag) for pag in dados_para_salvar['pagamentos']]
            
            # Gravação atômica
            SistemaAutenticacao._gravar_json_atomico(self.arquivo_dados, dados_para_salvar)
            logging.info("Dados salvos com sucesso")
        except Exception as e:
            logging.error(f"Erro ao salvar dados: {e}")
    
    def adicionar_cliente(self, cliente: CadastroCliente):
        """Adiciona um novo cliente"""
        if not cliente.id:
            cliente.id = self._gerar_id()
        self.dados['cadastros'].append(cliente)
        self._adicionar_auditoria(f"Cliente adicionado: {cliente.nome}")
        self.salvar_dados()
    
    def editar_cliente(self, indice: int, cliente: CadastroCliente):
        """Edita um cliente existente"""
        if 0 <= indice < len(self.dados['cadastros']):
            cliente_antigo = self.dados['cadastros'][indice]
            self.dados['cadastros'][indice] = cliente
            self._adicionar_auditoria(f"Cliente editado: {cliente.id} OLD=({cliente_antigo.nome}, '{cliente_antigo.email}', '{cliente_antigo.endereco}') NEW=({cliente.nome}, '{cliente.email}', '{cliente.endereco}')")
            self.salvar_dados()
    
    def remover_cliente(self, indice: int):
        """Remove um cliente"""
        if 0 <= indice < len(self.dados['cadastros']):
            cliente = self.dados['cadastros'].pop(indice)
            self._adicionar_auditoria(f"Cliente removido: {cliente.nome}")
            self.salvar_dados()
    
    def _gerar_id(self) -> str:
        """Gera um ID único para o cliente"""
        import secrets
        return uuid.uuid4().hex[:16]
    
    def _adicionar_auditoria(self, mensagem: str):
        """Adiciona entrada no log de auditoria"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dados['auditoria'].append(f"{timestamp} - [INFO] {mensagem}")

class SistemaCM:
    """Classe principal do sistema CM"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema CM - Gestão Comercial")
        self.root.geometry("1200x800")
        
        # Inicializar componentes
        self.sistema_auth = SistemaAutenticacao()
        self.gerenciador_dados = GerenciadorDados()
        
        # Ocultar janela principal até login ser realizado
        self.root.withdraw()
        
        # Flag para evitar recriação da interface
        self._interface_criada = False
        
        # Exibir tela de login imediatamente
        self._mostrar_login()
        # self._criar_interface()  # Removido: agora só após login
        
    def _criar_interface(self):
        """Cria a interface principal do sistema"""
        # Menu principal
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Sistema
        menu_sistema = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sistema", menu=menu_sistema)
        menu_sistema.add_command(label="Login", command=self._mostrar_login)
        menu_sistema.add_command(label="Logout", command=self._logout)
        menu_sistema.add_separator()
        menu_sistema.add_command(label="Sair", command=self.root.quit)
        
        # Menu Cadastros
        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)
        menu_cadastros.add_command(label="Novo Cliente", command=self._mostrar_cadastro_clientes)
        menu_cadastros.add_command(label="Lista de Clientes", command=self._mostrar_lista_clientes)
        
        # Menu Relatórios
        menu_relatorios = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Relatórios", menu=menu_relatorios)
        menu_relatorios.add_command(label="Vendas", command=self._mostrar_relatorio_vendas)
        menu_relatorios.add_command(label="Clientes", command=self._mostrar_relatorio_clientes)
        
        # Notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba inicial
        self._criar_aba_inicial()
        
    def _criar_aba_inicial(self):
        """Cria a aba inicial do sistema"""
        frame_inicial = ttk.Frame(self.notebook)
        self.notebook.add(frame_inicial, text="Início")
        
        # Título
        ttk.Label(frame_inicial, text="Sistema CM - Gestão Comercial", 
                 font=("Arial", 16, "bold")).pack(pady=40)
        
        # Botões de ação
        botoes_frame = ttk.Frame(frame_inicial)
        botoes_frame.pack(pady=20)
        
        
    def _mostrar_login(self):
        """Mostra janela de login"""
        JanelaLogin(self.sistema_auth, self._login_sucesso)
        
    def _login_sucesso(self):
        """Callback chamado após login bem-sucedido"""
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        # Criar interface principal se ainda não foi criada
        if not self._interface_criada:
            self._criar_interface()
            self._interface_criada = True
        # Exibir janela principal
        self.root.deiconify()
        
    def _logout(self):
        """Realiza logout do usuário"""
        self.sistema_auth.logout()
        messagebox.showinfo("Logout", "Logout realizado com sucesso!")
        
    def _mostrar_cadastro_clientes(self):
        """Mostra interface de cadastro de clientes"""
        try:
            # Garantir que o módulo esteja no path
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from interface_cadastro_clientes import InterfaceCadastroClientes
            InterfaceCadastroClientes(self.root, self.gerenciador_dados)
        except ImportError as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o módulo de cadastro: {e}")
            logging.error(f"Erro ao importar módulo de cadastro: {e}")
    
    def _mostrar_lista_clientes(self):
        """Mostra interface de lista de clientes"""
        try:
            # Garantir que o módulo esteja no path
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from interface_lista_clientes import InterfaceListaClientes
            InterfaceListaClientes(self.root, self.gerenciador_dados)
        except ImportError as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o módulo de lista: {e}")
            logging.error(f"Erro ao importar módulo de lista: {e}")
        
    def _mostrar_relatorio_vendas(self):
        """Mostra relatórios de vendas"""
        # Implementar relatórios
        messagebox.showinfo("Info", "Relatórios de vendas em desenvolvimento")
        
    def _mostrar_relatorio_clientes(self):
        """Mostra relatórios de clientes"""
        # Implementar relatórios
        messagebox.showinfo("Info", "Relatórios de clientes em desenvolvimento")
        
    def executar(self):
        """Executa o sistema"""
        self.root.mainloop()

class JanelaLogin:
    """Janela de login do sistema"""
    
    def __init__(self, sistema_auth: SistemaAutenticacao, callback_sucesso):
        self.sistema_auth = sistema_auth
        self.callback_sucesso = callback_sucesso
        
        self.janela = tk.Toplevel()
        self.janela.title("Login - Sistema CM")
        self.janela.geometry("300x200")
        self.janela.resizable(False, False)
        self.janela.grab_set()
        
        self._criar_interface()
        
    def _criar_interface(self):
        """Cria a interface da janela de login"""
        # Frame principal
        frame_principal = ttk.Frame(self.janela)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(frame_principal, text="Login", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Usuário
        ttk.Label(frame_principal, text="Usuário:").pack(anchor="w")
        self.entry_usuario = ttk.Entry(frame_principal, width=30)
        self.entry_usuario.pack(pady=(0, 10))
        
        # Senha
        ttk.Label(frame_principal, text="Senha:").pack(anchor="w")
        self.entry_senha = ttk.Entry(frame_principal, width=30, show="*")
        self.entry_senha.pack(pady=(0, 20))
        
        # Botões
        botoes_frame = ttk.Frame(frame_principal)
        botoes_frame.pack(fill="x")
        
        ttk.Button(botoes_frame, text="Login", command=self._fazer_login).pack(side="left", padx=(0, 10))
        ttk.Button(botoes_frame, text="Cancelar", command=self.janela.destroy).pack(side="left")
        
        # Focar no campo usuário
        self.entry_usuario.focus()
        
        # Bind Enter para login
        self.entry_senha.bind('<Return>', lambda e: self._fazer_login())
        
    def _fazer_login(self):
        """Realiza o login"""
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()
        
        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
            
        if self.sistema_auth.login(usuario, senha):
            self.janela.destroy()
            self.callback_sucesso()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

def main():
    """Função principal"""
    try:
        # Verificar se está em modo headless (teste)
        if len(sys.argv) > 1 and sys.argv[1] == "--headless":
            print("Executando em modo headless (teste)")
            # Inicializar componentes sem GUI
            sistema_auth = SistemaAutenticacao()
            gerenciador_dados = GerenciadorDados()
            print(f"Sistema inicializado com sucesso.")
            print(f"Usuários: {len(sistema_auth.usuarios)}")
            print(f"Clientes cadastrados: {len(gerenciador_dados.dados.get('cadastros', []))}")
            return
            
        # Modo normal com GUI
        try:
            app = SistemaCM()
            app.executar()
        except Exception as e:
            logging.error(f"Erro ao executar sistema: {e}")
            print(f"Erro ao executar sistema: {e}")
    except Exception as e:
        logging.error(f"Erro crítico: {e}")
        print(f"Erro crítico: {e}")

if __name__ == "__main__":
    main()