import matplotlib.pyplot as plt
import numpy as np

# --- DADOS REAIS (Retirados do teu print para N = 200, 400... 2000) ---
n_values = [250, 500, 750, 1000, 1250, 1500,
            1750, 2000, 2250, 2500, 2750, 3000]


tempos = [
    0.004,
    0.024,
    0.087,
    0.210,
    0.447,
    0.766,
    1.410,
    2.076,
    3.798,
    5.475,
    9.016,
    11.350]


# --- EIXO X: N ao Cubo ---
n_cubed = [n**3 for n in n_values]

# --- GRÁFICO ---
plt.figure(figsize=(10, 6))

# 1. Pontos
plt.scatter(n_cubed, tempos, color='green', s=50, label='Dados Experimentais')

# 2. Linha de Tendência
z = np.polyfit(n_cubed, tempos, 1)
p = np.poly1d(z)
plt.plot(n_cubed, p(n_cubed), "r--", linewidth=2,
         label='Tendência Linear (Teórica)')

# 3. Decoração
plt.title("Tempo em função da complexidade teórica")
plt.xlabel("Complexidade Teórica ($N^3$)")
plt.ylabel("Tempo (s)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

# Guardar
plt.savefig("grafico_final_12pontos.png")
print("Gráfico gerado: grafico_final_12pontos.png")
plt.show()
