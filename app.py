from flask import Flask, render_template, request, redirect
import json
from datetime import datetime, date

# Instancia a aplicação Flask, responsável pelo gerenciamento de rotas e processamento HTTP
app = Flask(__name__)

# ==========================================
# 1. MODELOS DE DADOS
# ==========================================
class Exercicio:
    """
    Representa um exercício individual dentro de um treino.
    Guarda as informações de nome, quantidade de séries, repetições e o grupo muscular alvo.
    """
    def __init__(self, nome, series, grupo_muscular="Outros"):
        self.nome = nome
        self.series = series
        self.grupo_muscular = grupo_muscular

class Rotina:
    """
    Representa uma rotina de treino (ex: Treino A, Treino B).
    Contém um ID único, um nome, o foco principal (ex: Peito e Tríceps) e uma lista de objetos Exercicio.
    """
    def __init__(self, id, nome, foco, exercicios):
        self.id = id
        self.nome = nome
        self.foco = foco
        self.exercicios = exercicios

# ==========================================
# 2. DADOS TEMPORÁRIOS (MOCK DATA)
# TODO: Substituir por um banco de dados real (ex: SQLite ou PostgreSQL) no futuro.
# ==========================================
minhas_rotinas = [
    Rotina(1, "Dia 1", "Peito, Tríceps e Ombro", [
        Exercicio("Supino Reto", [{"tipo": "Normal", "meta_reps": 10} for _ in range(4)], "Peito"),
        Exercicio("Desenvolvimento", [{"tipo": "Normal", "meta_reps": 10} for _ in range(4)], "Ombros")
    ]),
    Rotina(2, "Dia 2", "Costas e Bíceps", [
        Exercicio("Puxada Alta", [{"tipo": "Normal", "meta_reps": 10} for _ in range(4)], "Costas"),
        Exercicio("Remada Curvada", [{"tipo": "Normal", "meta_reps": 10} for _ in range(4)], "Costas")
    ]),
    Rotina(3, "Dia 3", "Pernas", [
        Exercicio("Agachamento Livre", [{"tipo": "Normal", "meta_reps": 10} for _ in range(4)], "Pernas"),
        Exercicio("Leg Press 45º", [{"tipo": "Normal", "meta_reps": 12} for _ in range(4)], "Pernas")
    ]),
    Rotina(4, "Dia 4", "Upper (Superior)", [
        Exercicio("Supino Inclinado", [{"tipo": "Normal", "meta_reps": 10} for _ in range(3)], "Peito"),
        Exercicio("Barra Fixa", [{"tipo": "Normal", "meta_reps": "Máx"} for _ in range(3)], "Costas")
    ])
]

historico_treinos = [
    {"data": datetime(2026, 8, 10, 9, 0), "exercicio": "Agachamento Livre", "peso_kg": 60},
    {"data": datetime(2026, 8, 17, 10, 30), "exercicio": "Agachamento Livre", "peso_kg": 64},
    {"data": datetime(2026, 8, 20, 8, 45), "exercicio": "Supino Reto", "peso_kg": 25}
]

def obter_ultimo_peso(nome_exercicio):
    """
    Busca no histórico de treinos a última carga utilizada para um determinado exercício.
    Percorre a lista de trás para frente (do mais recente para o mais antigo).
    """
    for treino in reversed(historico_treinos):
        if treino["exercicio"] == nome_exercicio:
            return treino["peso_kg"]
    return "-" 

# ==========================================
# 3. ROTAS DE VISUALIZAÇÃO (PÁGINAS DO APP)
# ==========================================

@app.route("/")
def home():
    """Rota da página inicial. Exibe a lista de todas as rotinas de treino disponíveis."""
    return render_template("index.html", rotinas=minhas_rotinas)

@app.route("/treino/<int:rotina_id>")
def iniciar_treino(rotina_id):
    """
    Página de execução do treino. Busca a rotina pelo ID e calcula a última carga 
    registrada para cada exercício dessa rotina, para exibir ao usuário.
    """
    rotina_selecionada = next((r for r in minhas_rotinas if r.id == rotina_id), None)
    
    if rotina_selecionada:
        ultimos_pesos = {}
        for ex in rotina_selecionada.exercicios:
            ultimos_pesos[ex.nome] = obter_ultimo_peso(ex.nome)
        return render_template("treino.html", rotina=rotina_selecionada, ultimos_pesos=ultimos_pesos)
    
    return "Rotina não encontrada", 404

@app.route("/editar/<int:rotina_id>")
def editar_rotina(rotina_id):
    """Página para editar uma rotina de treino existente (adicionar/remover exercícios)."""
    rotina_selecionada = next((r for r in minhas_rotinas if r.id == rotina_id), None)
    if rotina_selecionada:
        return render_template("editar.html", rotina=rotina_selecionada)
    return "Rotina não encontrada", 404

@app.route("/historico/<nome_exercicio>")
def historico_exercicio(nome_exercicio):
    """Página que exibe o histórico detalhado de cargas de um exercício específico."""
    # Filtra o histórico para pegar apenas os registros deste exercício,
    # ordenando do mais antigo para o mais recente (ideal para o gráfico de evolução).
    registros_raw = sorted(
        [t for t in historico_treinos if t["exercicio"] == nome_exercicio],
        key=lambda r: r["data"]
    )
    
    # Formata o objeto datetime para string legível antes de enviar ao template
    # Ex: datetime(2026, 8, 27, 10, 30) vira "27/08/26 10:30"
    registros = [
        {**r, "data": r["data"].strftime("%d/%m/%y %H:%M")}
        for r in registros_raw
    ]
    
    # Prepara dados para o gráfico (X = datas formatadas, Y = pesos)
    datas = [r["data"] for r in registros]
    pesos = [r["peso_kg"] for r in registros]
    
    return render_template("historico.html", 
                           nome_exercicio=nome_exercicio, 
                           registros=registros,
                           datas=datas,
                           pesos=pesos)


# ==========================================
# 4. ROTAS DE AÇÃO (FORMULÁRIOS E ALTERAÇÕES)
# ==========================================

@app.route("/adicionar_exercicio/<int:rotina_id>", methods=["POST"])
def adicionar_exercicio(rotina_id):
    """Recebe os dados do formulário via POST e adiciona um novo exercício à rotina selecionada."""
    rotina = next((r for r in minhas_rotinas if r.id == rotina_id), None)
    if rotina:
        nome = request.form.get("nome")
        grupo_muscular = request.form.get("grupo_muscular", "Outros")
        
        series_str = request.form.get("dados_series")
        series = []
        if series_str:
            try:
                series = json.loads(series_str)
            except Exception as e:
                print("Erro lendo json series", e)
                
        rotina.exercicios.append(Exercicio(nome, series, grupo_muscular))
    
    return redirect(f"/editar/{rotina_id}")

@app.route("/remover_exercicio/<int:rotina_id>/<nome_exercicio>")
def remover_exercicio(rotina_id, nome_exercicio):
    """Remove um exercício específico de uma rotina, buscando pelo nome do exercício."""
    rotina = next((r for r in minhas_rotinas if r.id == rotina_id), None)
    if rotina:
        rotina.exercicios = [ex for ex in rotina.exercicios if ex.nome != nome_exercicio]
    
    return redirect(f"/editar/{rotina_id}")

@app.route("/finalizar_treino", methods=["POST"])
def finalizar_treino():
    """Recebe os dados do treino finalizado via POST e salva as séries concluídas."""
    dados_str = request.form.get("dados_treino")
    if dados_str:
        try:
            dados = json.loads(dados_str)
            agora = datetime.now()  # Salva data E hora completa
            
            for item in dados:
                exercicio_nome = item.get("exercicio")
                series = item.get("series", [])
                
                if series:
                    # Para manter compatibilidade com o gráfico de histórico atual (que usa 1 carga por dia),
                    # registramos a maior carga executada entre as séries concluídas.
                    maior_carga = max(s.get("carga", 0) for s in series)
                    
                    historico_treinos.append({
                        "data": agora,       # Objeto datetime completo
                        "exercicio": exercicio_nome,
                        "peso_kg": maior_carga
                    })
        except Exception as e:
            print("Erro ao processar treino:", e)
            
    return redirect("/desempenho")

# ==========================================
# 5. ROTAS DE ESTATÍSTICAS E DESEMPENHO
# ==========================================

@app.route("/desempenho")
def desempenho():
    """Página de acompanhamento do desempenho, contendo o calendário de dias treinados."""
    sequencia_atual = 4 
    
    # Pega o mês da URL (ex: /desempenho?mes=8). Se não for passado, usa 8 (Agosto) como padrão.
    mes_atual = int(request.args.get("mes", 8))
    
    meses_info = {
        1: ("Janeiro", 31), 2: ("Fevereiro", 28), 3: ("Março", 31),
        4: ("Abril", 30), 5: ("Maio", 31), 6: ("Junho", 30),
        7: ("Julho", 31), 8: ("Agosto", 31), 9: ("Setembro", 30),
        10: ("Outubro", 31), 11: ("Novembro", 30), 12: ("Dezembro", 31)
    }
    
    nome_mes, total_dias = meses_info.get(mes_atual, ("Agosto", 31))
    
    treinos_por_mes = {
        7: [3, 10, 17, 24],                    
        8: [2, 5, 8, 12, 15, 19, 22, 26, 28],   
        9: [1, 4, 6, 11, 14, 18, 21, 25, 30]    
    }
    
    dias_treinados_mes = treinos_por_mes.get(mes_atual, [])
    
    mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
    mes_proximo = mes_atual + 1 if mes_atual < 12 else 1
    
    # Extrai os nomes únicos de exercícios que possuem histórico
    exercicios_historico = sorted(list(set([t["exercicio"] for t in historico_treinos])))
    
    return render_template("desempenho.html", 
                           sequencia_semanal=sequencia_atual, 
                           dias_treinados=dias_treinados_mes,
                           nome_mes=nome_mes,
                           total_dias=total_dias,
                           mes_anterior=mes_anterior,
                           mes_proximo=mes_proximo,
                           exercicios_historico=exercicios_historico)

if __name__ == "__main__":
    # Inicia o servidor local do Flask. O modo debug=True recarrega o servidor automaticamente a cada mudança de código.
    # TODO: Para deploy em produção (servidor real), remover debug=True e utilizar um servidor WSGI como o Gunicorn.
    app.run(debug=True)