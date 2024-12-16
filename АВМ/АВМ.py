import numpy as np 
import matplotlib.pyplot as plt


R_n = 1.9 
f = 0.005 
G_n_coefficient = 0.1


p_profile = [1, 5, 6, 8, 10, 12, 14, 16, 16, 16, 14, 16, 14, 10, 9, 8, 6, 4, 3, 1]
n_processors = 16 


O_n = sum(p_profile)

O_1 = O_n / R_n  
T_1 = O_1  


T_n = len(p_profile) 
P_avg = O_n / T_n 
S_n = T_1 / T_n 
E_n = S_n / n_processors 
U_n = O_n / (n_processors * T_n) 
C_n = 1 / R_n 
Q_n = S_n * E_n * C_n 


results_metrics = {
    "Общий объем вычислений O(n)": O_n,
    "Объем вычислений для однопроцессорной системы O(1)": O_1,
    "Средний параллелизм P_avg": P_avg,
    "Ускорение S(n)": S_n,
    "Эффективность E(n)": E_n,
    "Утилизация U(n)": U_n,
    "Сжатие C(n)": C_n,
    "Качество Q(n)": Q_n,
}


n_values = np.array([2, 8, 32, 128, 512]) 
G_n = G_n_coefficient * n_values


S_amdahl = n_values / (1 + (n_values - 1) * f)


S_gustafson = n_values + (1 - n_values) * f


S_sana_nai = (f + (1 - f) * G_n) / (f + (1 - f) * G_n / n_values)

plt.figure(figsize=(12, 6))
plt.plot(n_values, S_amdahl, label="Закон Амдала", marker="o", linestyle="-")
plt.plot(n_values, S_gustafson, label="Закон Густафсона", marker="s", linestyle="--")
plt.plot(n_values, S_sana_nai, label="Закон Сана-Ная", marker="^", linestyle="-.")
plt.xlabel("Количество процессоров (n)")
plt.ylabel("Ускорение (S(n))")
plt.title("Графики ускорения по трем законам")
plt.legend()
plt.grid(True)
plt.show()

print(results_metrics)