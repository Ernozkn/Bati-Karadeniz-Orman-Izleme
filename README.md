# Batı Karadeniz Orman İzleme Projesi (2020-2025)

Bu proje, Batı Karadeniz Bölgesi'nde (Karabük, Bartın ve Zonguldak) 2020-2025 yılları arasındaki orman alanı değişimlerini incelemeyi ve bu değişimlerin nedenlerini (yangın, kesim, madencilik) uzaktan algılama ve CBS yöntemleriyle ayrıştırmayı amaçlar.

## Proje Kapsamı
*   **Bölge:** Batı Karadeniz (Karabük, Bartın, Zonguldak)
*   **Zaman Aralığı:** 2020 - 2025
*   **Temel Hedefler:**
    1.  Sentinel-2 ile orman kayıplarının tespiti (ΔNBR).
    2.  Kayıp nedenlerinin (Yangın/Kesim/Maden) ayrıştırılması.
    3.  Mann-Kendall ve Sen's Slope ile zaman serisi trend analizi.
    4.  Afet risk haritaları ve karar destek sistemleri geliştirme.

## Kullanılan Teknolojiler
*   **Google Earth Engine (GEE):** Uydu görüntüsü işleme ve zaman serisi analizi.
*   **Python:** Veri analizi ve istatistik (Pandas, Rasterio, Geopandas).
*   **Sentinel-2:** Ana görüntü kaynağı.
*   **Veri Setleri:** CORINE 2023, MTA Ruhsatları (Entegre edilecek), MEŞCERE.

## Dosya Yapısı
*   `analysis.ipynb`: 2025 Yangın Sezonu Detaylı Analizi.
*   `time_series_analysis.ipynb`: (Planlanan) 2020-2025 Trend ve Değişim Analizi.
*   `gee/`: GEE yardımcı modülleri (`aoi.py`, `pipeline.py`).
*   `RESEARCH_PROPOSAL.md`: Detaylı araştırma önerisi ve metodoloji.
