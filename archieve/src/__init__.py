# -*- coding: utf-8 -*-
"""
Batı Karadeniz Orman İzleme - Python Modülleri
==============================================

Bu paket, Batı Karadeniz Bölgesi orman değişim analizi için
gerekli tüm Python modüllerini içerir.

Modüller:
    - config: Proje yapılandırma sabitleri
    - veri_islemleri: Veri yönetimi (VeriYoneticisi sınıfı)
    - analiz: İstatistiksel analizler (OrmanAnalizi sınıfı)
    - gorsellestirme: Grafik ve harita (Gorsellestiric sınıfı)
    - gee_pipeline: Google Earth Engine API (GEEYorumcusu, Goruntu_Isleme_Pipeline)

Kullanım Örneği:
    >>> from src import VeriYoneticisi, OrmanAnalizi, Gorsellestiric
    >>> from src.gee_pipeline import GEEYorumcusu, Goruntu_Isleme_Pipeline
    
    >>> # Veri yöneticisi başlat
    >>> veri = VeriYoneticisi()
    >>> orman_v, nbr_v, maden_v = veri.tum_verileri_olustur()
    
    >>> # Analiz yap
    >>> analiz = OrmanAnalizi(orman_v, nbr_v, maden_v)
    >>> trend = analiz.tum_iller_trend_analizi()
    
    >>> # Görselleştir
    >>> gorsel = Gorsellestiric(orman_v, nbr_v, maden_v)
    >>> fig = gorsel.orman_alani_grafigi()
    
    >>> # GEE API kullan
    >>> gee = GEEYorumcusu()
    >>> pipeline = Goruntu_Isleme_Pipeline()
"""

__version__ = "1.0.0"
__author__ = "Karabük Üniversitesi - Yapay Zeka Operatörlüğü"
__license__ = "MIT"

try:
    from .config import (
        ILLER, YILLAR, IL_KOORDINATLARI,
        RENKLER
    )
    from .veri_islemleri import VeriYoneticisi, veri_yukle_veya_olustur
    from .analiz import OrmanAnalizi, MannKendallSonuc, NBRAnalizSonuc
    from .gorsellestirme import Gorsellestiric
    from .gee_pipeline import GEEYorumcusu, Goruntu_Isleme_Pipeline
    
    __all__ = [
        'ILLER', 'YILLAR', 'IL_KOORDINATLARI', 'RENKLER',
        'VeriYoneticisi', 'veri_yukle_veya_olustur',
        'OrmanAnalizi', 'MannKendallSonuc', 'NBRAnalizSonuc',
        'Gorsellestiric',
        'GEEYorumcusu', 'Goruntu_Isleme_Pipeline'
    ]
except ImportError as e:
    print(f"⚠️ Import hatası: {e}")
    print("Bazı modüller yüklenemedi. Lütfen gerekli bağımlılıkları kontrol edin.")
    __all__ = []
