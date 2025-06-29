from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
import os
import random
from reportlab.pdfgen import canvas
from models import create_tables, buat_tabel_kuis, buat_tabel_curhat

app = Flask(__name__)
app.secret_key = 'rahasia_admin'

# ====== Buat tabel database saat awal ======
create_tables()
buat_tabel_kuis()
buat_tabel_curhat()

# ===================== HALAMAN PUBLIK =====================

@app.route('/')
def index():
    motivasi_list = [
        "Jangan takut gagal, takutlah untuk tidak mencoba.",
        "Langkah kecil hari ini adalah awal masa depan hebat.",
        "Kesuksesan butuh proses, bukan keajaiban.",
        "Jadilah versi terbaik dari dirimu sendiri.",
        "Belajar dari kemarin, hidup untuk hari ini, harapan untuk besok."
        "Jangan takut gagal, karena gagal adalah bagian dari proses belajar.",
        "Masa depanmu ditentukan oleh keputusanmu hari ini.",
        "Remaja hebat adalah yang bisa mengendalikan dirinya.",
        "Hindari kenakalan, bangun masa depan.",
        "Jadilah versi terbaik dari dirimu, bukan yang lain."
    ]
    motivasi = random.choice(motivasi_list)
    return render_template('index.html', motivasi=motivasi)

@app.route('/edukasi-user')
def edukasi_user():
    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM edukasi")
    data = c.fetchall()
    conn.close()
    return render_template('edukasi_user.html', data=data)


@app.route('/curhat', methods=['GET', 'POST'])
def curhat():
    if request.method == 'POST':
        isi = request.form['isi']
        conn = sqlite3.connect("database/data.db")
        c = conn.cursor()
        c.execute("INSERT INTO curhat (isi) VALUES (?)", (isi,))
        conn.commit()
        conn.close()
        return render_template('curhat.html', sukses=True)
    return render_template('curhat.html', sukses=False)

@app.route('/kontak')
def kontak_user():
    return render_template('kontak.html')

@app.route('/buat-sertifikat', methods=['POST'])
def buat_sertifikat():
    nama = request.form['nama']
    skor = int(request.form['skor'])

    if skor < 60:
        return "Maaf, kamu belum memenuhi syarat untuk sertifikat.", 400

    os.makedirs("sertifikat", exist_ok=True)
    file_path = f"sertifikat/{nama.replace(' ', '_')}_sertifikat.pdf"

    c = canvas.Canvas(file_path)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "SERTIFIKAT KELULUSAN")
    c.setFont("Helvetica", 14)
    c.drawString(100, 700, f"Diberikan kepada: {nama}")
    c.drawString(100, 670, f"Skor kelulusan: {skor}%")
    c.drawString(100, 640, "Selamat! Kamu telah lulus kuis edukasi remaja.")
    c.save()

    return send_file(file_path, as_attachment=True)

# ===================== ADMIN LOGIN =====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if user == 'admin' and pw == 'admin123':
            session['admin'] = True
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Login gagal')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

# ===================== DASHBOARD =====================

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('login'))
    return render_template('admin/dashboard.html')

# ===================== MANAJEMEN EDUKASI =====================

@app.route('/edukasi')
def edukasi():
    if not session.get('admin'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM edukasi")
    data = c.fetchall()
    conn.close()
    return render_template('manage_edukasi.html', data=data)

@app.route('/edukasi/tambah', methods=['POST'])
def tambah_edukasi():
    if not session.get('admin'):
        return redirect(url_for('login'))

    judul = request.form['judul']
    isi = request.form['isi']

    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute("INSERT INTO edukasi (judul, isi) VALUES (?, ?)", (judul, isi))
    conn.commit()
    conn.close()
    return redirect(url_for('edukasi'))

@app.route('/edukasi/edit/<int:id>', methods=['GET', 'POST'])
def edit_edukasi(id):
    if not session.get('admin'):
        return redirect(url_for('login'))

    conn = sqlite3.connect("database/data.db")
    c = conn.cursor()

    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        c.execute("UPDATE edukasi SET judul=?, isi=? WHERE id=?", (judul, isi, id))
        conn.commit()
        conn.close()
        return redirect(url_for('edukasi'))

    c.execute("SELECT * FROM edukasi WHERE id=?", (id,))
    data = c.fetchone()
    conn.close()
    return render_template('edit_edukasi.html', data=data)

@app.route('/edukasi/hapus/<int:id>')
def hapus_edukasi(id):
    if not session.get('admin'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute("DELETE FROM edukasi WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('edukasi'))

# ===================== MANAJEMEN KUIS =====================
@app.route('/kuis-user')
def kuis_user():
    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM kuis")
    data = c.fetchall()
    conn.close()
    return render_template('kuis_user.html', data=data)

@app.route('/kuis')
def kuis():
    if not session.get('admin'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM kuis")
    data = c.fetchall()
    conn.close()
    return render_template('manage_kuis.html', data=data)

@app.route('/kuis/tambah', methods=['POST'])
def tambah_kuis():
    if not session.get('admin'):
        return redirect(url_for('login'))

    pertanyaan = request.form['pertanyaan']
    a = request.form['pilihan_a']
    b = request.form['pilihan_b']
    c_ = request.form['pilihan_c']
    d = request.form['pilihan_d']
    jawaban = request.form['jawaban']

    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute('''INSERT INTO kuis 
        (pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, jawaban) 
        VALUES (?, ?, ?, ?, ?, ?)''', (pertanyaan, a, b, c_, d, jawaban))
    conn.commit()
    conn.close()
    return redirect(url_for('kuis'))

@app.route('/kuis/hapus/<int:id>')
def hapus_kuis(id):
    if not session.get('admin'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute("DELETE FROM kuis WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('kuis'))



# ===================== LIHAT CURHAT (ADMIN) =====================

@app.route('/admin/curhat')
def lihat_curhat():
    if not session.get('admin'):
        return redirect(url_for('login'))

    conn = sqlite3.connect("database/data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM curhat ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return render_template("admin/lihat_curhat.html", data=data)

# ===================== RUN APP =====================

if __name__ == '__main__':
    app.run(debug=True)
