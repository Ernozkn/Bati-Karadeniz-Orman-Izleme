# 🌲 Batı Karadeniz Bölgesi Orman Değişim Analizi ve Afet Yönetimi (2020-2025)

Batı Karadeniz'de (2020-2025) orman değişimlerinin **Google Earth Engine API**, **Sentinel-2 uydu görüntüleri**, **ΔNBR indeksi** ve **istatistiksel analizler** ile incelenmesi.

## 🚀 Hızlı Başlama

```bash
# 1. Gerekli paketleri yükle
pip install -r requirements.txt

# 2. Jupyter'ı başlat
jupyter lab notebooks/orman_analizi.ipynb

# 3. Notebook'taki hücreleri sırasıyla çalıştır (Shift+Enter)
```

⭐ **Tüm analiz `notebooks/orman_analizi.ipynb` dosyasında yapılır. CLI komutları yoktur.**

## 🔗 Web Sayfası
**🌐 [Canlı Demo - GitHub Pages](https://ernozkn.github.io/Bati-Karadeniz-Orman-Izleme/)**

---

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![GEE API](https://img.shields.io/badge/Google%20Earth%20Engine-API-green?logo=google)
![Sentinel-2](https://img.shields.io/badge/Sentinel--2-Uydu%20Verisi-brightgreen)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📖 Proje Hakkında

Bu çalışma, **Karabük Üniversitesi Yapay Zeka Operatörlüğü Bölümü** bitirme projesi olarak hazırlanmıştır.

Batı Karadeniz Bölgesi'nde (Karabük, Bartın, Zonguldak) 2020-2025 yılları arasında meydana gelen orman alanı değişimlerini **Google Earth Engine API** üzerinden Sentinel-2 uydu görüntüleriyle inceleyerek, orman kayıplarını **yangın, kesim ve madencilik** faaliyetlerine göre sınıflandırıyor. Afet yönetimi perspektifinden değerlendirilen bu çalışma, karar destek mekanizmalarına katkı sağlamayı hedefliyor.

---

## 📍 Çalışma Alanı

| Özellik | Detay |
|---------|-------|
| **Bölge** | Karabük, Bartın, Zonguldak İlleri |
| **Koordinatlar** | 31.5°E - 33.5°E, 40.8°N - 42.0°N |
| **Zaman Aralığı** | 2020 - 2025 |
| **Veri Kaynağı** | Sentinel-2 Level-2A (Google Earth Engine) |

---

## 🎯 Proje Hedefleri

1. **🛰️ Uydu Görüntü İşleme**
   - Sentinel-2 görüntüleri üzerinde QA60 bulut maskesi uygulaması
   - ΔNBR (Normalized Burn Ratio Difference) indeksi ile orman yangını analizi
   - NDVI, NDMI gibi spektral indekslerin hesaplanması

2. **📊 Etki Ayrıştırma**
   - Orman kaybı nedenlerinin sınıflandırması (Yangın/Kesim/Maden)
   - Mekansal analiz ile risk haritaları oluşturma
   - Madencilik alanlarının orman kayıplarına etkisi değerlendirmesi

3. **📈 Trend Analizi**
   - Mann-Kendall testi ile zaman serisi trendlerinin belirlenmesi
   - Sen's Slope yöntemiyle eğim tahminleri
   - İstatistiksel anlamlılık testleri

4. **🗺️ Afet Yönetimi Önerileri**
   - Risk skoru hesaplaması ve haritalaması
   - Erken uyarı sistemleri için metodoloji önerisi
   - Rehabilitasyon ve ağaçlandırma stratejileri

---

## 🛠️ Teknoloji Stack

### Python Kütüphaneleri
| Kategori | Araçlar |
|----------|---------|
| **Veri İşleme** | NumPy, Pandas, SciPy |
| **Uydu Verisi** | earthengine-api, geemap, rasterio, geopandas |
| **İstatistik** | scipy.stats, scikit-learn, statsmodels |
| **Görselleştirme** | Matplotlib, Plotly, Seaborn |
| **CBS Analiz** | GeoPandas, Shapely, Folium |
| **Notebook** | Jupyter, JupyterLab, IPyWidgets |

### Harici Kaynaklar
- **Google Earth Engine API** - Sentinel-2 uydu görüntüleri
- **CORINE 2023** - Arazi örtüsü sınıflandırması
- **MTA** - Madencilik Ruhsat Verileri
- **MEŞCERE** - Orman Envanteri Verileri

---

## 📂 Proje Yapısı

```
Bati-Karadeniz-Orman-Izleme/
├── 📁 src/                           # Yerel Python modülleri
│   ├── __init__.py
│   ├── config.py                     # Yapılandırma sabitleri
│   ├── veri_islemleri.py             # Veri yönetimi (VeriYoneticisi)
│   ├── analiz.py                     # İstatistiksel analiz (OrmanAnalizi)
│   ├── gorsellestirme.py             # Grafik ve harita (Gorsellestiric)
│   └── gee_pipeline.py               # Google Earth Engine API (GEEYorumcusu)
│
├── 📁 notebooks/                     # Jupyter Notebooks
│   └── orman_analizi.ipynb           # Ana analiz notebook
│
├── 📁 data/                          # Veri dosyaları
│   ├── orman_verileri.json
│   ├── nbr_verileri.json
│   └── maden_verileri.json
│
├── 📁 assets/                        # Web sayfası kaynakları
│   ├── css/
│   │   └── style.css                 # Stil sayfası
│   └── images/                       # Resimler ve ikonlar
│
├── 📁 docs/                          # Proje dokümantasyonu
│   ├── proje_raporu.md
│   └── teknik_dokumantasyon.md
│
├── index.html                        # Ana web sayfası (GitHub Pages)
├── requirements.txt                  # Python bağımlılıkları
├── README.md                         # Bu dosya
└── LICENSE                           # MIT Lisansı
```

---

## 🚀 Hızlı Başlangıç

### 1. Depoyu Klonla
```bash
git clone https://github.com/Ernozkn/Bati-Karadeniz-Orman-Izleme.git
cd Bati-Karadeniz-Orman-Izleme
```

### 2. Sanal Ortam Oluştur
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 4. Google Earth Engine Kurulumu (Opsiyonel)
```bash
earthengine authenticate
```

### 5. Jupyter Notebook'u Başlat
```bash
jupyter notebook notebooks/orman_analizi.ipynb
```

---

## 📊 Kullanılan Yöntemler

### ΔNBR (Yangın Şiddeti İndeksi)
$$\text{ΔNBR} = \text{NBR}_{\text{öncesi}} - \text{NBR}_{\text{sonrası}}$$
$$\text{NBR} = \frac{\text{B8} - \text{B12}}{\text{B8} + \text{B12}}$$

**Sınıflandırma:**
- ΔNBR < 0.1: Yangın Yok
- 0.1 ≤ ΔNBR < 0.27: Düşük Şiddet
- 0.27 ≤ ΔNBR < 0.44: Orta-Düşük Şiddet
- 0.44 ≤ ΔNBR < 0.66: Orta-Yüksek Şiddet
- ΔNBR ≥ 0.66: Yüksek Şiddet

### Mann-Kendall Trend Testi
Zaman serisinde monoton trend varlığını test eder.
- **H₀:** Trend yok
- **H₁:** Trend var (artan/azalan)
- **p-değeri < 0.05:** İstatistiksel olarak anlamlı

### Sen's Slope Tahmini
$$\text{Slope}_{\text{Sen}} = \text{median}\left(\frac{y_j - y_i}{j - i}\right) \quad (i < j)$$
**Birim:** ha/yıl

### NDVI (Bitki Örtüsü Endeksi)
$$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}} = \frac{\text{B8} - \text{B4}}{\text{B8} + \text{B4}}$$

### NDMI (Nem İndeksi)
$$\text{NDMI} = \frac{\text{B8A} - \text{B11}}{\text{B8A} + \text{B11}}$$

---

## 📝 Modül Açıklaması

### `src/config.py`
Proje genelinde kullanılan sabit değerler, bölge koordinatları ve renk şeması.

### `src/veri_islemleri.py`
**VeriYoneticisi sınıfı** ile örnek veri oluşturma, yükleme, dönüştürme ve JSON'da saklama.

### `src/analiz.py`
**OrmanAnalizi sınıfı** ile:
- Mann-Kendall trend testi
- Sen's Slope hesaplaması
- ΔNBR analizi
- Risk skoru hesaplama
- Karşılaştırmalı analizler

### `src/gorsellestirme.py`
**Gorsellestiric sınıfı** ile:
- Orman alanı grafikleri
- Kayıp dağılımı pasta grafikleri
- Risk haritaları
- Trend grafikleri
- Plotly interaktif görseller

### `src/gee_pipeline.py`
**Google Earth Engine API entegrasyonu:**
- **GEEYorumcusu**: GEE API bağlantısı ve spektral indeks hesaplaması
- **Goruntu_Isleme_Pipeline**: Yangın, orman değişimi ve çok spektral analiz pipeline'ları

---

## 🔗 Google Earth Engine API Kullanımı

### Bağlantı Kurma
```python
from src.gee_pipeline import GEEYorumcusu

gee = GEEYorumcusu()
gee.bulut_maskesi_uygula(image)
```

### Pipeline Çalıştırma
```python
from src.gee_pipeline import Goruntu_Isleme_Pipeline

pipeline = Goruntu_Isleme_Pipeline()
bolge = {"bati": 31.5, "dogu": 33.5, "guney": 40.8, "kuzey": 42.0}

sonuc = pipeline.yangin_analizi_pipeline(
    bolge,
    "2023-08-15",  # Yangın tarihi
    "2023-06-15",  # Yangın öncesi
    "2023-10-15"   # Yangın sonrası
)
```

---

## 📊 Örnek Çıktılar

### Orman Alanı Değişimi Grafiği
```
Karabük:   245,000 ha (2020) → 235,200 ha (2025)
Bartın:    178,000 ha (2020) → 171,500 ha (2025)
Zonguldak: 312,000 ha (2020) → 300,100 ha (2025)
```

### Kayıp Dağılımı
- 🔥 Yangın: %38.0
- 🪓 Kesim: %31.3
- ⛏️ Madencilik: %30.5

### Risk Skoru
| İl | Risk Skoru | Seviye |
|----|-----------|--------|
| Karabük | 0.45 | Orta Risk |
| Bartın | 0.35 | Düşük Risk |
| Zonguldak | 0.72 | Yüksek Risk |

---

## 💡 Afet Yönetimi Önerileri

### 🎯 Senaryo 1: Yangın Risk Azaltma
- Yüksek ΔNBR değerli alanlarda erken uyarı sistemleri
- Yangın kırma bantları oluşturma
- Hava takip istasyonlarını artırma

### 🎯 Senaryo 2: Maden Etkisi Kontrolü
- Maden ruhsat alanlarında tampon bölgeler
- Zorunlu rehabilitasyon programları
- Ağaçlandırma projeleri

### 🎯 Senaryo 3: Entegre Yönetim
- CBS tabanlı sürekli izleme
- Mevsimsel risk haritası güncellemeleri
- Yerel yönetimlerle koordinasyon

---

## 📚 Kaynaklar

- [Google Earth Engine](https://earthengine.google.com/)
- [Sentinel-2 Dokümantasyonu](https://sentinel.esa.int/web/sentinel/missions/sentinel-2)
- [geemap - Interactive GEE Maps](https://github.com/giswqs/geemap)
- [Rasterio - GIS Raster Processing](https://rasterio.readthedocs.io/)
- [GeoPandas - GIS Vector Processing](https://geopandas.org/)

---

## 👨‍💻 Katkıda Bulunma

Bu proje açık kaynaktır. İyileştirmeler ve hata raporlaması için lütfen:
1. Fork'layın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişiklikleri commit'leyin (`git commit -m 'Add AmazingFeature'`)
4. Branch'i push'layın (`git push origin feature/AmazingFeature`)
5. Pull Request açın

---

## 📄 Lisans

Bu proje **MIT Lisansı** altında yayınlanmıştır. Detaylar için bkz: [LICENSE](LICENSE)

---

## 📧 İletişim

**Proje Lideri:** Ernozkn  
**E-posta:** ernozkn@gmail.com  
**GitHub:** [@Ernozkn](https://github.com/Ernozkn)  
**Kurum:** Karabük Üniversitesi - Yapay Zeka Operatörlüğü Bölümü

---

## 🙏 Teşekkürler

- **ESA** - Sentinel-2 uydu programı
- **Google** - Earth Engine API
- **Karabük Üniversitesi** - Akademik danışmanlık
- **Tüm katkıda bulunanlar**

---

**Son Güncelleme:** Aralık 2025  
**Versiyon:** 1.0.0
