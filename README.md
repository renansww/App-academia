# TheLoad
Aplicação web Flask para controle de rotinas de treino, acompanhamento de exercícios e histórico de cargas. Projeto de portfólio demonstrando habilidades de desenvolvimento full-stack.

## Funcionalidades

- **Gerenciamento de Rotinas** — Crie e edite rotinas (ex: Push/Pull/Legs, Superior/Inferior)
- **Rastreamento de Exercícios** — Registre exercícios com séries, repetições e grupos musculares
- **Histórico de Progresso** — Visualize evolução de cargas por exercício com gráficos
- **Calendário de Treinos** — Calendário visual com frequência e consistência dos treinos
- **Interface Responsiva** — UI limpa e mobile-first com CSS/JS vanilla

## Projeto:
| Backend: Python 3, Flask 3 
| Frontend: HTML5, CSS3, JavaScript
| Templates: Jinja2
| Dados: Em memória  — FUTURAMENTE SQLITE
| Gráficos: Chart.js (via CDN)


### Instalação
- em ambiente virtual (venv) e python 3


## Detalhes de Implementação

### Modelos de Dados
- `Exercicio` — Exercício individual com nome, séries (tipo + repetições alvo), grupo muscular
- `Rotina` — Rotina de treino contendo múltiplos exercícios com ID único e foco principal
- utilização de rotas com decorador @ 

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