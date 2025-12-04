# Escopo do Projeto

## Escopo do MVP
O MVP do Terê Verde Online entrega uma solução web simples e objetiva para divulgação e gestão básica de informações dos parques de Teresópolis.

- Consulta pública a informações de parques:
	- Listagem e detalhes dos parques (nome, tipo, localização e descrição).
	- Trilhas por parque (nome, dificuldade, duração estimada, status aberta/fechada).
	- Eventos (lista de próximos eventos ativos, com período e descrição curta).
	- Disponibilidade (períodos e horários vigentes por parque).
	- Biodiversidade (itens principais como fauna e flora por parque — opcional no MVP, mas suportado pelo modelo).
- Área administrativa protegida por login para:
	- Gerenciar parques (CRUD simples).
	- Gerenciar trilhas (CRUD simples e alternar status aberta/fechada).
	- Gerenciar eventos (CRUD simples e ativar/desativar).
	- Gerenciar períodos de disponibilidade (CRUD simples).
- Atualização básica de conteúdo pelos administradores (CRUD simples, sem fluxos complexos).
- Foco em:
	- Desempenho razoável (consultas diretas, ordenações simples, e estrutura leve com SQLite).
	- Interface responsiva simples (HTML/CSS básicos, grid/cards para listagens).
	- Segurança mínima para dados de admins (login, sessão, hash de senha, CSRF em formulários).

## Fora do Escopo
Para manter o MVP enxuto e viável no curto prazo, os seguintes itens NÃO serão implementados:

- Sistema de reservas ou agendamento de visitas (tickets, pagamentos, lotes, etc.).
- Integração com APIs externas (por exemplo, clima em tempo real, mapas avançados com trilhas). 
- Aplicativos móveis nativos (Android/iOS) — apenas web responsivo.
- Painéis avançados de analytics e relatórios complexos (gráficos, exportações, BI).
- Múltiplos níveis de permissão ou perfis de acesso administrativos (roles complexos).
- Cadastro/autenticação de visitantes ou armazenamento de dados pessoais de turistas.
- Moderação de conteúdo, workflows de aprovação ou versionamento de mudanças.
- Internacionalização/idiomas múltiplos (o MVP será em português).
- Upload/gestão de mídia avançada (galerias, CDN, transformação de imagens).


