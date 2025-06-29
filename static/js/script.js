document.addEventListener("DOMContentLoaded", function () {
  // ==================== Navigasi Aktif ====================
  const links = document.querySelectorAll("nav a");
  const currentUrl = window.location.pathname;
  links.forEach(link => {
    if (link.getAttribute("href") === currentUrl) {
      link.style.fontWeight = "bold";
      link.style.textDecoration = "underline";
    }
  });

  // ==================== Animasi Fade-in ====================
  const main = document.querySelector("main");
  if (main) {
    main.style.opacity = 0;
    main.style.transition = "opacity 1s ease-in";
    setTimeout(() => {
      main.style.opacity = 1;
    }, 100);
  }

  const scrollItems = document.querySelectorAll(".fade-in");
  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("appear");
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });
  scrollItems.forEach(item => observer.observe(item));

  // ==================== Tombol Ke Atas ====================
  const toTop = document.createElement("button");
  toTop.textContent = "⬆️";
  toTop.id = "toTopBtn";
  toTop.style.cssText = `
    position: fixed; bottom: 20px; right: 20px;
    display: none; background-color: #ff4081;
    color: white; border: none; padding: 12px;
    border-radius: 50%; cursor: pointer; font-size: 20px;
    z-index: 1000; box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  `;
  document.body.appendChild(toTop);

  window.addEventListener("scroll", () => {
    toTop.style.display = window.scrollY > 250 ? "block" : "none";
  });
  toTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // ==================== Kuis Edukasi (1 soal) ====================
  const quizForm = document.getElementById("quizForm");
  const quizResult = document.getElementById("quizResult");
  if (quizForm && quizResult) {
    quizForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const answer = document.querySelector('input[name="quiz"]:checked');
      if (!answer) {
        quizResult.textContent = "Silakan pilih jawaban terlebih dahulu.";
        quizResult.style.color = "#e91e63";
        return;
      }

      if (answer.value === "c") {
        quizResult.textContent = "✅ Benar! Bolos sekolah termasuk kenakalan remaja.";
        quizResult.style.color = "#4caf50";
      } else {
        quizResult.textContent = "❌ Salah. Jawaban yang benar adalah 'Bolos sekolah'.";
        quizResult.style.color = "#f44336";
      }
    });
  }

  // ==================== Kuis Interaktif (multi-soal) ====================
  const formKuis = document.getElementById("kuisForm");
  const hasilDiv = document.getElementById("hasil");
  if (formKuis && hasilDiv) {
    formKuis.addEventListener("submit", function (e) {
      e.preventDefault();
      const jawabanBenar = {
        q1: "B",
        q2: "C",
      };
      let skor = 0;
      let total = Object.keys(jawabanBenar).length;

      for (let key in jawabanBenar) {
        const jawabanUser = formKuis.elements[key]?.value;
        if (jawabanUser === jawabanBenar[key]) {
          skor++;
        }
      }

      const persentase = (skor / total) * 100;
      hasilDiv.innerHTML = `
        <h2>Hasil Kuis</h2>
        <p>Skor kamu: ${skor} dari ${total}</p>
        <p>Persentase: ${persentase.toFixed(0)}%</p>
        ${persentase >= 60 ? '<p>🎉 Selamat, kamu lulus!</p>' : '<p>😢 Sayang sekali, coba lagi ya!</p>'}
      `;
      hasilDiv.style.display = "block";
      formKuis.style.display = "none";
    });
  }

  // ==================== Konsultasi ke WhatsApp ====================
  const konsultasiForm = document.getElementById("konsultasiForm");
  if (konsultasiForm) {
    konsultasiForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const nama = document.getElementById("nama").value.trim();
      const masalah = document.getElementById("masalah").value.trim();
      if (!nama || !masalah) return alert("Harap isi semua kolom.");

      const pesan = `Halo, saya ${nama}. Saya ingin konsultasi tentang:\n${masalah}`;
      const nomorWa = "6285624375695"; // Ganti dengan nomor admin
      const url = `https://wa.me/${nomorWa}?text=${encodeURIComponent(pesan)}`;
      window.open(url, "_blank");
    });
  }
});
