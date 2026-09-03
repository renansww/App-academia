# TheLoad
Aplicação web Flask para controle de rotinas de treino, acompanhamento de exercícios e histórico de cargas.

## Funcionalidades

- **Gerenciamento de Rotinas** — Crie e edite rotinas (ex: Push/Pull/Legs, Superior/Inferior)
- **Rastreamento de Exercícios** — Registre exercícios com séries, repetições e grupos musculares
- **Histórico de Progresso** — Visualize evolução de cargas por exercício com gráficos
- **Calendário de Treinos** — Calendário visual com frequência e consistência dos treinos
- **Interface Responsiva** — UI limpa e mobile-first com CSS/JS vanilla

## Stack
- Backend: Python 3, Flask 3
- Frontend: HTML5, CSS3, JavaScript
- Templates: Jinja2
- Dados: em memória (mock)
- Gráficos: Chart.js (via CDN)


## Instalação
1. Crie e ative um ambiente virtual (venv).
2. Instale as dependências do projeto.
3. Execute a aplicação Flask.


## Detalhes de Implementação

### Modelos de Dados
- `Exercicio` — Exercício individual com nome, séries (tipo + repetições alvo), grupo muscular
- `Rotina` — Rotina de treino contendo múltiplos exercícios com ID único e foco principal
- Rotas Flask com decoradores `@app.route`

### Próximos Passos
- [ ] Substituir dados mock por SQLite/SQLAlchemy
- [ ] Autenticação de usuários (suporte multi-usuário)
- [ ] API REST para integração com app mobile
- [ ] Testes unitários com pytest
- [ ] Containerização com Docker
- [ ] Deploy no Render/Fly.io/Heroku


**Autor:** Renan Andrade  
**Curso:** Ciência da Computação — Projeto de Portfólio 
**Contato:** [LinkedIn](https://linkedin.com/in/renanconta) • [GitHub](https://github.com/renansww)