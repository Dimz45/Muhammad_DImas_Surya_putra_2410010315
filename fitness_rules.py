# fitness_rules.py

# =========================
# BMI
# =========================

def hitung_bmi(berat, tinggi):
    tinggi_m = tinggi / 100
    bmi = berat / (tinggi_m ** 2)
    return round(bmi, 2)


def kategori_bmi(bmi):
    if bmi < 18.5:
        return "Kurus"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesitas"


# =========================
# KNOWLEDGE BASE
# =========================

PROGRAM_LATIHAN = {

    ("diet", "pemula"): {
        "Senin": "Jalan cepat 30 menit",
        "Selasa": "Stretching 15 menit",
        "Rabu": "Squat 3x10",
        "Kamis": "Istirahat aktif",
        "Jumat": "Jogging 30 menit",
        "Sabtu": "Bersepeda 30 menit",
        "Minggu": "Istirahat"
    },

    ("diet", "menengah"): {
        "Senin": "Jogging 45 menit",
        "Selasa": "Burpee 3x15",
        "Rabu": "Squat 4x15",
        "Kamis": "Plank 4x45 detik",
        "Jumat": "Jogging 45 menit",
        "Sabtu": "Bersepeda 45 menit",
        "Minggu": "Istirahat"
    },

    ("otot", "pemula"): {
        "Senin": "Push-up 3x10",
        "Selasa": "Sit-up 3x15",
        "Rabu": "Istirahat",
        "Kamis": "Push-up 3x12",
        "Jumat": "Plank 3x30 detik",
        "Sabtu": "Bodyweight Squat 3x10",
        "Minggu": "Istirahat"
    },

    ("otot", "menengah"): {
        "Senin": "Push-up 4x15",
        "Selasa": "Pull-up 3x8",
        "Rabu": "Sit-up 4x20",
        "Kamis": "Dumbbell Curl 3x12",
        "Jumat": "Plank 4x45 detik",
        "Sabtu": "Squat 4x15",
        "Minggu": "Istirahat"
    },

    ("kebugaran", "pemula"): {
        "Senin": "Jalan santai 20 menit",
        "Selasa": "Stretching",
        "Rabu": "Senam ringan",
        "Kamis": "Istirahat",
        "Jumat": "Jalan santai 20 menit",
        "Sabtu": "Stretching",
        "Minggu": "Istirahat"
    },

    ("kebugaran", "menengah"): {
        "Senin": "Jogging 30 menit",
        "Selasa": "Burpee 3x10",
        "Rabu": "Stretching",
        "Kamis": "Jogging 30 menit",
        "Jumat": "Plank 3x45 detik",
        "Sabtu": "Senam kardio",
        "Minggu": "Istirahat"
    }
}


# =========================
# INFERENCE ENGINE
# =========================

def buat_jadwal(tujuan, level):
    return PROGRAM_LATIHAN.get(
        (tujuan, level),
        {}
    )


# =========================
# TIPS
# =========================

def tips_fitness(tujuan):

    if tujuan == "diet":
        return [
            "Kurangi minuman manis.",
            "Perbanyak air putih.",
            "Tidur 7-8 jam setiap hari."
        ]

    elif tujuan == "otot":
        return [
            "Perbanyak konsumsi protein.",
            "Istirahat cukup setelah latihan.",
            "Latih otot secara konsisten."
        ]

    else:
        return [
            "Lakukan olahraga secara rutin.",
            "Jaga pola makan seimbang.",
            "Tetap aktif setiap hari."
        ]