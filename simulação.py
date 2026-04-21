import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = [12, 8]

def simular_com_historico(x_inicial, p, max_steps=1000, n_simulacoes=1000):
    """
    Simula e armazena os dados detalhados para o gráfico.
    """
    todas_trajetorias = []
    resultados = []
    historico_passos = []

    for _ in range(n_simulacoes):
        posicao = x_inicial
        trajetoria = [posicao]
        passos = []
        caiu = False

        for _ in range(max_steps):
            if random.random() < p:
                passo = 1
                posicao += 1  # Afasta da borda
            else:
                passo = -1
                posicao -= 1  # Aproxima da borda

            trajetoria.append(posicao)
            passos.append(passo)

            if posicao == 0:
                caiu = True
                break

        todas_trajetorias.append(trajetoria)
        resultados.append("Caiu" if caiu else "Sobreviveu")  # ✅ corrigido
        historico_passos.extend(passos)

    return todas_trajetorias, resultados, historico_passos


# --- Parâmetros ---
x_ini = 2
prob_afasta = 0.6
n_grafico = 1000

trajetorias, resultados, todos_passos = simular_com_historico(x_ini, prob_afasta, n_simulacoes=n_grafico)

# --- Painel Gráfico ---
fig, axes = plt.subplots(2, 1)
fig.suptitle(f'Simulação do Despenhadeiro (p={prob_afasta}, x={x_ini})', fontsize=16)

# Gráfico 1: Trajetórias Individuais
ax1 = axes[0]
for traj in trajetorias[:100]:
    color = 'red' if traj[-1] == 0 else 'green'
    alpha = 0.3 if color == 'red' else 0.15  # ✅ verde mais visível
    ax1.plot(traj, color=color, alpha=alpha, linewidth=1)

ax1.axhline(y=0, color='black', linestyle='-', linewidth=2, label='Borda')
ax1.set_title("Amostra de 100 Trajetórias Individuais", fontsize=14)
ax1.set_ylabel("Posição (Passos da Borda)")
ax1.set_xlabel("Número de Passos Dados")

# Gráfico 2: Resumo Geral
ax2 = axes[1]
count_caiu = resultados.count("Caiu")
count_viveu = resultados.count("Sobreviveu")  # ✅ corrigido

ax2.bar(['Caiu', 'Sobreviveu'], [count_caiu, count_viveu], color=['#e74c3c', '#2ecc71'])
ax2.set_title(f"Resultado Final ({n_grafico} Simulações)", fontsize=14)
ax2.set_ylabel("Quantidade de Simulações")

for bar in ax2.patches:
    ax2.annotate(
        f'{int(bar.get_height())}\n({bar.get_height() / n_grafico:.1%})',
        (bar.get_x() + bar.get_width() / 2, bar.get_height() / 2),
        ha='center', va='center', color='white', fontweight='bold'
    )

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# --- Estatísticas de Passos ---
pf = todos_passos.count(1)
pt = todos_passos.count(-1)
print(f"Total de passos dados nas simulações: {len(todos_passos)}")
print(f"Passos para FRENTE (afasta): {pf} ({pf/len(todos_passos):.1%})")
print(f"Passos para TRÁS (aproxima): {pt} ({pt/len(todos_passos):.1%})")
