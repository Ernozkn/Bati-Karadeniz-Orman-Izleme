# 🚀 Hızlı Başlangıç Rehberi

Bu rehber, Batı Karadeniz Orman İzleme Sistemi'ni kurmak ve çalıştırmak için adım adım talimatlar sağlar.

---

## 📋 Ön Koşullar

- **Python 3.8 veya daha yeni sürüm**
- **Git** (kod klonlama için)
- **pip** (Python paket yöneticisi)
- **Disk alanı:** Minimum 2GB (veri dosyaları için)

### Windows'ta Python Kontrolü
```powershell
python --version
pip --version
```

### macOS/Linux'ta Python Kontrolü
```bash
python3 --version
pip3 --version
```

---

## 1️⃣ Depoyu Klonla

```bash
git clone https://github.com/Ernozkn/Bati-Karadeniz-Orman-Izleme.git
cd Bati-Karadeniz-Orman-Izleme
```

---

## 2️⃣ Sanal Ortam Oluştur

### Windows
```powershell
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

Sanal ortamın aktif olduğunu doğrulamak için prompt'un başında `(venv)` görmeli.

---

## 3️⃣ Bağımlılıkları Yükle

### Temel Kurulum (Önerilir)
```bash
pip install -r requirements.txt
```

### Geliştirici Kurulum
```bash
pip install -e ".[dev]"
```

### Tam Kurulum (Tüm Özellikleri)
```bash
pip install -e ".[full]"
```

Kurulum başarılı oldu mu kontrol et:
```bash
python -c "import src; print(src.__version__)"
```

---

## 4️⃣ Google Earth Engine Kurulumu (Opsiyonel)

GEE API'sini kullanmak için:

```bash
# GEE yetkilendirmesi (tarayıcı açılacak)
earthengine authenticate

# Doğrulama
python -c "import ee; ee.Initialize(project='ee-project'); print('✅ GEE bağlantısı başarılı')"
```

> **Not:** GEE credentials dosyası `~/.config/earthengine/` dizinine kaydedilecek

---

## 5️⃣ Jupyter Notebook'u Başlat

```bash
jupyter notebook notebooks/orman_analizi.ipynb
```

Tarayıcı otomatik açılacak ve notebook yüklenecek.

---

## 📊 Ana Analiz Çalıştırma

### Python Script'i Olarak Çalıştır

```python
from src import VeriYoneticisi, OrmanAnalizi, Gorsellestiric

# Veri oluştur
veri = VeriYoneticisi()
orman_v, nbr_v, maden_v = veri.tum_verileri_olustur()

# Analiz yap
analiz = OrmanAnalizi(orman_v, nbr_v, maden_v)
trend = analiz.tum_iller_trend_analizi()

for il, sonuc in trend.items():
    print(f"\n{il}: Trend = {sonuc.trend_yonu}, p-değeri = {sonuc.p_degeri:.6f}")

# Görselleştir
gorsel = Gorsellestiric(orman_v, nbr_v, maden_v)
fig = gorsel.orman_alani_grafigi()
```

### Jupyter Notebook'ta

Notebook hücreleri sırayla çalıştır (`Shift+Enter`):

1. **Kütüphane İçe Aktar** - Tüm gerekli modülleri yükleme
2. **Veri Keşfi** - Örnek verileri inceleme
3. **Analiz Çalıştır** - İstatistiksel analizler
4. **Sonuçları Görselleştir** - Grafikler ve haritalar

---

## 🗺️ Google Earth Engine Pipeline Kullanımı

```python
from src.gee_pipeline import Goruntu_Isleme_Pipeline

# Pipeline başlat
pipeline = Goruntu_Isleme_Pipeline()

# Batı Karadeniz bölgesi
bolge = {
    "bati": 31.5,
    "dogu": 33.5,
    "guney": 40.8,
    "kuzey": 42.0
}

# Yangın analizi
yangin_sonuc = pipeline.yangin_analizi_pipeline(
    bolge,
    "2023-08-15",    # Yangın tarihi
    "2023-06-15",    # Yangın öncesi (başlangıç)
    "2023-10-15"     # Yangın sonrası (bitiş)
)

print(f"Status: {yangin_sonuc['status']}")
print(f"Koleksiyon Boyutu: {yangin_sonuc['koleksiyon_boyutu']}")

# Orman değişim analizi
degisim_sonuc = pipeline.orman_degisim_pipeline(
    bolge,
    "2023-01-01",
    "2025-12-31"
)
```

---

## 📁 Dosya Yapısı

```
Bati-Karadeniz-Orman-Izleme/
├── src/                      # Yerel modüller
├── notebooks/                # Jupyter Notebooks
├── data/                      # Veri dosyaları
├── assets/                    # Web kaynakları
├── index.html                 # GitHub Pages
├── requirements.txt           # Bağımlılıklar
├── README.md                  # Proje dokümantasyonu
└── QUICKSTART.md             # Bu dosya
```

---

## 🔧 Sorun Giderme

### ❌ "ModuleNotFoundError: No module named 'src'"
```bash
# Sanal ortamın aktif olduğundan emin ol
# Proje kökünde olduğundan emin ol
# Gerekirse yeniden yükle
pip install -e .
```

### ❌ "earthengine-api not installed"
```bash
pip install earthengine-api geemap
earthengine authenticate
```

### ❌ "Jupyter kernel seçeneklerinde Python yok"
```bash
python -m ipykernel install --user --name venv --display-name "Python (Orman İzleme)"
# Sonra jupyter'ı yeniden başlat
```

### ❌ GEE bağlantısı başarısız
```bash
# Credentials sıfırla
rm -rf ~/.config/earthengine/
earthengine authenticate
```

---

## 📚 Sonraki Adımlar

1. **Notebook'u Keşfet:** `notebooks/orman_analizi.ipynb`
2. **Modülleri İnceleme:** `src/` klasöründeki Python dosyaları
3. **Web Sayfasını Aç:** `index.html` (GitHub Pages)
4. **Katkı Yapma:** [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını oku

---

## 🆘 Yardım

- **GitHub Issues:** [Sorun bildir](https://github.com/Ernozkn/Bati-Karadeniz-Orman-Izleme/issues)
- **Dokümantasyon:** [README.md](README.md)
- **İletişim:** ernozkn@gmail.com

---

**Keyifli çalışmalar!** 🌲🚀
