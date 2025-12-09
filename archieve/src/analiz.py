# -*- coding: utf-8 -*-
"""
Analiz Modülü
=============

Mann-Kendall trend testi, Sen's Slope ve ΔNBR analizleri için fonksiyonlar.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

from .config import ILLER, YILLAR, MANN_KENDALL_ALPHA, NBR_ESIK_DEGERLERI


@dataclass
class MannKendallSonuc:
    """Mann-Kendall test sonuçları"""
    s_istatistik: float
    z_istatistik: float
    p_degeri: float
    sens_slope: float
    trend_yonu: str
    anlamli_mi: bool
    
    def __repr__(self):
        return (
            f"MannKendallSonuc(\n"
            f"  S={self.s_istatistik:.0f}, Z={self.z_istatistik:.4f}, "
            f"p={self.p_degeri:.6f}\n"
            f"  Sen's Slope={self.sens_slope:.2f} ha/yıl\n"
            f"  Trend: {self.trend_yonu}, Anlamlı: {self.anlamli_mi}\n"
            f")"
        )


@dataclass
class NBRAnalizSonuc:
    """ΔNBR analiz sonuçları"""
    nbr_oncesi: float
    nbr_sonrasi: float
    delta_nbr: float
    yangin_siddeti: str
    etkilenen_alan_ha: Optional[float] = None


class OrmanAnalizi:
    """Orman değişim analizi sınıfı"""
    
    def __init__(self, orman_verileri: Dict, nbr_verileri: Dict, maden_verileri: Dict):
        """
        Analiz sınıfını başlat.
        
        Args:
            orman_verileri: İl ve yıl bazında orman verileri
            nbr_verileri: İl ve yıl bazında NBR verileri
            maden_verileri: İl bazında maden verileri
        """
        self.orman_verileri = orman_verileri
        self.nbr_verileri = nbr_verileri
        self.maden_verileri = maden_verileri
        self.iller = ILLER
        self.yillar = YILLAR
        
    def mann_kendall_testi(self, veri_serisi: List[float], alpha: float = MANN_KENDALL_ALPHA) -> MannKendallSonuc:
        """
        Mann-Kendall trend testi uygula.
        
        Args:
            veri_serisi: Zaman serisi verileri
            alpha: Anlamlılık düzeyi
            
        Returns:
            MannKendallSonuc: Test sonuçları
        """
        n = len(veri_serisi)
        
        # S istatistiği hesapla
        s = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                s += np.sign(veri_serisi[j] - veri_serisi[i])
        
        # Varyans hesapla
        var_s = n * (n - 1) * (2 * n + 5) / 18
        
        # Z istatistiği
        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)
        else:
            z = 0
        
        # p-değeri
        if SCIPY_AVAILABLE:
            p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        else:
            # Basit yaklaşım
            p_value = 0.05 if abs(z) < 1.96 else 0.01
        
        # Sen's Slope
        sens_slope = self._sens_slope_hesapla(veri_serisi)
        
        # Trend yönü
        if z > 0:
            trend_yonu = "Artış ↑"
        elif z < 0:
            trend_yonu = "Azalış ↓"
        else:
            trend_yonu = "Değişim Yok"
        
        return MannKendallSonuc(
            s_istatistik=s,
            z_istatistik=z,
            p_degeri=p_value,
            sens_slope=sens_slope,
            trend_yonu=trend_yonu,
            anlamli_mi=p_value < alpha
        )
    
    def _sens_slope_hesapla(self, veri_serisi: List[float]) -> float:
        """
        Sen's Slope tahminini hesapla.
        
        Args:
            veri_serisi: Zaman serisi verileri
            
        Returns:
            float: Medyan eğim değeri
        """
        n = len(veri_serisi)
        slopes = []
        
        for i in range(n - 1):
            for j in range(i + 1, n):
                slope = (veri_serisi[j] - veri_serisi[i]) / (j - i)
                slopes.append(slope)
        
        return np.median(slopes)
    
    def il_trend_analizi(self, il: str) -> MannKendallSonuc:
        """
        Belirli bir il için trend analizi yap.
        
        Args:
            il: İl adı
            
        Returns:
            MannKendallSonuc: Trend analiz sonucu
        """
        alanlar = [self.orman_verileri[il][y]["toplam_alan"] for y in self.yillar]
        return self.mann_kendall_testi(alanlar)
    
    def tum_iller_trend_analizi(self) -> Dict[str, MannKendallSonuc]:
        """
        Tüm iller için trend analizi yap.
        
        Returns:
            Dict: İl bazında trend sonuçları
        """
        sonuclar = {}
        for il in self.iller:
            sonuclar[il] = self.il_trend_analizi(il)
        return sonuclar
    
    def nbr_analizi(self, il: str, yil: int) -> NBRAnalizSonuc:
        """
        Belirli il ve yıl için ΔNBR analizi.
        
        Args:
            il: İl adı
            yil: Yıl
            
        Returns:
            NBRAnalizSonuc: NBR analiz sonucu
        """
        veri = self.nbr_verileri[il][yil]
        
        return NBRAnalizSonuc(
            nbr_oncesi=veri["nbr_oncesi"],
            nbr_sonrasi=veri["nbr_sonrasi"],
            delta_nbr=veri["delta_nbr"],
            yangin_siddeti=veri["yangin_siddeti"]
        )
    
    def bolgesel_nbr_ozeti(self) -> pd.DataFrame:
        """
        Tüm bölge için NBR özet tablosu oluştur.
        
        Returns:
            pd.DataFrame: NBR özet tablosu
        """
        rows = []
        for il in self.iller:
            for yil in self.yillar:
                sonuc = self.nbr_analizi(il, yil)
                rows.append({
                    "İl": il,
                    "Yıl": yil,
                    "NBR Öncesi": sonuc.nbr_oncesi,
                    "NBR Sonrası": sonuc.nbr_sonrasi,
                    "ΔNBR": sonuc.delta_nbr,
                    "Yangın Şiddeti": sonuc.yangin_siddeti
                })
        
        return pd.DataFrame(rows)
    
    def kayip_analizi(self, il: str) -> Dict:
        """
        İl bazında orman kaybı analizi.
        
        Args:
            il: İl adı
            
        Returns:
            Dict: Kayıp analiz sonuçları
        """
        toplam_yangin = sum(self.orman_verileri[il][y]["yangin_kaybi"] for y in self.yillar)
        toplam_kesim = sum(self.orman_verileri[il][y]["kesim_kaybi"] for y in self.yillar)
        toplam_maden = sum(self.orman_verileri[il][y]["maden_kaybi"] for y in self.yillar)
        toplam_artis = sum(self.orman_verileri[il][y]["dogal_artis"] for y in self.yillar)
        
        toplam_kayip = toplam_yangin + toplam_kesim + toplam_maden
        net_degisim = toplam_artis - toplam_kayip
        
        return {
            "yangin_kaybi": round(toplam_yangin, 2),
            "kesim_kaybi": round(toplam_kesim, 2),
            "maden_kaybi": round(toplam_maden, 2),
            "dogal_artis": round(toplam_artis, 2),
            "toplam_kayip": round(toplam_kayip, 2),
            "net_degisim": round(net_degisim, 2),
            "yangin_orani": round(toplam_yangin / toplam_kayip * 100, 1),
            "kesim_orani": round(toplam_kesim / toplam_kayip * 100, 1),
            "maden_orani": round(toplam_maden / toplam_kayip * 100, 1)
        }
    
    def bolgesel_kayip_ozeti(self) -> pd.DataFrame:
        """
        Tüm bölge için kayıp özet tablosu.
        
        Returns:
            pd.DataFrame: Kayıp özet tablosu
        """
        rows = []
        for il in self.iller:
            analiz = self.kayip_analizi(il)
            rows.append({"İl": il, **analiz})
        
        return pd.DataFrame(rows)
    
    def risk_skoru_hesapla(self, il: str) -> Dict:
        """
        İl için orman yangını risk skoru hesapla.
        
        Args:
            il: İl adı
            
        Returns:
            Dict: Risk skoru ve detayları
        """
        # NBR bazlı risk
        nbr_degerleri = [self.nbr_verileri[il][y]["delta_nbr"] for y in self.yillar]
        ortalama_nbr = np.mean(nbr_degerleri)
        
        # Kayıp bazlı risk
        kayip = self.kayip_analizi(il)
        kayip_orani = kayip["toplam_kayip"] / self.orman_verileri[il][2020]["toplam_alan"]
        
        # Maden etkisi
        maden_etkisi = self.maden_verileri[il]["etki_alani_ha"] / 10000  # Normalize
        
        # Bileşik risk skoru (0-1 arası)
        risk_skoru = (
            0.4 * min(ortalama_nbr / 0.66, 1) +  # NBR etkisi
            0.4 * min(kayip_orani * 10, 1) +      # Kayıp etkisi
            0.2 * min(maden_etkisi, 1)             # Maden etkisi
        )
        
        # Risk seviyesi
        if risk_skoru > 0.7:
            risk_seviyesi = "YÜKSEK"
        elif risk_skoru > 0.5:
            risk_seviyesi = "ORTA"
        else:
            risk_seviyesi = "DÜŞÜK"
        
        return {
            "risk_skoru": round(risk_skoru, 3),
            "risk_seviyesi": risk_seviyesi,
            "nbr_faktoru": round(ortalama_nbr, 4),
            "kayip_faktoru": round(kayip_orani, 4),
            "maden_faktoru": round(maden_etkisi, 4)
        }
    
    def tum_iller_risk_analizi(self) -> pd.DataFrame:
        """
        Tüm iller için risk analizi tablosu.
        
        Returns:
            pd.DataFrame: Risk analiz tablosu
        """
        rows = []
        for il in self.iller:
            risk = self.risk_skoru_hesapla(il)
            rows.append({"İl": il, **risk})
        
        return pd.DataFrame(rows)
    
    def yillik_degisim_analizi(self) -> pd.DataFrame:
        """
        Yıllık orman değişim analizi.
        
        Returns:
            pd.DataFrame: Yıllık değişim tablosu
        """
        rows = []
        
        for yil in self.yillar:
            toplam_alan = sum(self.orman_verileri[il][yil]["toplam_alan"] for il in self.iller)
            toplam_yangin = sum(self.orman_verileri[il][yil]["yangin_kaybi"] for il in self.iller)
            toplam_kesim = sum(self.orman_verileri[il][yil]["kesim_kaybi"] for il in self.iller)
            toplam_maden = sum(self.orman_verileri[il][yil]["maden_kaybi"] for il in self.iller)
            toplam_artis = sum(self.orman_verileri[il][yil]["dogal_artis"] for il in self.iller)
            
            rows.append({
                "Yıl": yil,
                "Toplam Alan (ha)": round(toplam_alan, 0),
                "Yangın Kaybı (ha)": round(toplam_yangin, 0),
                "Kesim Kaybı (ha)": round(toplam_kesim, 0),
                "Maden Kaybı (ha)": round(toplam_maden, 0),
                "Doğal Artış (ha)": round(toplam_artis, 0),
                "Net Değişim (ha)": round(toplam_artis - toplam_yangin - toplam_kesim - toplam_maden, 0)
            })
        
        return pd.DataFrame(rows)
    
    def karsilastirmali_analiz(self) -> Dict:
        """
        Bölgesel karşılaştırmalı analiz.
        
        Returns:
            Dict: Karşılaştırma sonuçları
        """
        sonuclar = {
            "en_cok_kayip_il": None,
            "en_az_kayip_il": None,
            "en_yuksek_risk_il": None,
            "bolgesel_toplam_kayip": 0,
            "bolgesel_ortalama_nbr": 0
        }
        
        kayiplar = {}
        riskler = {}
        nbr_toplamlari = []
        
        for il in self.iller:
            kayip = self.kayip_analizi(il)
            kayiplar[il] = kayip["toplam_kayip"]
            sonuclar["bolgesel_toplam_kayip"] += kayip["toplam_kayip"]
            
            risk = self.risk_skoru_hesapla(il)
            riskler[il] = risk["risk_skoru"]
            
            for yil in self.yillar:
                nbr_toplamlari.append(self.nbr_verileri[il][yil]["delta_nbr"])
        
        sonuclar["en_cok_kayip_il"] = max(kayiplar, key=kayiplar.get)
        sonuclar["en_az_kayip_il"] = min(kayiplar, key=kayiplar.get)
        sonuclar["en_yuksek_risk_il"] = max(riskler, key=riskler.get)
        sonuclar["bolgesel_ortalama_nbr"] = round(np.mean(nbr_toplamlari), 4)
        sonuclar["bolgesel_toplam_kayip"] = round(sonuclar["bolgesel_toplam_kayip"], 2)
        
        return sonuclar
