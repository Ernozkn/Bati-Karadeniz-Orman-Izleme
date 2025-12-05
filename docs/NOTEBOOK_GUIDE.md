# 📓 Notebook-Merkezli Analiz Rehberi

## 🎯 Proje Yapısı: Notebook-First Yaklaşım

Bu proje **Jupyter Notebook tabanlı** bir analiz sistemidir. Tüm analiz kodu `notebooks/orman_analizi.ipynb` dosyası üzerinden çalışır. Ayrı CLI komutları veya çalıştırılabilir script'ler **yoktur**.

```
Bati-Karadeniz-Orman-Izleme/
├── 📓 notebooks/
│   └── orman_analizi.ipynb          # ⭐ ANA ANALİZ NOTEBOOK'U (28 hücre)
├── 🐍 src/
│   ├── __init__.py                   # Paket başlatıcısı (tüm importları yönetir)
│   ├── config.py                     # Sabitler: İller, yıllar, renkler, koordinatlar
│   ├── veri_islemleri.py            # VeriYoneticisi sınıfı (veri oluşturma/işleme)
│   ├── analiz.py                     # OrmanAnalizi sınıfı (Mann-Kendall, ΔNBR, risk)
│   ├── gorsellestirme.py            # Gorsellestiric sınıfı (grafikler ve haritalar)
│   └── gee_pipeline.py              # GEEYorumcusu ve Goruntu_Isleme_Pipeline (GEE API)
├── 📁 data/                          # Veri dosyaları (JSON, CSV, vb.)
├── 📁 docs/                          # Dokumentasyon
├── 📁 assets/
│   └── css/style.css                # GitHub Pages CSS
├── 🌐 index.html                     # GitHub Pages ana sayfa
├── 📋 requirements.txt               # Python bağımlılıkları
├── 📦 setup.py                       # Paket kurulumu
├── 📄 README.md                      # Proje açıklaması
├── 📄 QUICKSTART.md                  # Başlama kılavuzu
└── 📄 NOTEBOOK_GUIDE.md              # Bu dosya
```

---

## 🚀 Başlangıç

### 1. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Notebook'u Açın

```bash
jupyter notebook notebooks/orman_analizi.ipynb
```

veya JupyterLab:

```bash
jupyter lab notebooks/orman_analizi.ipynb
```

### 3. Hücreleri Çalıştırın

Notebook'ta **Hücre 1**'den başlayarak **Hücre 28**'e kadar sırasıyla çalıştırın:
- `Cell → Run All` (tüm hücreleri bir kez çalıştır)
- veya her hücreyi ayrı ayrı çalıştır (`Shift+Enter`)

---

## 📓 Notebook Yapısı (28 Hücre)

| # | Tür | İçerik | Açıklama |
|---|-----|--------|----------|
| 1 | 📝 | Başlık | "Batı Karadeniz Orman Analizi" |
| 2 | 🐍 | **Sistem Yolu + İmportlar** | ⚠️ **ÖNCE çalıştırılmalı** |
| 3 | 🐍 | Veri Oluşturma | VeriYoneticisi başlatma |
| 4 | 📝 | Bölüm: Veri Keşfi | Markdown başlık |
| 5-8 | 🐍 | Veri Tabloları | Orman, ΔNBR, Maden verileri |
| 9 | 📝 | Bölüm: Orman Analizi | Markdown başlık |
| 10-14 | 🐍 | Orman Değişim | Grafikler, kayıp analizi |
| 15 | 📝 | Bölüm: ΔNBR Yangın | Markdown başlık |
| 16-18 | 🐍 | Yangın Analizi | ΔNBR grafiği, şiddet dağılımı |
| 19 | 📝 | Bölüm: Mann-Kendall Trend | Markdown başlık |
| 20-21 | 🐍 | Trend Testi | Sonuçlar ve grafikler |
| 22 | 📝 | Bölüm: Risk Analizi | Markdown başlık |
| 23-25 | 🐍 | Risk Hesaplama | Tablosu, harita, karşılaştırma |
| 26 | 📝 | Bölüm: Sonuçlar | Markdown başlık |
| 27 | 🐍 | Sonuç Raporu | Özet bulgular |
| 28 | 📝 | Kaynaklar | Markdown başlık |

---

## 🔧 İmport Mekanizması

### Hücre 2'de (Sistem Yolu Ayarı)

```python
import sys
import os

# Notebook'un bulunduğu dizin
notebook_dir = os.path.dirname(os.path.abspath(__file__))
# Proje kök dizini (notebooks'ün bir üst dizini)
project_root = os.path.dirname(notebook_dir)

# Kök dizini Python path'ine ekle
if project_root not in sys.path:
    sys.path.insert(0, project_root)
```

✅ **Bu sayede `from src import ...` çalışır!**

### Modül İmportları (Hücre 2 - Devam)

```python
# Temel modüller
from src.config import ILLER, YILLAR, RENKLER, IL_KOORDINATLARI
from src.veri_islemleri import VeriYoneticisi
from src.analiz import OrmanAnalizi
from src.gorsellestirme import Gorsellestiric

# GEE modülleri (opsiyonel)
try:
    from src.gee_pipeline import GEEYorumcusu, Goruntu_Isleme_Pipeline
    GEE_AVAILABLE = True
except ImportError:
    GEE_AVAILABLE = False
```

---

## 📦 Modüller ve Sınıflar

### `src/config.py` - Sabitler

```python
ILLER = ['Kastamonu', 'Sinop', 'Zonguldak']
YILLAR = [2020, 2021, 2022, 2023, 2024, 2025]
RENKLER = {'Kastamonu': '#1f77b4', 'Sinop': '#ff7f0e', 'Zonguldak': '#2ca02c'}
IL_KOORDINATLARI = {...}
BASLANGIC_ORMAN_ALANLARI = {...}
```

### `src/veri_islemleri.py` - VeriYoneticisi

```python
# Başlatma
veri = VeriYoneticisi(seed=42)

# Veri oluşturma
orman_v, nbr_v, maden_v = veri.tum_verileri_olustur()

# DataFrame'e dönüştürme
orman_df = veri.veriyi_dataframe_yap("orman")

# Özet istatistikler
ozet = veri.ozet_istatistikler()

# JSON kaydetme/yükleme
veri.veriyi_json_kaydet("orman", "orman_verileri.json")
veri.veriyi_json_yukle("orman_verileri.json")
```

### `src/analiz.py` - OrmanAnalizi

```python
# Başlatma
analiz = OrmanAnalizi(orman_v, nbr_v, maden_v)

# Trend testi
trend = analiz.mann_kendall_testi("Kastamonu")
print(f"Trend: {trend.trend_yonu}, p-değeri: {trend.p_degeri}")

# ΔNBR analizi
nbr_sonuc = analiz.nbr_analizi("Kastamonu")

# Risk skoru
risk = analiz.risk_skoru_hesapla("Kastamonu")

# Tüm iller için
trend_all = analiz.tum_iller_trend_analizi()
risk_all = analiz.tum_iller_risk_analizi()
```

### `src/gorsellestirme.py` - Gorsellestiric

```python
# Başlatma
gorsel = Gorsellestiric(orman_v, nbr_v, maden_v)

# Grafikler
fig = gorsel.orman_alani_grafigi(figsize=(14, 7))
fig = gorsel.nbr_zaman_serisi(figsize=(14, 7))
fig = gorsel.yillik_kayip_bar(figsize=(14, 7))
fig = gorsel.risk_haritasi(risk_verileri, figsize=(12, 10))
fig = gorsel.trend_grafigi(trend_sonuclari, figsize=(16, 5))

plt.show()
```

### `src/gee_pipeline.py` - GEE API (Opsiyonel)

```python
# GEE başlatma (kimlik doğrulama gerekli)
gee = GEEYorumcusu()

# Sentinel-2 koleksiyonu yükle
sentinel2 = gee.sentinel2_koleksiyonu_yukle(
    start_date="2023-01-01",
    end_date="2023-12-31",
    aoi=aoi_polygon
)

# Spektral indeksler hesapla
nbr = gee.nbr_hesapla(sentinel2)
ndvi = gee.ndvi_hesapla(sentinel2)
ndmi = gee.ndmi_hesapla(sentinel2)

# ΔNBR hesapla
delta_nbr = gee.delta_nbr_hesapla(pre_fire, post_fire)

# Sınıflandırma
fire_severity = gee.siniflandirma_yap(delta_nbr)

# Pipeline örneği
pipeline = Goruntu_Isleme_Pipeline()
fire_results = pipeline.yangin_analizi_pipeline(
    aoi=aoi,
    date_range=("2023-06-01", "2023-09-30")
)
```

---

## ⚠️ Önemli Notlar

### 1. Çalışma Dizini
- Notebook **her zaman proje kök dizininde** bulunmalı
- `notebooks/orman_analizi.ipynb` dosyası kendi yolunu doğru algılar

### 2. İmportlar
- **Notebook'un ilk hücresi** (`Cell 2`) `sys.path` ayarlamalı
- Bundan sonra `from src import ...` güvenle kullanılabilir
- GEE modülleri opsiyonel (earthengine-api kurulu değilse atlanır)

### 3. Veri Durumu
- Veri örneğe dayalı (gerçek uydu verisi değil)
- GEE API ile gerçek Sentinel-2 verisi kullanılabilir
- JSON dosyaları `data/` dizinine kaydedilebilir

### 4. Kimlik Doğrulama
- GEE API'sini kullanmak için Google hesabı gerekli
- `gee = GEEYorumcusu()` çalıştırıldığında tarayıcı penceresi açılır
- Kimlik doğrulama başarısız olursa demo modunda çalışır

---

## 📊 Analiz Özeti

### Yapılan Analiz Türleri

1. **Orman Alanı Değişimi** (2020-2025)
   - Yıllık değişim grafiği
   - Kaybın nedenleri (yangın, kesim, madencilik)

2. **ΔNBR Yangın Şiddeti**
   - 5 sınıf: Yangın Yok, Düşük, Orta-Düşük, Orta-Yüksek, Yüksek
   - Zaman serisi analizi

3. **Mann-Kendall Trend Testi**
   - İstatistiksel anlamlılık (p < 0.05)
   - Sen's Slope (eğim tahmini: ha/yıl)

4. **Risk Skoru Hesaplama**
   - Bileşim: %40 ΔNBR + %40 Kayıp Oranı + %20 Madencilik
   - 0-100 aralığında normalized skor

5. **Karşılaştırmalı Analiz**
   - En çok kayıp yaşayan il
   - En az kayıp yaşayan il
   - En yüksek riskli il

---

## 🔗 İlişkili Belgeler

- [`README.md`](README.md) - Proje genel açıklaması
- [`QUICKSTART.md`](QUICKSTART.md) - Hızlı başlama kılavuzu
- [`requirements.txt`](requirements.txt) - Python paketleri
- [`setup.py`](setup.py) - Paket kurulum yapısı

---

## 📧 İletişim

**Proje:** Batı Karadeniz Orman İzleme Sistemi
**Kurum:** Karabük Üniversitesi - Yapay Zeka Operatörlüğü
**Lisans:** MIT

---

**Son Güncelleme:** 2025
**Notebook Versiyonu:** 1.0 (28 hücre, tamamen fonksiyonel)
