# Batı Karadeniz Bölgesi Orman Değişim Analizi ve Afet Yönetimi (2020-2025)

Batı Karadeniz'de (2020-2025) orman değişimlerinin Sentinel-2, ΔNBR ve CBS teknikleriyle analizi ve afet yönetimi simülasyonu.


![Python](https://img.shields.io/badge/Dil-Python-blue)
![Sentinel-2](https://img.shields.io/badge/Veri-Sentinel--2-green)
![Lisans](https://img.shields.io/badge/Lisans-MIT-lightgrey)

## 📖 Proje Hakkında
Bu çalışma, **Karabük Üniversitesi Yapay Zeka Operatörlüğü Bölümü** bitirme projesi olarak hazırlanmıştır.

Araştırmanın temel amacı; **Batı Karadeniz Bölgesi'nde (Karabük, Bartın ve Zonguldak)** 2020-2025 yılları arasında meydana gelen orman alanı değişimlerini uzaktan algılama teknikleri ile incelemektir. Proje, orman kayıplarını **yangın, kesim ve madencilik** faaliyetleri olarak sınıflandırarak afet yönetimi perspektifinden ayrıştırmayı ve karar destek mekanizmalarına katkı sağlamayı hedefler.

## 📍 Çalışma Alanı ve Kapsam
* **Bölge:** Batı Karadeniz (Karabük, Bartın, Zonguldak illeri).
* **Zaman Aralığı:** 2020 - 2025.
* **Odak:** Yangın sonrası kayıplar, madencilik faaliyetleri ve orman kesimleri.

## 🎯 Proje Hedefleri
Bu proje dört ana hedef doğrultusunda ilerlemektedir:

1.  **Uydu Görüntü İşleme:** Sentinel-2 (Level-2A) görüntüleri üzerinde bulut maskesi (QA60) ve **ΔNBR (Normalized Burn Ratio Difference)** indeksi kullanılarak orman kayıplarının %90 doğrulukla tespiti.
2.  **Etki Ayrıştırma:** CORINE 2023, MEŞCERE ve MTA Maden Ruhsat verileri entegre edilerek orman değişim nedenlerinin (Yangın/Kesim/Maden) oransal olarak belirlenmesi.
3.  **Trend Analizi:** Mann-Kendall testi ve Sen’s slope yöntemi ile zaman serisi analizleri yapılarak değişim eğilimlerinin afet risk haritalarına dönüştürülmesi.
4.  **Doğrulama ve Raporlama:** Sonuçların Google Earth üzerinden görsel doğrulaması ve bölgesel afet yönetimi için stratejik önerilerin sunulması.

## 🛠️ Kullanılan Yöntem ve Teknolojiler
Projede **Nicel Araştırma Yöntemi** kullanılmış olup, aşağıdaki teknolojilerden yararlanılmıştır:

| Kategori | Araçlar / Kütüphaneler |
| :--- | :--- |
| **Programlama** | Python 3.x (Pandas, NumPy) |
| **Coğrafi Analiz** | Rasterio, Geopandas, QGIS |
| **Uydu Verisi** | Google Earth Engine (GEE), Sentinel-2 L2A |
| **İstatistik** | Mann-Kendall Testi, SciPy |

## 📂 Proje Yapısı
```text
├── veri/               # Ham ve işlenmiş coğrafi veriler
├── kodlar/             # Python analiz kodları ve GEE scriptleri
├── haritalar/          # Üretilen risk ve analiz haritaları (Çıktılar)
├── dokumanlar/         # Proje raporu ve literatür taraması notları
└── README.md           # Proje tanıtım dosyası
