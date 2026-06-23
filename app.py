import re

from flask import Flask, render_template, request, jsonify

from fitness_rules import (
    hitung_bmi,
    kategori_bmi,
    buat_jadwal,
    tips_fitness
)

def normalisasi_tujuan(text):

    text = text.lower()

    if any(kata in text for kata in [
        "diet",
        "kurus",
        "turun berat",
        "menurunkan berat",
        "fat loss"
    ]):
        return "diet"

    if any(kata in text for kata in [
        "otot",
        "massa otot",
        "muscle",
        "membentuk otot",
        "bulking"
    ]):
        return "otot"

    if any(kata in text for kata in [
        "bugar",
        "kebugaran",
        "sehat",
        "fitness"
    ]):
        return "kebugaran"

    return None


def normalisasi_level(text):

    text = text.lower()

    if any(kata in text for kata in [
        "pemula",
        "baru",
        "beginner",
        "awam"
    ]):
        return "pemula"

    if any(kata in text for kata in [
        "menengah",
        "intermediate",
        "sedang"
    ]):
        return "menengah"

    return None

def ekstrak_data(text):

    text = text.lower()

    hasil = {
        "tujuan": normalisasi_tujuan(text),
        "level": normalisasi_level(text),
        "berat": None,
        "tinggi": None
    }

    # Cari berat
    berat_match = re.search(
        r'berat\s*(?:badan)?\s*(\d+)',
        text
    )

    if berat_match:
        hasil["berat"] = float(
            berat_match.group(1)
        )

    # Cari tinggi
    tinggi_match = re.search(
        r'tinggi\s*(?:badan)?\s*(\d+)',
        text
    )

    if tinggi_match:
        hasil["tinggi"] = float(
            tinggi_match.group(1)
        )

    return hasil

app = Flask(__name__)

# Menyimpan percakapan sementara
user_data = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    
    data = request.get_json()

    session_id = data["session_id"]
    message = data["message"].lower()
    
    faq = {
    "apa itu bmi":
        "BMI adalah Body Mass Index, digunakan untuk mengukur kategori berat badan.",

    "cara diet":
        "Diet sehat dilakukan dengan mengatur kalori, olahraga rutin, dan tidur cukup.",

    "cara menambah otot":
        "Fokus pada latihan beban dan konsumsi protein yang cukup."
    }

    if message in faq:
        return jsonify({
        "reply": faq[message]
        })

    data_cepat = ekstrak_data(message)

    if (
        data_cepat["tujuan"]
        and data_cepat["level"]
        and data_cepat["berat"]
        and data_cepat["tinggi"]
    ):
    
        bmi = hitung_bmi(
            data_cepat["berat"],
            data_cepat["tinggi"]
        )
    
        kategori = kategori_bmi(bmi)
    
        jadwal = buat_jadwal(
            data_cepat["tujuan"],
            data_cepat["level"]
        )
    
        tips = tips_fitness(
            data_cepat["tujuan"]
        )
    
        hasil = f"""
    BMI: {bmi}
    
    Kategori: {kategori}
    
    📅 Jadwal Latihan:
    """
    
        for hari, latihan in jadwal.items():
            hasil += f"\n📅 {hari}\n{latihan}\n"
    
        hasil += "\n💡 Tips:\n"
    
        for tip in tips:
            hasil += f"- {tip}\n"
    
        return jsonify({
            "reply": hasil
        })

    # Buat sesi baru
    if session_id not in user_data:

        user_data[session_id] = {
            "step": "menu"
        }

        return jsonify({
            "reply":
            """Halo! 👋

            Saya FitBot.

            Ketik:

            - konsultasi bertahap

            atau langsung tulis:

            'Saya ingin membentuk otot, berat 55 kg, tinggi 170 cm, saya pemula'
            """
                })

    state = user_data[session_id]

    # MENU
    if state["step"] == "menu":

        if "bertahap" in message:

            state["step"] = "tujuan"

            return jsonify({
                "reply":
                "Baik 😊\n\nApa tujuan kebugaranmu?\n\nContoh:\n- Diet\n- Membentuk otot\n- Menjaga kebugaran"
            })

        return jsonify({
            "reply":
            "Ketik 'konsultasi bertahap' atau langsung tulis data lengkapmu."
        })
    
    # STEP 1
    if state["step"] == "tujuan":

        tujuan = normalisasi_tujuan(message)

        if not tujuan:
            return jsonify({
            "reply":
            "🤔 Saya kurang memahami tujuanmu.\n\nContoh:\n- Saya ingin diet\n- Saya ingin membentuk otot\n- Saya ingin hidup lebih sehat"
            })

        state["tujuan"] = tujuan
        state["step"] = "berat"

        return jsonify({
            "reply":
            "Berapa berat badanmu (kg)?"
        })

    # STEP 2
    elif state["step"] == "berat":

        try:
            berat = float(message)

            if berat <= 0:
                raise ValueError

            state["berat"] = berat
            state["step"] = "tinggi"

            return jsonify({
                "reply":
                "Berapa tinggi badanmu (cm)?"
            })

        except:
            return jsonify({
                "reply":
                "⚠️ Masukkan berat badan dalam angka.\n\nContoh: 70"
        })

    # STEP 3
    elif state["step"] == "tinggi":

        try:
            tinggi = float(message)

            if tinggi <= 0:
                raise ValueError

            state["tinggi"] = tinggi
            state["step"] = "level"

            return jsonify({
                "reply":
                "Level latihanmu?\n\n(pemula / menengah)"
            })

        except:
            return jsonify({
                "reply":
                "⚠️ Masukkan tinggi badan dalam angka.\n\nContoh: 170"
            })

    # STEP 4
    elif state["step"] == "level":

        level = normalisasi_level(message)

        if not level:
            return jsonify({
                "reply":
                "🤔 Saya tidak mengenali level tersebut.\n\nPilih:\n- Pemula\n- Menengah"
            })
        
        state["level"] = level

        bmi = hitung_bmi(
            state["berat"],
            state["tinggi"]
        )

        kategori = kategori_bmi(bmi)

        jadwal = buat_jadwal(
            state["tujuan"],
            state["level"]
        )

        tips = tips_fitness(
            state["tujuan"]
        )

        hasil = f"""
        BMI: {bmi}
        
        Kategori: {kategori}
        
        📅 Jadwal Latihan:
        
        """

        for hari, latihan in jadwal.items():
            hasil += f"\n📅 {hari}\n{latihan}\n"

        hasil += "\n💡 Tips:\n"

        for tip in tips:
            hasil += f"- {tip}\n"

        del user_data[session_id]

        return jsonify({
            "reply": hasil
        })


if __name__ == "__main__":
    app.run(debug=True)