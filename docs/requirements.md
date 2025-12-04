# Requisitos do Projeto

## Requisitos Funcionais

### RF-01: Visualização de Lista de Parques
O sistema deve permitir que visitantes visualizem a lista de parques cadastrados, com informações básicas como nome, tipo e descrição.

### RF-02: Visualização de Detalhes de Parques
O sistema deve permitir que visitantes visualizem detalhes completos de um parque, incluindo:
- Informações gerais (nome, tipo, localização, descrição)
- Trilhas associadas ao parque
- Eventos futuros ativos do parque
- Períodos de disponibilidade vigentes
- Itens de biodiversidade (fauna e flora)

### RF-03: Listagem de Trilhas
O sistema deve permitir que visitantes visualizem uma lista de trilhas, com filtros opcionais por parque e nível de dificuldade. As informações devem incluir nome, parque, dificuldade, duração estimada e status (aberta/fechada).

### RF-04: Listagem de Eventos Futuros
O sistema deve exibir lista de eventos futuros para visitantes, com filtro opcional por parque. As informações devem incluir título, parque, período (data/hora de início e término) e descrição.

### RF-05: Página Sobre o Projeto
O sistema deve oferecer uma página explicando o objetivo do Terê Verde Online e orientações sobre uso consciente das áreas naturais protegidas.

### RF-06: Login de Administradores
O sistema deve permitir que administradores façam login em área restrita utilizando email e senha. O sistema deve validar as credenciais e criar uma sessão autenticada.

### RF-07: Gestão de Parques (CRUD)
O sistema deve permitir que administradores autenticados:
- Cadastrem novos parques (nome, tipo, localização, descrição)
- Editem informações de parques existentes
- Excluam parques (com remoção em cascata de trilhas, eventos e períodos associados)

### RF-08: Gestão de Trilhas (CRUD)
O sistema deve permitir que administradores autenticados:
- Cadastrem novas trilhas (parque, nome, dificuldade, duração estimada, descrição)
- Editem informações de trilhas existentes
- Alternem o status de trilhas (aberta/fechada)
- Excluam trilhas

### RF-09: Gestão de Eventos (CRUD)
O sistema deve permitir que administradores autenticados:
- Cadastrem novos eventos (parque, título, descrição, data/hora de início e término)
- Editem informações de eventos existentes
- Alternem o status de eventos (ativo/inativo)
- Excluam eventos

### RF-10: Gestão de Períodos de Disponibilidade (CRUD)
O sistema deve permitir que administradores autenticados:
- Cadastrem novos períodos de disponibilidade (parque, nome da temporada, horários de abertura/fechamento, datas de início e término)
- Editem informações de períodos existentes
- Excluam períodos de disponibilidade

### RF-11: Dashboard Administrativo
O sistema deve exibir um dashboard administrativo com estatísticas básicas:
- Quantidade de parques cadastrados
- Quantidade de trilhas (total e abertas)
- Quantidade de eventos (total, ativos e futuros)
- Quantidade de períodos de disponibilidade

### RF-12: Informações de Biodiversidade
O sistema deve exibir informações sobre biodiversidade (fauna e flora) associada aos parques, quando disponíveis.

## Requisitos Não Funcionais

### RNF-01: Tecnologia Back-end
O sistema deve ser desenvolvido em Python 3 utilizando o framework Flask para o back-end.

### RNF-02: Banco de Dados
O sistema deve armazenar dados em um banco de dados SQLite local, utilizando SQLAlchemy como ORM.

### RNF-03: Desempenho
O sistema deve responder em tempo adequado para uso por múltiplos usuários simultâneos, considerando otimização básica de consultas (índices, ordenações adequadas, limites de resultados quando necessário).

### RNF-04: Interface do Usuário
O sistema deve possuir interface web intuitiva, responsiva e de fácil navegação, utilizando HTML/CSS básico e templates Jinja2.

### RNF-05: Segurança
O sistema deve proteger dados de administradores utilizando:
- Senhas armazenadas com hash (bcrypt via passlib)
- Autenticação baseada em sessão
- Proteção CSRF em formulários administrativos (Flask-WTF)

### RNF-06: Estrutura do Projeto
O projeto deve estar organizado com as seguintes pastas:
- `src/` - código-fonte da aplicação
- `src/app/` - aplicação Flask principal
- `src/app/templates/` - templates HTML (Jinja2)
- `src/app/static/` - arquivos estáticos (CSS, JS)
- `test/` - testes automatizados (pytest)
- `data/` - banco de dados SQLite e arquivos de dados
- `docs/` - documentação do projeto

### RNF-07: Testes
O projeto deve incluir testes básicos com pytest para validar funcionalidades críticas (criação da aplicação, rotas públicas, autenticação).

### RNF-08: Documentação
O repositório deve conter:
- `README.md` informativo com descrição do projeto, instruções de instalação e execução, estrutura de diretórios e dados da equipe
- `docs/scope.md` com escopo do MVP e itens fora do escopo
- `docs/requirements.md` com lista de requisitos funcionais e não funcionais

### RNF-09: Versionamento
O repositório deve ser versionado utilizando Git e hospedado no GitHub (ou similar).

### RNF-10: Dependências
O projeto deve incluir um arquivo `requirements.txt` listando todas as dependências Python necessárias para execução.
