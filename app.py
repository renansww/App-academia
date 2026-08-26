from flask import Flask, render_template, request, redirect
app = Flask(__name__) #flask é como se fosse uma classe que eu baixo para integrar PY com HTML

#Moldes ex: cada exercicio tem seu nome, quantas series e repeticoes
class Exercicio:
    # ATT Adicionei o grupo_muscular como uma obrigação do molde
    def __init__(self, nome, series, repeticoes, grupo_muscular):
        self.nome = nome
        self.series = series
        self.repeticoes = repeticoes
        self.grupo_muscular = grupo_muscular

class Rotina:
    def __init__(self, id, nome, foco, exercicios):
        self.id = id
        self.nome = nome
        self.foco = foco
        self.exercicios = exercicios

#cada rotina é uma lista que pode ser mudada(temporário) --------------
minhas_rotinas = [
    Rotina(1, "Dia 1", "Peito, Tríceps e Ombro", [
        # ATT: Agora cada exercício diz exatamente de qual grupo ele é
        Exercicio("Supino Reto", 4, 10, "Peito"),
        Exercicio("Desenvolvimento", 4, 10, "Ombros")
    ]),
    Rotina(2, "Dia 2", "Costas e Bíceps", [
        Exercicio("Puxada Alta", 4, 10, "Costas"),
        Exercicio("Remada Curvada", 4, 10, "Costas")
    ]),
    Rotina(3, "Dia 3", "Pernas", [
        Exercicio("Agachamento Livre", 4, 10, "Pernas"),
        Exercicio("Leg Press 45º", 4, 12, "Pernas")
    ]),
    Rotina(4, "Dia 4", "Upper (Superior)", [
        Exercicio("Supino Inclinado", 3, 10, "Peito"),
        Exercicio("Barra Fixa", 3, "Máx", "Costas")
    ])
]

# Histórico simulado 
historico_treinos = [
    {"data": "10/08", "exercicio": "Agachamento Livre", "peso_kg": 60},
    {"data": "17/08", "exercicio": "Agachamento Livre", "peso_kg": 64},
    {"data": "20/08", "exercicio": "Supino Reto", "peso_kg": 25}
]
# TEMPORÁRIO------------------------- ˆˆˆˆ



# achar a última carga usando o reverse
def obter_ultimo_peso(nome_exercicio):
    # Procura de trás para frente (mais recentes primeiro)
    for treino in reversed(historico_treinos):
        if treino["exercicio"] == nome_exercicio:
            return treino["peso_kg"]
    return "-" 

# ROTA PAGINA INICIAL
@app.route("/")#meio que quando a página é acessada, o python vai execultar essa função.
def home(): #aqui na home ele vai carregar o index.html
    return render_template("index.html", rotinas=minhas_rotinas)

# ROTA DA TELA DE TREINO ATIVO
@app.route("/treino/<int:rotina_id>") #URL dinamica(metodo GET)
def iniciar_treino(rotina_id):
    rotina_selecionada = next((r for r in minhas_rotinas if r.id == rotina_id), None)
    #next: passa pela lista e se for o id certo vira a selecionada
    if rotina_selecionada:
        ultimos_pesos = {}
        for ex in rotina_selecionada.exercicios:
            ultimos_pesos[ex.nome] = obter_ultimo_peso(ex.nome)# ex nome = ex peso
    #percorrre exercicios e pega os ultimos pesos de todos e coloca nesse dicionario(ultimos pesos)
        return render_template("treino.html", rotina=rotina_selecionada, ultimos_pesos=ultimos_pesos)
    return "Rotina não encontrada", 404

# ROTA editar rotinas
@app.route("/editar/<int:rotina_id>")
def editar_rotina(rotina_id):
    rotina_selecionada = next((r for r in minhas_rotinas if r.id == rotina_id), None)
    if rotina_selecionada:#o primeiro id que bater vira a rotina_selecionada
        return render_template("editar.html", rotina=rotina_selecionada)#vai pro html de edicao
    return "Rotina não encontrada", 404

# ROTA ADICIONAR EXERCICIO
@app.route("/adicionar_exercicio/<int:rotina_id>", methods=["POST"])#aqui vai chegar as informacoes escondidas
def adicionar_exercicio(rotina_id):
    rotina = next((r for r in minhas_rotinas if r.id == rotina_id), None)
    if rotina:
        nome = request.form.get("nome") #pega as informacoes que foram enviadas do metodo post
        series = request.form.get("series")
        reps = request.form.get("reps")
        
        # ATUALIZAÇÃO: Pega o grupo do HTML. Se não vier, assume "Outros" para não dar erro
        grupo_muscular = request.form.get("grupo_muscular", "Outros")
        
        #na hora adiciona nome series e reps para exercicios (agora com o grupo)
        rotina.exercicios.append(Exercicio(nome, series, reps, grupo_muscular))#vem do html e adiciona a rotina um exercicio
    return redirect(f"/editar/{rotina_id}")

# ROTA DE ACAO: REMOVER EXERCICIO
@app.route("/remover_exercicio/<int:rotina_id>/<nome_exercicio>")
def remover_exercicio(rotina_id, nome_exercicio):
    rotina = next((r for r in minhas_rotinas if r.id == rotina_id), None)
    if rotina:
        # filtra a lista, mantendo apenas os exercícios com nome diferente do que queremos remover
        rotina.exercicios = [ex for ex in rotina.exercicios if ex.nome != nome_exercicio]
    return redirect(f"/editar/{rotina_id}")


# ROTA DE DESEMPENHO
@app.route("/desempenho")
def desempenho():
    # 1. Sequência (Streak) atual
    sequencia_atual = 4 
    
    # 2. Captura o mês da URL (ex: ?mes=7). Padrão é Agosto (8).
    mes_atual = int(request.args.get("mes", 8))
    
    # Dicionário de meses e total de dias
    meses_info = {
        1: ("Janeiro", 31), 2: ("Fevereiro", 28), 3: ("Março", 31),
        4: ("Abril", 30), 5: ("Maio", 31), 6: ("Junho", 30),
        7: ("Julho", 31), 8: ("Agosto", 31), 9: ("Setembro", 30),
        10: ("Outubro", 31), 11: ("Novembro", 30), 12: ("Dezembro", 31)
    }
    
    nome_mes, total_dias = meses_info.get(mes_atual, ("Agosto", 31))
    
    # =========================================================================
    # CORREÇÃO DO BUG: Dicionário separando os dias treinados por CADA mês!
    # =========================================================================
    treinos_por_mes = {
        7: [3, 10, 17, 24],                    # Julho (exemplo de poucos treinos)
        8: [2, 5, 8, 12, 15, 19, 22, 26, 28],   # Agosto (seus dias originais)
        9: [1, 4, 6, 11, 14, 18, 21, 25, 30]    # Setembro (dias diferentes)
    }
    
    # Pega os dias do mês atual. Se o mês não estiver no dicionário, retorna lista vazia ([])
    dias_treinados_mes = treinos_por_mes.get(mes_atual, [])
    
    # Lógica das Setinhas
    mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
    mes_proximo = mes_atual + 1 if mes_atual < 12 else 1
    
    # Entregando os pacotes corretos para o Jinja2
    return render_template("desempenho.html", 
                           sequencia_semanal=sequencia_atual, 
                           dias_treinados=dias_treinados_mes,
                           nome_mes=nome_mes,
                           total_dias=total_dias,
                           mes_anterior=mes_anterior,
                           mes_proximo=mes_proximo)
if __name__ == "__main__":
    app.run(debug=True)