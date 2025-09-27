# 🧪 GUIA COMPLETO DE TESTES - Sistema CM Premium

## 🎯 COMO TESTAR TODAS AS FUNCIONALIDADES VISUAIS

Este guia te ensina como testar cada parte do sistema e suas melhorias visuais.

---

## 🚀 PARTE 1: TESTANDO O DECORADOR DE TEMAS

### 1.1 Executar o Decorador
```bash
python decorar_sistema.py
```

**O que você deve ver:**
- ✅ Janela moderna com título "🎨 DECORADOR DO SISTEMA CM"
- ✅ 4 botões de temas: Premium, Cyberpunk, Nature, Sunset
- ✅ Cards com estatísticas de demonstração
- ✅ Gráfico de barras interativo
- ✅ Botão "🚀 APLICAR AO SISTEMA REAL"

**Como testar:**
1. **Clique em cada tema** - Observe as mudanças de cores
2. **Veja os cards** - Devem mostrar valores como "R$ 150.000,00"
3. **Observe o gráfico** - Barras coloridas com dados de exemplo
4. **Teste o botão aplicar** - Pergunta se quer aplicar ao sistema real

### 1.2 Aplicar Tema ao Sistema
1. Escolha um tema (ex: Premium)
2. Clique "🚀 APLICAR AO SISTEMA REAL"
3. Confirme "Sim"
4. Deve aparecer mensagem de sucesso

---

## 🚀 PARTE 2: TESTANDO O SISTEMA PREMIUM

### 2.1 Executar Sistema Premium
```bash
cd src
python premium_app.py
```

**Tela de Login - O que testar:**
- ✅ **Centralização**: Janela deve abrir centralizada
- ✅ **Layout**: Header azul, card branco no centro
- ✅ **Foto do usuário**: Círculo com foto ou ícone padrão
- ✅ **Campos**: Usuário e senha visíveis e editáveis
- ✅ **Botões**: "Entrar" e "🌙" (trocar tema) funcionando
- ✅ **Upload de foto**: Botões "Upload Foto" e "Remover Foto"

**Como testar login:**
1. **Login padrão**: admin / 1234
2. **Teste foto**: Clique "Upload Foto" → Selecione imagem → Deve aparecer circular
3. **Teste tema**: Clique "🌙" → Deve alternar claro/escuro
4. **Teste diferentes usuários**: Se houver outros usuários cadastrados

### 2.2 Tela Principal Premium
**O que deve aparecer após login:**
- ✅ **Header**: Azul com foto do usuário e nome
- ✅ **Sidebar**: Menu lateral com ícones coloridos
- ✅ **Dashboard**: Gráficos e métricas centrais
- ✅ **Botão tema**: "🌙" no header

**Como testar:**
1. **Navegação**: Clique em cada item do menu (Início, Cadastros, etc.)
2. **Gráficos**: Devem aparecer gráficos de exemplo com matplotlib
3. **Cards**: Métricas com valores formatados
4. **Tema**: Botão "🌙" deve alternar cores sem travar
5. **Responsividade**: Redimensione a janela

### 2.3 Testando Cadastros
**Navegue para: Sidebar → Cadastros**

**Sub-abas disponíveis:**
- Usuários | Lojas | Clientes | Módulos de Curso | Imóvel Vendido | Receita | Despesa

**Como testar cada cadastro:**

#### 2.3.1 Usuários
1. **Lista**: Deve mostrar usuários existentes
2. **Novo usuário**: Clique "Novo Usuário"
3. **Campos**: Nome, senha, admin (checkbox)
4. **Upload foto**: Teste upload e remoção
5. **Salvar**: Deve aparecer na lista
6. **Editar**: Clique duplo em usuário existente

#### 2.3.2 Lojas
1. **Nova loja**: Clique "Nova Loja"
2. **Campos obrigatórios**: Nome, tipo (dropdown)
3. **Campos opcionais**: Cidade, UF, responsável, etc.
4. **Máscaras**: Telefone deve formatar automático (00) 00000-0000
5. **Salvar**: Deve aparecer na lista com status ativo

#### 2.3.3 Clientes
1. **Novo cliente**: Clique "Novo Cliente"
2. **Máscaras automáticas**:
   - CPF: 000.000.000-00
   - Telefone: (00) 00000-0000
   - Valores: R$ 0.000,00
   - Data: 00/00/0000
3. **Upload foto**: Deve salvar como PNG circular
4. **Cálculo automático**: Limite de crédito baseado na renda

#### 2.3.4 Módulos de Curso
1. **Novo curso**: Clique "Novo Curso"
2. **Valores**: Digite "150000" → Deve virar "R$ 1.500,00"
3. **Cashback**: Valor em reais, não porcentagem
4. **Parcelas**: Número entre 2-12
5. **Status**: Ativo/Inativo

#### 2.3.5 Imóvel Vendido
1. **Novo imóvel**: Clique "Novo Imóvel"
2. **Valores grandes**: Digite "500000000" → "R$ 5.000.000,00"
3. **Comissão**: Valor em reais
4. **Data**: Formato DD/MM/AAAA

---

## 🚀 PARTE 3: TESTANDO FUNCIONALIDADES ESPECÍFICAS

### 3.1 Upload de Fotos
**Onde testar:**
- Login premium (foto do usuário)
- Cadastros → Usuários
- Cadastros → Clientes

**Como testar:**
1. Clique "Upload Foto"
2. Selecione qualquer imagem (JPG, PNG, etc.)
3. **Resultado esperado**: Foto circular, 400x400px, centralizada
4. **Arquivo salvo em**: 
   - Usuários: `user_photos/nome_usuario.png`
   - Clientes: `client_photos/cpf_cliente.png`

### 3.2 Máscaras Automáticas
**Campos com máscaras:**

#### Valores monetários:
- Digite: `150000` → Resultado: `R$ 1.500,00`
- Digite: `1500000` → Resultado: `R$ 15.000,00`
- Digite: `50` → Resultado: `R$ 50,00`

#### Telefones:
- Digite: `11999887766` → Resultado: `(11) 99988-7766`

#### CPF:
- Digite: `12345678901` → Resultado: `123.456.789-01`

#### Datas:
- Digite: `15032024` → Resultado: `15/03/2024`

### 3.3 Temas Claro/Escuro
**Como testar:**
1. **Na tela de login**: Clique botão "🌙"
2. **Na tela principal**: Clique botão "🌙" no header
3. **Resultado esperado**: 
   - Cores devem alternar instantaneamente
   - Texto deve ficar legível
   - Sistema não deve travar
   - Mensagem no terminal: "Modo Escuro/Claro ativado com sucesso!"

---

## 🚀 PARTE 4: TESTANDO EXTENSÕES DO VS CODE

### 4.1 Executar Setup Visual
```bash
python setup_visual.py
```

**O que deve acontecer:**
- ✅ Instala extensões recomendadas
- ✅ Configura settings.json
- ✅ Aplica tema Material Dark High Contrast
- ✅ Ativa ícones Material Icon Theme

### 4.2 Verificar Extensões Instaladas
1. Abra VS Code: `code .`
2. Pressione `Ctrl+Shift+X` (Extensions)
3. **Extensões que devem aparecer como instaladas:**
   - Material Theme
   - Material Icon Theme  
   - Python
   - Black Formatter
   - Pylance
   - Error Lens
   - Bracket Pair Colorizer

### 4.3 Testar Visual do Código
```bash
python demo_visual.py
```

**O que observar:**
- ✅ Código com syntax highlighting colorido
- ✅ Parênteses coloridos
- ✅ Indentação visível
- ✅ Ícones de arquivo modernos
- ✅ Tema escuro aplicado

---

## 🚀 PARTE 5: TESTES DE ESTABILIDADE

### 5.1 Teste de Stress - Mudanças de Tema
1. Execute o sistema premium
2. Alterne tema 10 vezes seguidas (claro/escuro)
3. **Resultado esperado**: Sistema deve continuar funcionando
4. **Se travar**: Feche e reabra o sistema

### 5.2 Teste de Upload Múltiplo
1. Cadastre 3 usuários diferentes
2. Faça upload de foto para cada um
3. Verifique se fotos ficam salvas corretamente
4. Teste trocar foto de usuário existente

### 5.3 Teste de Valores Grandes
1. Cadastros → Imóvel Vendido
2. Digite valor: `999999999`
3. Deve formatar: `R$ 9.999.999,99`
4. Salve e verifique se mantém formatação

---

## 🚀 PARTE 6: RESOLUÇÃO DE PROBLEMAS

### 6.1 Sistema não inicia
```bash
# Verificar dependências
pip install -r requirements.txt

# Executar com debug
cd src
python -u premium_app.py
```

### 6.2 Erro de foto
```bash
# Criar diretórios se não existirem
mkdir user_photos
mkdir client_photos
```

### 6.3 Banco de dados corrompido
```bash
# Deletar banco (ATENÇÃO: perde dados!)
del sistema.db
```

### 6.4 Tema travando
- **Sintoma**: Sistema trava ao trocar tema
- **Solução**: Feche a janela e reabra o sistema
- **Prevenção**: Aguarde tema carregar completamente antes de trocar novamente

---

## 🚀 PARTE 7: CHECKLIST FINAL

### ✅ Decorador de Temas
- [ ] Abre sem erros
- [ ] 4 temas funcionam
- [ ] Cards mostram dados
- [ ] Gráfico aparece
- [ ] Botão aplicar funciona

### ✅ Sistema Premium - Login
- [ ] Centraliza na tela
- [ ] Campos visíveis
- [ ] Upload foto funciona
- [ ] Troca tema funciona
- [ ] Login admin/1234 funciona

### ✅ Sistema Premium - Principal
- [ ] Dashboard com gráficos
- [ ] Sidebar navegável
- [ ] Header com foto usuário
- [ ] Troca tema sem travar
- [ ] Todas as abas abrem

### ✅ Cadastros
- [ ] Usuários: CRUD + foto
- [ ] Lojas: Campos + máscaras
- [ ] Clientes: Foto + máscaras + cálculos
- [ ] Cursos: Valores + cashback
- [ ] Imóveis: Valores grandes

### ✅ Funcionalidades Especiais
- [ ] Máscaras automáticas funcionam
- [ ] Fotos ficam circulares
- [ ] Valores formatam corretamente
- [ ] Upload salva arquivos
- [ ] Tema persiste entre telas

### ✅ VS Code
- [ ] Extensões instaladas
- [ ] Tema aplicado
- [ ] Ícones modernos
- [ ] Syntax highlighting

---

## 🎯 RESULTADO ESPERADO

Após todos os testes, você deve ter:

1. **Sistema visual moderno** com tema premium
2. **Fotos de usuários** salvas e exibidas corretamente  
3. **Máscaras automáticas** funcionando em todos os campos
4. **Temas claro/escuro** alternando sem problemas
5. **VS Code configurado** com visual profissional
6. **Cadastros funcionais** com validações e formatações
7. **Dashboard com gráficos** exibindo métricas

---

## 📞 SUPORTE

Se algum teste falhar:
1. Verifique se executou os comandos na pasta correta
2. Confirme se todas as dependências estão instaladas
3. Teste com dados simples primeiro
4. Verifique mensagens no terminal
5. Reinicie o sistema se necessário

**Sistema testado e aprovado!** ✅

---

*Guia criado para Sistema CM Premium v2.0*
*Última atualização: $(date)*
