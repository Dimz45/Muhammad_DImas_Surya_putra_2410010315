from fitness_rules import *

bmi = hitung_bmi(80, 170)

print("BMI:", bmi)
print("Kategori:", kategori_bmi(bmi))

print("\n=== Jadwal Latihan ===")

jadwal = buat_jadwal("diet", "pemula")

for hari, latihan in jadwal.items():
    print(f"{hari}: {latihan}")

print("\n=== Tips ===")

for tip in tips_fitness("diet"):
    print("-", tip)