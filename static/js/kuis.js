document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("kuisForm");
  const hasilDiv = document.getElementById("hasil");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const nama = document.getElementById("nama").value;
    const soalEls = form.querySelectorAll(".soal");
    let skor = 0;
    let total = soalEls.length;

    soalEls.forEach((soal, index) => {
      const nomor = index + 1;
      const benar = soal.querySelector(`input[name="jawaban_benar_q${nomor}"]`).value;
      const jawabanUser = form.querySelector(`input[name="q${nomor}"]:checked`);
      if (jawabanUser && jawabanUser.value.toUpperCase() === benar.toUpperCase()) {
        skor++;
      }
      
      
    });

    const persentase = (skor / total) * 100;
    const lulus = persentase >= 60;

    hasilDiv.innerHTML = `
  <h2 style="color: black;">Hasil Kuis</h2>
  <p>Skor kamu: ${skor} dari ${total} (${persentase.toFixed(0)}%)</p>
  ${lulus ? `
    <p>🎉 Selamat ${nama}, kamu lulus!</p>
    <form method="POST" action="/buat-sertifikat">
      <input type="hidden" name="nama" value="${nama}">
      <input type="hidden" name="skor" value="${persentase.toFixed(0)}">
      <button type="submit">🎓 Unduh Sertifikat</button>
    </form>
  ` : `
    <p>😢 Sayang sekali, coba lagi ya!</p>
  `}
  <button id="ulangKuis" style="margin-top:20px;">🔁 Coba Lagi</button>
`;


    hasilDiv.style.display = "block";
    document.getElementById("ulangKuis").addEventListener("click", () => {
      window.location.reload();
    });
    
    form.style.display = "none";
  });
});
