# Terê Verde Online - MVP

## Equipe

| Nome | E-mail | RA/Matrícula |
|------|--------|--------------|
|      |        |              |
|      |        |              |
|      |        |              |

## Situação-Problema

Este projeto é baseado no **Círculo Terê Verde**, uma iniciativa relacionada à preservação e divulgação das áreas naturais protegidas de Teresópolis.

A situação-problema identificada é a necessidade de uma solução digital simples e eficiente para facilitar o acesso às informações dos parques da região, permitindo que visitantes e turistas consultem dados sobre trilhas, eventos, biodiversidade e condições de visitação, enquanto administradores possam gerenciar essas informações de forma centralizada.

## Descrição do MVP

O **Terê Verde Online** é um sistema web desenvolvido como MVP para acesso às informações dos parques em Teresópolis:

- **Parque Nacional da Serra dos Órgãos**
- **Parque Estadual dos Três Picos**
- **Parque Natural Municipal Montanhas de Teresópolis**

### Funcionalidades Principais

**Para Visitantes:**
- Consulta pública de informações sobre parques, trilhas, eventos e períodos de disponibilidade
- Visualização de detalhes de parques (incluindo trilhas, eventos futuros e biodiversidade)
- Filtros para trilhas (por parque e dificuldade) e eventos (por parque)
- Página informativa sobre o projeto e uso consciente das áreas naturais

**Para Administradores:**
- Área restrita com autenticação por login
- Dashboard com estatísticas básicas
- Gestão completa (CRUD) de parques, trilhas, eventos e períodos de disponibilidade
- Ativação/desativação de trilhas e eventos

## Tecnologias Utilizadas

- **Python 3** - Linguagem de programação
- **Flask** - Framework web para back-end
- **SQLite** - Banco de dados relacional
- **SQLAlchemy** - ORM para acesso ao banco de dados
- **Flask-WTF** - Proteção CSRF e formulários
- **Jinja2** - Motor de templates HTML
- **HTML/CSS** - Interface do usuário (front-end básico)
- **pytest** - Framework de testes

## Estrutura de Diretórios

```
tere-verde-online/
├── src/                    # Código-fonte da aplicação
│   └── app/                # Módulo principal da aplicação Flask
│       ├── templates/      # Templates HTML (Jinja2)
│       ├── static/         # Arquivos estáticos (CSS, JS, imagens)
│       ├── __init__.py     # Factory da aplicação Flask
│       ├── routes_public.py # Rotas públicas (visitantes)
│       ├── routes_admin.py  # Rotas administrativas
│       ├── models.py        # Modelos do banco de dados (SQLAlchemy)
│       ├── config.py        # Configurações da aplicação
│       ├── forms.py         # Formulários (Flask-WTF)
│       └── cli.py           # Comandos de linha de comando
├── test/                   # Testes automatizados (pytest)
├── data/                   # Banco de dados SQLite e arquivos de dados
├── docs/                   # Documentação do projeto
│   ├── scope.md            # Escopo do MVP
│   └── requirements.md     # Requisitos funcionais e não funcionais
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## Como Executar o Projeto Localmente

### 1. Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### 2. Configuração do Ambiente

```bash
# Criar ambiente virtual (recomendado)
python -m venv .venv

# Ativar ambiente virtual
# Windows (PowerShell)
.venv\Scripts\activate
# Windows (CMD)
.venv\Scripts\activate.bat
# macOS/Linux
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Inicialização do Banco de Dados

```bash
# Criar as tabelas no banco de dados
python -m src.app.cli init-db

# Popular com dados de exemplo (admin, parques, trilhas, eventos, disponibilidade)
python -m src.app.cli seed
```

**Credenciais padrão do administrador:**
- Email: `admin@teste.com`
- Senha: `admin123`

### 4. Executar a Aplicação

**Opção A: Usando arquivo `run.py` (recomendado)**

O arquivo `run.py` já está na raiz do projeto:

```python
from src.app import create_app

app = create_app("development")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

Execute:
```bash
python run.py
```

**Opção B: Usando Flask CLI**

```bash
# Configurar variável de ambiente (opcional)
# Windows (PowerShell)
$env:FLASK_APP = "src/app/__init__.py"
# macOS/Linux
export FLASK_APP=src/app/__init__.py

# Executar
flask run --host=0.0.0.0 --port=5000
```

A aplicação estará disponível em: `http://localhost:5000`

### 5. Acessar a Aplicação

- **Site público:** http://localhost:5000
- **Área administrativa:** http://localhost:5000/admin/login

## Como Rodar os Testes

Execute os testes automatizados com pytest:

```bash
pytest
```

Para saída mais detalhada:

```bash
pytest -v
```

Para saída resumida:

```bash
pytest -q
```

## Informações Adicionais

### Observações

- O banco de dados SQLite é criado automaticamente em `data/tere_verde.db` ao executar `init-db`
- Em ambiente de desenvolvimento, a chave secreta padrão é usada. Em produção, defina `SECRET_KEY` via variável de ambiente
- O sistema utiliza CSRF protection em todos os formulários administrativos
- Para mais detalhes sobre o escopo e requisitos, consulte os arquivos em `docs/`

### Evoluções Futuras (Fora do Escopo do MVP)

- Sistema de reservas ou agendamento de visitas
- Integração com APIs externas (clima, mapas avançados)
- Aplicativos móveis nativos
- Painéis avançados de analytics
- Múltiplos níveis de permissão de administradores
- Cadastro de visitantes ou armazenamento de dados pessoais

Para mais informações sobre o escopo, consulte `docs/scope.md`.
