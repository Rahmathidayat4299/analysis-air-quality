<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README - Aplikasi Analisis Kualitas Udara</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            background-color: #f4f4f4;
            color: #333;
        }
        h1, h2 {
            color: #2c3e50;
        }
        code {
            background-color: #e1e1e1;
            padding: 2px 4px;
            border-radius: 4px;
        }
        pre {
            background-color: #e1e1e1;
            padding: 10px;
            border-radius: 4px;
            overflow: auto;
        }
        ul {
            margin: 10px 0;
            padding: 0 20px;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Aplikasi Analisis Kualitas Udara</h1>

    <h2>Cara Menjalankan Aplikasi</h2>

    <ol>
        <li>
            <strong>Kloning Repositori:</strong>
            <pre><code>git clone https://github.com/Rahmathidayat4299/analysis-air-quality.git</code></pre>
        </li>
        <li>
            <strong>Buat Lingkungan Virtual (Opsional):</strong>
            <pre><code>python -m venv venv</code></pre>
            <pre><code>source venv/bin/activate  # Untuk pengguna Linux/Mac</code></pre>
            <pre><code>venv\Scripts\activate     # Untuk pengguna Windows</code></pre>
        </li>
        <li>
            <strong>Instal Pustaka:</strong>
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li>
            <strong>Jalankan Aplikasi:</strong>
            <pre><code>streamlit run streamlit_app.py</code></pre>
        </li>
        <li>
            <strong>Akses Aplikasi:</strong>
            <p>Aplikasi akan terbuka secara otomatis di browser Anda. Jika tidak, salin alamat URL yang ditampilkan di terminal dan buka di browser.</p>
        </li>
    </ol>

    <h2>Fitur Aplikasi</h2>
    <ul>
        <li>Menampilkan statistik deskriptif kualitas udara.</li>
        <li>Menyediakan visualisasi grafik untuk pemahaman yang lebih baik.</li>
        <li>Antarmuka pengguna yang interaktif dan responsif.</li>
    </ul>

    <h2>Kebutuhan Sistem</h2>
    <ul>
        <li>Python 3.6 atau lebih tinggi.</li>
        <li>Dependensi dalam <code>requirements.txt</code>.</li>
    </ul>

    <h2>Lisensi</h2>
    <p>Proyek ini dilisensikan di bawah MIT License.</p>
</body>
</html>
