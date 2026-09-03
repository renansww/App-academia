document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.fade-in');

    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('visible');
        }, index * 150);
    });
});

let segundos = 0;
let minutos = 0;
let intervalo = null;
let rodando = false;

function iniciarCronometro() {
    const display = document.getElementById('cronometro');
    const inputTempoFinal = document.getElementById('tempo_final');

    if (rodando) {
        clearInterval(intervalo);
        rodando = false;
    } else {
        rodando = true;
        intervalo = setInterval(() => {
            segundos++;
            if (segundos === 60) {
                minutos++;
                segundos = 0;
            }

            const txtMin = minutos < 10 ? "0" + minutos : minutos;
            const txtSeg = segundos < 10 ? "0" + segundos : segundos;
            const tempoFormatado = `${txtMin}:${txtSeg}`;

            if (display) display.innerText = tempoFormatado;
            if (inputTempoFinal) inputTempoFinal.value = tempoFormatado;
        }, 1000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const btnPlay = document.getElementById('btn-timer-control');
    if (btnPlay) {
        btnPlay.addEventListener('click', iniciarCronometro);
    }

    if (document.getElementById('cronometro')) {
        iniciarCronometro();
    }
});

function adicionarSerie(btn, nomeExercicio) {
    const container = btn.previousElementSibling;
    const divLinha = document.createElement('div');
    divLinha.className = 'form-linha serie-linha fade-in mb-15';
    divLinha.style.alignItems = 'center';
    
    divLinha.innerHTML = `
        <select class="input-treino input-tipo-serie" style="flex: 1;" onchange="verificarCor(this)">
            <option value="Normal">Normal</option>
            <option value="Aquecimento">Aquecimento</option>
            <option value="Falha">Falha</option>
        </select>
        <input type="number" class="input-treino input-carga" style="flex: 1;" placeholder="Kg" oninput="autoFillCarga(this)">
        <input type="number" class="input-treino input-reps" style="flex: 1;" placeholder="Reps" oninput="autoFillReps(this)">
        <input type="checkbox" class="checkbox-serie" style="transform: scale(1.5); margin: 0 10px; cursor: pointer;">
    `;
    
    container.appendChild(divLinha);
    
    setTimeout(() => {
        divLinha.classList.add('visible');
    }, 10);
}

function verificarCor(selectElem) {
    const cor = {
        'Normal': '#e0e0e0',
        'Aquecimento': '#4caf50',
        'Falha': '#f44336'
    };
    selectElem.style.color = cor[selectElem.value] || '#e0e0e0';
}

function autoFillCarga(inputCarga) {
    const container = inputCarga.closest('.series-container');
    const linhas = Array.from(container.querySelectorAll('.serie-linha'));
    const indexAtual = linhas.indexOf(inputCarga.closest('.serie-linha'));
    const valor = inputCarga.value;

    for (let i = indexAtual + 1; i < linhas.length; i++) {
        const proximoInput = linhas[i].querySelector('.input-carga');
        if (!proximoInput.value) {
            proximoInput.value = valor;
        }
    }
}

function autoFillReps(inputReps) {
    const container = inputReps.closest('.series-container');
    const linhas = Array.from(container.querySelectorAll('.serie-linha'));
    const indexAtual = linhas.indexOf(inputReps.closest('.serie-linha'));
    const valor = inputReps.value;

    for (let i = indexAtual + 1; i < linhas.length; i++) {
        const proximoInput = linhas[i].querySelector('.input-reps');
        if (!proximoInput.value) {
            proximoInput.value = valor;
        }
    }
}

function adicionarExercicioExtra() {
    const nomeInput = document.getElementById('novo_exercicio_nome');
    const nomeExercicio = nomeInput.value.trim();
    if (!nomeExercicio) {
        alert("Por favor, digite o nome do exercício.");
        return;
    }
    
    const lista = document.getElementById('lista-exercicios');
    
    const divCard = document.createElement('div');
    divCard.className = 'card-rotina fade-in exercicio-card';
    divCard.dataset.nome = nomeExercicio;
    
    divCard.innerHTML = `
        <div class="card-header flex-between-start">
            <div>
                <h2>${nomeExercicio}</h2>
                <span class="foco">Adicionado Extra</span>
            </div>
        </div>
        <div class="series-container mt-15">
        </div>
        <button type="button" class="btn-cronometro mt-10 btn-add-serie" onclick="adicionarSerie(this, '${nomeExercicio}')">+ Adicionar Série</button>
    `;
    
    lista.appendChild(divCard);
    
    setTimeout(() => {
        divCard.classList.add('visible');
    }, 10);
    nomeInput.value = "";
}

function prepararEnvio(event) {
    event.preventDefault();
    const listaExercicios = document.querySelectorAll('.exercicio-card');
    const dadosFinais = [];
    
    listaExercicios.forEach(card => {
        const nomeExercicio = card.dataset.nome;
        const series = card.querySelectorAll('.serie-linha');
        const seriesFinalizadas = [];
        
        series.forEach(linha => {
            const finalizada = linha.querySelector('.checkbox-serie').checked;
            if (finalizada) {
                const tipo = linha.querySelector('.input-tipo-serie').value;
                const carga = linha.querySelector('.input-carga').value || 0;
                const reps = linha.querySelector('.input-reps').value || 0;
                
                seriesFinalizadas.push({
                    tipo: tipo,
                    carga: parseFloat(carga),
                    reps: parseInt(reps, 10)
                });
            }
        });
        
        if (seriesFinalizadas.length > 0) {
            dadosFinais.push({
                exercicio: nomeExercicio,
                series: seriesFinalizadas
            });
        }
    });
    document.getElementById('dados_treino').value = JSON.stringify(dadosFinais);
    event.target.submit();
}

function adicionarSerieEdicao(btn) {
    const container = btn.previousElementSibling;
    const divLinha = document.createElement('div');
    divLinha.className = 'form-linha serie-edicao-linha fade-in mb-15';
    divLinha.style.alignItems = 'center';
    
    divLinha.innerHTML = `
        <select class="input-treino input-tipo-serie" style="flex: 1;" onchange="verificarCor(this)">
            <option value="Normal">Normal</option>
            <option value="Aquecimento">Aquecimento</option>
            <option value="Falha">Falha</option>
        </select>
        <input type="number" class="input-treino input-meta-reps" style="flex: 1;" placeholder="Meta Reps" required>
        <button type="button" class="btn-descartar" style="flex: 0; padding: 10px;" onclick="this.parentElement.remove()">X</button>
    `;
    
    container.appendChild(divLinha);
    
    setTimeout(() => {
        divLinha.classList.add('visible');
    }, 10);
}

function prepararEnvioEdicao(event) {
    event.preventDefault();
    const form = event.target;
    
    const linhas = form.querySelectorAll('.serie-edicao-linha');
    const series = [];
    
    linhas.forEach(linha => {
        const tipo = linha.querySelector('.input-tipo-serie').value;
        const meta_reps = linha.querySelector('.input-meta-reps').value;
        
        series.push({
            tipo: tipo,
            meta_reps: meta_reps
        });
    });
    if (series.length === 0) {
        alert("Adicione pelo menos uma série ao exercício!");
        return;
    }
    
    document.getElementById('dados_series_edicao').value = JSON.stringify(series);
    
    form.submit();
}