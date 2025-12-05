# -*- coding: utf-8 -*-
"""
Proje Yapılandırma Sabitleri
============================

Batı Karadeniz Orman İzleme projesi için sabit değerler ve yapılandırmalar.
"""

# Proje Bilgileri
PROJE_ADI = "Batı Karadeniz Bölgesi Orman Değişim Analizi"
PROJE_VERSIYON = "1.0.0"

# Bölge Bilgileri
ILLER = ["Karabük", "Bartın", "Zonguldak"]
YILLAR = list(range(2020, 2026))

# İl Koordinatları (Merkez Noktaları - WGS84)
IL_KOORDINATLARI = {
    "Karabük": {"lat": 41.2, "lon": 32.6},
    "Bartın": {"lat": 41.6, "lon": 32.3},
    "Zonguldak": {"lat": 41.4, "lon": 31.8}
}

# Başlangıç Orman Alanları (Hektar)
BASLANGIC_ORMAN_ALANLARI = {
    "Karabük": 245000,
    "Bartın": 178000,
    "Zonguldak": 312000
}

# ΔNBR Yangın Şiddeti Sınıflandırması
NBR_ESIK_DEGERLERI = {
    "yangin_yok": 0.1,
    "dusuk_siddet": 0.27,
    "orta_dusuk_siddet": 0.44,
    "orta_yuksek_siddet": 0.66
}

NBR_SINIFLANDIRMA = {
    (float('-inf'), 0.1): "Yangın Yok",
    (0.1, 0.27): "Düşük Şiddet",
    (0.27, 0.44): "Orta-Düşük Şiddet",
    (0.44, 0.66): "Orta-Yüksek Şiddet",
    (0.66, float('inf')): "Yüksek Şiddet"
}

# Renk Şeması
RENKLER = {
    "arkaplan": "#1a1a2e",
    "panel": "#16213e",
    "vurgu": "#0f3460",
    "yesil": "#2ecc71",
    "kirmizi": "#e74c3c",
    "sari": "#f39c12",
    "mavi": "#3498db",
    "beyaz": "#ecf0f1",
    "turuncu": "#e67e22"
}

# Grafik Ayarları
GRAFIK_AYARLARI = {
    "figsize": (12, 6),
    "dpi": 100,
    "style": "seaborn-v0_8-darkgrid"
}

# Mann-Kendall Test Ayarları
MANN_KENDALL_ALPHA = 0.05

# Dosya Yolları
VERI_KLASORU = "data"
CIKTI_KLASORU = "outputs"
HARITA_KLASORU = "maps"
