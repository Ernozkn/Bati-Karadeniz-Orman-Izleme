# -*- coding: utf-8 -*-
"""
Veri İşlemleri Modülü
=====================

Orman verilerinin yüklenmesi, işlenmesi ve dönüştürülmesi için fonksiyonlar.
"""

import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json
import os

from .config import (
    ILLER, YILLAR, BASLANGIC_ORMAN_ALANLARI, 
    IL_KOORDINATLARI, NBR_ESIK_DEGERLERI
)


class VeriYoneticisi:
    """Orman verileri yönetim sınıfı"""
    
    def __init__(self, seed: int = 42):
        """
        Veri yöneticisini başlat.
        
        Args:
            seed: Rastgele sayı üreteci tohumu (tekrarlanabilirlik için)
        """
        self.seed = seed
        np.random.seed(seed)
        
        self.iller = ILLER
        self.yillar = YILLAR
        
        # Veri depoları
        self.orman_verileri: Dict = {}
        self.nbr_verileri: Dict = {}
        self.maden_verileri: Dict = {}
        
        # Veri yapılarını başlat
        for il in self.iller:
            self.orman_verileri[il] = {}
            self.nbr_verileri[il] = {}
            
    def veri_ekle(self, il: str, yil: int, veri_tipi: str, veri: Dict) -> None:
        """
        Dışarıdan hesaplanan gerçek veriyi ekle.
        
        Args:
            il: İl adı
            yil: Yıl
            veri_tipi: "orman" veya "nbr"
            veri: Veri sözlüğü
        """
        if veri_tipi == "orman":
            if il not in self.orman_verileri:
                self.orman_verileri[il] = {}
            self.orman_verileri[il][yil] = veri
        elif veri_tipi == "nbr":
            if il not in self.nbr_verileri:
                self.nbr_verileri[il] = {}
            self.nbr_verileri[il][yil] = veri
            
    def maden_verisi_ekle(self, il: str, veri: Dict) -> None:
        """
        Maden verisi ekle.
        
        Args:
            il: İl adı
            veri: Maden veri sözlüğü
        """
        self.maden_verileri[il] = veri

    def _yangin_siddeti_sinifla(self, delta_nbr: float) -> str:
        """
        ΔNBR değerine göre yangın şiddeti sınıflandır.
        
        Args:
            delta_nbr: ΔNBR değeri
            
        Returns:
            str: Yangın şiddeti sınıfı
        """
        if delta_nbr < NBR_ESIK_DEGERLERI["yangin_yok"]:
            return "Yangın Yok"
        elif delta_nbr < NBR_ESIK_DEGERLERI["dusuk_siddet"]:
            return "Düşük Şiddet"
        elif delta_nbr < NBR_ESIK_DEGERLERI["orta_dusuk_siddet"]:
            return "Orta-Düşük Şiddet"
        elif delta_nbr < NBR_ESIK_DEGERLERI["orta_yuksek_siddet"]:
            return "Orta-Yüksek Şiddet"
        else:
            return "Yüksek Şiddet"
    
    def veriyi_dataframe_yap(self, veri_tipi: str = "orman") -> pd.DataFrame:
        """
        Verileri pandas DataFrame formatına dönüştür.
        
        Args:
            veri_tipi: "orman", "nbr" veya "maden"
            
        Returns:
            pd.DataFrame: Tablo formatında veri
        """
        if veri_tipi == "orman":
            rows = []
            for il in self.iller:
                for yil in self.yillar:
                    veri = self.orman_verileri[il][yil]
                    rows.append({
                        "il": il,
                        "yil": yil,
                        **veri
                    })
            return pd.DataFrame(rows)
        
        elif veri_tipi == "nbr":
            rows = []
            for il in self.iller:
                for yil in self.yillar:
                    veri = self.nbr_verileri[il][yil]
                    rows.append({
                        "il": il,
                        "yil": yil,
                        **veri
                    })
            return pd.DataFrame(rows)
        
        elif veri_tipi == "maden":
            rows = []
            for il, veri in self.maden_verileri.items():
                rows.append({
                    "il": il,
                    **{k: v if not isinstance(v, list) else ", ".join(v) for k, v in veri.items()}
                })
            return pd.DataFrame(rows)
        
        else:
            raise ValueError(f"Geçersiz veri tipi: {veri_tipi}")
    
    def veriyi_json_kaydet(self, dosya_yolu: str, veri_tipi: str = "orman") -> None:
        """
        Verileri JSON dosyasına kaydet.
        
        Args:
            dosya_yolu: Kaydedilecek dosya yolu
            veri_tipi: "orman", "nbr" veya "maden"
        """
        veri_haritasi = {
            "orman": self.orman_verileri,
            "nbr": self.nbr_verileri,
            "maden": self.maden_verileri
        }
        
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(veri_haritasi[veri_tipi], f, ensure_ascii=False, indent=2)
    
    def veriyi_json_yukle(self, dosya_yolu: str, veri_tipi: str = "orman") -> Dict:
        """
        JSON dosyasından veri yükle.
        
        Args:
            dosya_yolu: Yüklenecek dosya yolu
            veri_tipi: "orman", "nbr" veya "maden"
            
        Returns:
            Dict: Yüklenen veri
        """
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            veri = json.load(f)
        
        if veri_tipi == "orman":
            # JSON'dan yüklerken yıl anahtarlarını integer yap
            self.orman_verileri = {
                il: {int(yil): deger for yil, deger in yil_verileri.items()}
                for il, yil_verileri in veri.items()
            }
            return self.orman_verileri
        elif veri_tipi == "nbr":
            self.nbr_verileri = {
                il: {int(yil): deger for yil, deger in yil_verileri.items()}
                for il, yil_verileri in veri.items()
            }
            return self.nbr_verileri
        else:
            self.maden_verileri = veri
            return self.maden_verileri
    
    def ozet_istatistikler(self) -> Dict:
        """
        Tüm veriler için özet istatistikler hesapla.
        
        Returns:
            Dict: Özet istatistikler
        """
        ozet = {}
        
        for il in self.iller:
            alanlar = [self.orman_verileri[il][y]["toplam_alan"] for y in self.yillar]
            kayiplar = [
                self.orman_verileri[il][y]["yangin_kaybi"] + 
                self.orman_verileri[il][y]["kesim_kaybi"] + 
                self.orman_verileri[il][y]["maden_kaybi"]
                for y in self.yillar
            ]
            
            ozet[il] = {
                "ortalama_alan": round(np.mean(alanlar), 2),
                "std_alan": round(np.std(alanlar), 2),
                "min_alan": round(np.min(alanlar), 2),
                "max_alan": round(np.max(alanlar), 2),
                "toplam_kayip": round(np.sum(kayiplar), 2),
                "ortalama_yillik_kayip": round(np.mean(kayiplar), 2),
                "degisim_yuzdesi": round(
                    (alanlar[-1] - alanlar[0]) / alanlar[0] * 100, 2
                )
            }
        
        return ozet


def veri_yukle_veya_olustur(veri_klasoru: str = "data") -> VeriYoneticisi:
    """
    Veri dosyaları varsa yükle, yoksa oluştur.
    
    Args:
        veri_klasoru: Veri dosyalarının bulunduğu klasör
        
    Returns:
        VeriYoneticisi: Verilerle doldurulmuş yönetici
    """
    yonetici = VeriYoneticisi()
    
    orman_dosya = os.path.join(veri_klasoru, "orman_verileri.json")
    nbr_dosya = os.path.join(veri_klasoru, "nbr_verileri.json")
    maden_dosya = os.path.join(veri_klasoru, "maden_verileri.json")
    
    if all(os.path.exists(f) for f in [orman_dosya, nbr_dosya, maden_dosya]):
        yonetici.veriyi_json_yukle(orman_dosya, "orman")
        yonetici.veriyi_json_yukle(nbr_dosya, "nbr")
        yonetici.veriyi_json_yukle(maden_dosya, "maden")
    else:
        print("⚠️ Veri dosyaları bulunamadı. GEE üzerinden veri çekilmesi gerekiyor.")
    
    return yonetici
