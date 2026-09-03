from flask import Flask, render_template, request, redirect, abort
import json
from datetime import datetime

app = Flask(__name__)

class Exercicio:
    def __init__(self, nome, series, grupo_muscular="Outros"):
        self.nome = nome
        self.series = series
        self.grupo_muscular = grupo_muscular

class Rotina:
    def __init__(self, id, nome, foco, exercicios):
        self.id = id
        self.nome = nome
        self.foco = foco
        self.exercicios = exercicios

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
    for treino in reversed(historico_treinos):
        if treino["exercicio"] == nome_exercicio:
            return treino["peso_kg"]
    return "-"


def obter_rotina_ou_404(rotina_id):
    rotina = next((r for r in minhas_rotinas if r.id == rotina_id), None)
    if not rotina:
        abort(404, description="Rotina não encontrada")
    return rotina

@app.route("/")
def home():
    return render_template("index.html", rotinas=minhas_rotinas)

@app.route("/treino/<int:rotina_id>")
def iniciar_treino(rotina_id):
    rotina = obter_rotina_ou_404(rotina_id)
    ultimos_pesos = {ex.nome: obter_ultimo_peso(ex.nome) for ex in rotina.exercicios}
    return render_template("treino.html", rotina=rotina, ultimos_pesos=ultimos_pesos)

@app.route("/editar/<int:rotina_id>")
def editar_rotina(rotina_id):
    rotina = obter_rotina_ou_404(rotina_id)
    return render_template("editar.html", rotina=rotina)

@app.route("/historico/<nome_exercicio>")
def historico_exercicio(nome_exercicio):
    registros_raw = sorted(
        [t for t in historico_treinos if t["exercicio"] == nome_exercicio],
        key=lambda r: r["data"]
    )

    registros = [
        {**r, "data": r["data"].strftime("%d/%m/%y %H:%M")}
        for r in registros_raw
    ]

    datas = [r["data"] for r in registros]
    pesos = [r["peso_kg"] for r in registros]
    return render_template(
        "historico.html",
        nome_exercicio=nome_exercicio,
        registros=registros,
        datas=datas,
        pesos=pesos,
    )

@app.route("/adicionar_exercicio/<int:rotina_id>", methods=["POST"])
def adicionar_exercicio(rotina_id):
    rotina = obter_rotina_ou_404(rotina_id)
    nome = request.form.get("nome")
    grupo_muscular = request.form.get("grupo_muscular", "Outros")

    series = []
    series_str = request.form.get("dados_series")
    if series_str:
        try:
            series = json.loads(series_str)
        except json.JSONDecodeError:
            abort(400, description="Formato inválido em dados_series")

    rotina.exercicios.append(Exercicio(nome, series, grupo_muscular))
    return redirect(f"/editar/{rotina_id}")

@app.route("/remover_exercicio/<int:rotina_id>/<nome_exercicio>")
def remover_exercicio(rotina_id, nome_exercicio):
    rotina = obter_rotina_ou_404(rotina_id)
    rotina.exercicios = [ex for ex in rotina.exercicios if ex.nome != nome_exercicio]
    return redirect(f"/editar/{rotina_id}")

@app.route("/finalizar_treino", methods=["POST"])
def finalizar_treino():
    dados_str = request.form.get("dados_treino")
    if dados_str:
        try:
            dados = json.loads(dados_str)
            agora = datetime.now()

            for item in dados:
                exercicio_nome = item.get("exercicio")
                series = item.get("series", [])

                if series:
                    maior_carga = max(s.get("carga", 0) for s in series)
                    historico_treinos.append({
                        "data": agora,
                        "exercicio": exercicio_nome,
                        "peso_kg": maior_carga
                    })
        except json.JSONDecodeError:
            abort(400, description="Formato inválido em dados_treino")

    return redirect("/desempenho")

@app.route("/desempenho")
def desempenho():
    sequencia_atual = 4
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

    exercicios_historico = sorted({t["exercicio"] for t in historico_treinos})

    return render_template(
        "desempenho.html",
        sequencia_semanal=sequencia_atual,
        dias_treinados=dias_treinados_mes,
        nome_mes=nome_mes,
        total_dias=total_dias,
        mes_anterior=mes_anterior,
        mes_proximo=mes_proximo,
        exercicios_historico=exercicios_historico,
    )

if __name__ == "__main__":
    app.run(debug=True)