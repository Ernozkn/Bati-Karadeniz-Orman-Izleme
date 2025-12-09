# Araştırma: Batı Karadeniz Bölgesi Orman Alanı Değişim Analizi (2020-2025)

## Genel Amaç
Batı Karadeniz Bölgesi'nde (Karabük, Bartın ve Zonguldak illeri) 2020-2025 yılları arasında meydana gelen orman alanı değişimlerini uzaktan algılama teknikleriyle inceleyerek, bu değişimlerin yangın, kesim ve madencilik faaliyetlerinden kaynaklanan etkilerini afet yönetimi perspektifinden ayrıştırmak ve bölgesel karar destek mekanizmalarına katkı sağlamaktır.

## Hedefler

### Hedef 1: Mevsimsel Mozaik ve Yangın Tespiti
*   **Veri:** Sentinel-2 Level-2A.
*   **Yöntem:** Bulut maskesi (QA60), Mevsimsel mozaikleme.
*   **İndeks:** ΔNBR (Normalized Burn Ratio Difference).
*   **Kriter:** %90 doğruluk oranı.

### Hedef 2: Etki Ayrıştırması (Yangın / Kesim / Maden)
*   **Veri:** CORINE 2023, MEŞCERE haritaları, MTA maden ruhsat verileri.
*   **Yöntem:** CBS entegrasyonu, Raster katman analizleri.
*   **Çıktı:** Her faktörün orman kaybına katkı oranları (%).

### Hedef 3: Zaman Serisi ve Trend Analizi
*   **Yöntem:** Mann-Kendall testi, Sen’s slope.
*   **Çıktı:** Orman değişim eğilimleri, Afet riski haritaları, Karar destek senaryoları.

### Hedef 4: Doğrulama ve Raporlama
*   **Yöntem:** Google Earth görsel doğrulama.
*   **Çıktı:** %20 iyileştirilmiş orman yangını riski modelleri önerisi.

## Metodoloji
*   **Kapsam:** Batı Karadeniz (Karabük, Bartın, Zonguldak).
*   **Dönem:** 2020-2025.
*   **Platform:** Google Earth Engine (GEE), QGIS, Python (rasterio, geopandas).
*   **İstatistik:** Mann-Kendall, Sen's Slope, Regresyon, Moran's I.

## Zaman Çizelgesi
1.  **Ay 1:** Veri toplama ve ön işleme (Sentinel-2).
2.  **Ay 2:** CBS entegrasyonu ve ΔNBR.
3.  **Ay 3.5:** Zaman serisi analizleri (Mann-Kendall).
4.  **Ay 5.5:** Doğrulama, raporlama ve risk haritaları.
