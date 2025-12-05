# -*- coding: utf-8 -*-
"""
Google Earth Engine API Entegrasyonu
=====================================

Sentinel-2 uydu görüntülerinden ΔNBR ve diğer spektral indeksleri
hesaplamak için GEE API kullanımı.
"""

import ee
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import warnings

try:
    import geemap
    GEEMAP_AVAILABLE = True
except ImportError:
    GEEMAP_AVAILABLE = False
    warnings.warn("geemap yüklü değil. Harita gösterilmeyecek.")


class GEEYorumcusu:
    """Google Earth Engine API wrapper sınıfı"""
    
    def __init__(self, credentials_path: Optional[str] = None, project: Optional[str] = None):
        """
        GEE bağlantısını başlat.
        
        Args:
            credentials_path: GEE credentials JSON dosya yolu
            project: Google Cloud projesi adı (opsiyonel)
        """
        self.authenticated = False
        try:
            # Önce mevcut kimlik bilgilerini dene
            if project:
                ee.Initialize(project=project)
            else:
                ee.Initialize()
            self.authenticated = True
            print("✅ Google Earth Engine bağlantısı başarılı (Mevcut kimlik bilgileri)")
            
        except Exception as e:
            print(f"ℹ️ GEE başlatılamadı: {str(e)}")
            print("🚀 Kimlik doğrulama başlatılıyor...")
            
            try:
                if credentials_path:
                    ee.Authenticate(auth_mode='service_account', key_file=credentials_path)
                else:
                    ee.Authenticate()
                
                if project:
                    ee.Initialize(project=project)
                else:
                    ee.Initialize()
                    
                self.authenticated = True
                print("✅ Google Earth Engine bağlantısı ve kimlik doğrulama başarılı")
            except Exception as e2:
                print(f"❌ GEE bağlantı hatası: {str(e2)}")
                print("   ⚠️ Sistem GEE özellikleri olmadan devam edecek.")
                self.authenticated = False
    
    def bolge_sinirlari_olustur(self, komsuluk: Dict[str, float]) -> ee.Geometry:
        """
        Çalışma bölgesini GEE geometrisi olarak oluştur.
        
        Args:
            komsuluk: {"kuzey": lat, "guney": lat, "dogu": lon, "bati": lon}
            
        Returns:
            ee.Geometry: Bölge geometrisi
        """
        if not self.authenticated:
            return None
        
        return ee.Geometry.Rectangle([
            komsuluk["bati"],
            komsuluk["guney"],
            komsuluk["dogu"],
            komsuluk["kuzey"]
        ])
    
    def sentinel2_koleksiyonu_yukle(
        self,
        basla_tarihi: str,
        bitis_tarihi: str,
        bolge: ee.Geometry,
        max_bulut_orani: float = 20.0
    ) -> ee.ImageCollection:
        """
        Sentinel-2 görüntü koleksiyonunu yükle.
        
        Args:
            basla_tarihi: Başlangıç tarihi (YYYY-MM-DD)
            bitis_tarihi: Bitiş tarihi (YYYY-MM-DD)
            bolge: Çalışma bölgesi geometrisi
            max_bulut_orani: Maksimum bulut yüzdesi
            
        Returns:
            ee.ImageCollection: Sentinel-2 görüntü koleksiyonu
        """
        if not self.authenticated:
            return None
        
        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterDate(basla_tarihi, bitis_tarihi)
            .filterBounds(bolge)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_bulut_orani))
            .select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12', 'QA60'])
        )
        
        return collection
    
    def bulut_maskesi_uygula(self, image: ee.Image) -> ee.Image:
        """
        Sentinel-2 QA60 bandını kullanarak bulut maskesi uygula.
        
        Args:
            image: Sentinel-2 görüntüsü
            
        Returns:
            ee.Image: Bulut maskesi uygulanmış görüntü
        """
        if not self.authenticated:
            return None
        
        qa = image.select('QA60')
        
        # QA60 maskeleri
        cirrus_mask = qa.bitwiseAnd(1 << 10).eq(0)
        cloud_mask = qa.bitwiseAnd(1 << 11).eq(0)
        
        return image.updateMask(cirrus_mask).updateMask(cloud_mask)
    
    def nbr_hesapla(self, image: ee.Image) -> ee.Image:
        """
        Normalized Burn Ratio (NBR) indeksini hesapla.
        
        NBR = (B8 - B12) / (B8 + B12)
        B8: NIR (Near Infrared)
        B12: SWIR (Shortwave Infrared)
        
        Args:
            image: Sentinel-2 görüntüsü
            
        Returns:
            ee.Image: NBR indeksi
        """
        if not self.authenticated:
            return None
        
        nir = image.select('B8').divide(10000)
        swir = image.select('B12').divide(10000)
        
        nbr = nir.subtract(swir).divide(nir.add(swir)).rename('NBR')
        
        return nbr
    
    def ndvi_hesapla(self, image: ee.Image) -> ee.Image:
        """
        Normalized Difference Vegetation Index (NDVI) hesapla.
        
        NDVI = (B8 - B4) / (B8 + B4)
        
        Args:
            image: Sentinel-2 görüntüsü
            
        Returns:
            ee.Image: NDVI indeksi
        """
        if not self.authenticated:
            return None
        
        nir = image.select('B8').divide(10000)
        red = image.select('B4').divide(10000)
        
        ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
        
        return ndvi
    
    def ndmi_hesapla(self, image: ee.Image) -> ee.Image:
        """
        Normalized Difference Moisture Index (NDMI) hesapla.
        
        NDMI = (B8A - B11) / (B8A + B11)
        
        Args:
            image: Sentinel-2 görüntüsü
            
        Returns:
            ee.Image: NDMI indeksi
        """
        if not self.authenticated:
            return None
        
        nir = image.select('B8A').divide(10000)
        swir = image.select('B11').divide(10000)
        
        ndmi = nir.subtract(swir).divide(nir.add(swir)).rename('NDMI')
        
        return ndmi
    
    def delta_nbr_hesapla(
        self,
        koleksiyon: ee.ImageCollection,
        yangın_oncesi_tarih: str,
        yangın_sonrasi_tarih: str
    ) -> ee.Image:
        """
        ΔNBR (NBR Farkı) hesapla - yangın öncesi ve sonrasını karşılaştır.
        
        ΔNBR = NBR_öncesi - NBR_sonrası
        
        Args:
            koleksiyon: Sentinel-2 görüntü koleksiyonu
            yangın_oncesi_tarih: Yangın öncesi tarih (YYYY-MM-DD)
            yangın_sonrasi_tarih: Yangın sonrası tarih (YYYY-MM-DD)
            
        Returns:
            ee.Image: ΔNBR fark görüntüsü
        """
        if not self.authenticated:
            return None
        
        # Yangın öncesi ve sonrası görüntüleri al
        oncesi = (
            koleksiyon
            .filterDate(yangın_oncesi_tarih, yangın_sonrasi_tarih)
            .map(self.bulut_maskesi_uygula)
            .map(self.nbr_hesapla)
            .median()
        )
        
        sonrasi = (
            koleksiyon
            .filterDate(yangın_sonrasi_tarih, "2025-12-31")
            .map(self.bulut_maskesi_uygula)
            .map(self.nbr_hesapla)
            .median()
        )
        
        delta_nbr = oncesi.subtract(sonrasi).rename('DELTA_NBR')
        
        return delta_nbr
    
    def spektral_indeksler_hesapla(self, image: ee.Image) -> ee.Image:
        """
        Tüm spektral indeksleri hesapla ve birleştir.
        
        Args:
            image: Sentinel-2 görüntüsü
            
        Returns:
            ee.Image: Tüm indeksleri içeren birleştirilmiş görüntü
        """
        if not self.authenticated:
            return None
        
        # Görüntüyü hazırla
        image = self.bulut_maskesi_uygula(image)
        
        # İndeksleri hesapla
        nbr = self.nbr_hesapla(image)
        ndvi = self.ndvi_hesapla(image)
        ndmi = self.ndmi_hesapla(image)
        
        # Birleştir
        combined = image.addBands(nbr).addBands(ndvi).addBands(ndmi)
        
        return combined
    
    def siniflandirma_yap(self, delta_nbr: ee.Image) -> ee.Image:
        """
        ΔNBR değerlerine göre yangın şiddeti sınıflandırması yap.
        
        Sınıflar:
        0: Yangın Yok (ΔNBR < 0.1)
        1: Düşük Şiddet (0.1 ≤ ΔNBR < 0.27)
        2: Orta-Düşük (0.27 ≤ ΔNBR < 0.44)
        3: Orta-Yüksek (0.44 ≤ ΔNBR < 0.66)
        4: Yüksek Şiddet (ΔNBR ≥ 0.66)
        
        Args:
            delta_nbr: ΔNBR görüntüsü
            
        Returns:
            ee.Image: Sınıflandırılmış görüntü
        """
        if not self.authenticated:
            return None
        
        sinifli = delta_nbr.where(delta_nbr.lt(0.1), 0)
        sinifli = sinifli.where(delta_nbr.gte(0.1).And(delta_nbr.lt(0.27)), 1)
        sinifli = sinifli.where(delta_nbr.gte(0.27).And(delta_nbr.lt(0.44)), 2)
        sinifli = sinifli.where(delta_nbr.gte(0.44).And(delta_nbr.lt(0.66)), 3)
        sinifli = sinifli.where(delta_nbr.gte(0.66), 4)
        
        return sinifli.rename('YANGIN_SINIFI')
    
    def istatistik_hesapla(
        self,
        image: ee.Image,
        bolge: ee.Geometry,
        scale: int = 30
    ) -> Dict:
        """
        Görüntü istatistiklerini hesapla.
        
        Args:
            image: Analiz yapılacak görüntü
            bolge: Çalışma bölgesi
            scale: Piksel ölçeği (metre)
            
        Returns:
            Dict: İstatistikler
        """
        if not self.authenticated:
            return {}
        
        stats_dict = {}
        
        # Bandları al
        bands = image.bandNames().getInfo()
        
        for band in bands:
            try:
                reduced = image.select(band).reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=bolge,
                    scale=scale,
                    maxPixels=1e9
                )
                stats_dict[f"{band}_mean"] = reduced.getInfo()
            except:
                pass
        
        return stats_dict

    def orman_alani_hesapla(self, image: ee.Image, bolge: ee.Geometry, scale: int = 100) -> float:
        """
        NDVI > 0.3 olan pikselleri orman olarak sayıp alan hesabı yapar (hektar).
        
        Args:
            image: Sentinel-2 görüntüsü
            bolge: Analiz bölgesi
            scale: Ölçek (varsayılan 100m - hız için)
            
        Returns:
            float: Orman alanı (hektar)
        """
        if not self.authenticated: return 0.0
        
        try:
            ndvi = image.normalizedDifference(['B8', 'B4'])
            orman_maskesi = ndvi.gt(0.3)
            
            pixel_area = ee.Image.pixelArea()
            orman_alani = pixel_area.updateMask(orman_maskesi).reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=bolge,
                scale=scale,
                maxPixels=1e9
            ).get('area')
            
            # Metrekareden hektara çevir
            return ee.Number(orman_alani).divide(10000).getInfo()
        except Exception as e:
            print(f"Orman alanı hesaplama hatası: {e}")
            return 0.0

    def ortalama_nbr_getir(self, image: ee.Image, bolge: ee.Geometry, scale: int = 100) -> float:
        """
        Bölgedeki ortalama NBR değerini getir.
        """
        if not self.authenticated: return 0.0
        
        try:
            nbr = image.normalizedDifference(['B8', 'B12'])
            mean_nbr = nbr.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=bolge,
                scale=scale,
                maxPixels=1e9
            ).get('nd')
            
            return ee.Number(mean_nbr).getInfo()
        except:
            return 0.0
    
    def goruntu_indir(
        self,
        image: ee.Image,
        bolge: ee.Geometry,
        dosya_adi: str,
        scale: int = 30
    ) -> Dict:
        """
        İşlenmiş görüntüyü indir.
        
        Args:
            image: İndirilecek görüntü
            bolge: Çalışma bölgesi
            dosya_adi: Çıktı dosya adı
            scale: Piksel ölçeği
            
        Returns:
            Dict: İndirme URL ve bilgileri
        """
        if not self.authenticated:
            return {}
        
        try:
            task = ee.batch.Export.image.toDrive(
                image=image,
                description=dosya_adi,
                folder='GEE_Exports',
                scale=scale,
                region=bolge,
                maxPixels=1e9
            )
            task.start()
            
            return {
                "status": "başlatıldı",
                "dosya": dosya_adi,
                "task_id": task.id
            }
        except Exception as e:
            return {"status": "hata", "mesaj": str(e)}
    
    def zaman_serisi_analizi(
        self,
        koleksiyon: ee.ImageCollection,
        bolge: ee.Geometry,
        scale: int = 30
    ) -> pd.DataFrame:
        """
        Zaman serisi analizini gerçekleştir.
        
        Args:
            koleksiyon: Görüntü koleksiyonu
            bolge: Çalışma bölgesi
            scale: Piksel ölçeği
            
        Returns:
            pd.DataFrame: Tarih ve indeks değerleri
        """
        if not self.authenticated:
            return pd.DataFrame()
        
        def add_date_and_stats(image):
            date = image.date().format('YYYY-MM-DD')
            reduced = (
                image.select('NDVI', 'NBR', 'NDMI')
                .reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=bolge,
                    scale=scale,
                    maxPixels=1e9
                )
                .set('date', date)
            )
            return reduced
        
        try:
            time_series = koleksiyon.map(add_date_and_stats).getInfo()
            
            # Pandas DataFrame'e dönüştür
            rows = []
            for feature in time_series['features']:
                rows.append(feature['properties'])
            
            df = pd.DataFrame(rows)
            df['date'] = pd.to_datetime(df['date'])
            
            return df
        except Exception as e:
            print(f"Zaman serisi analiz hatası: {str(e)}")
            return pd.DataFrame()


class Goruntu_Isleme_Pipeline:
    """Sentinel-2 görüntü işleme pipeline'ı"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Pipeline başlat.
        
        Args:
            credentials_path: GEE credentials dosya yolu
        """
        self.gee = GEEYorumcusu(credentials_path)
        self.son_goruntu = None
        self.son_delta_nbr = None
        
    def yangin_analizi_pipeline(
        self,
        komsuluk: Dict[str, float],
        yangin_tarihi: str,
        onc_baslangic: str,
        sonr_bitis: str
    ) -> Dict:
        """
        Yangın analizi için tam pipeline.
        
        Args:
            komsuluk: Çalışma bölgesinin koordinatları
            yangin_tarihi: Yangın tarihi
            onc_baslangic: Yangın öncesi başlangıç
            sonr_bitis: Yangın sonrası bitiş
            
        Returns:
            Dict: Pipeline sonuçları
        """
        if not self.gee.authenticated:
            return {"status": "error", "mesaj": "GEE bağlantısı yok"}
        
        try:
            # Bölge tanımla
            bolge = self.gee.bolge_sinirlari_olustur(komsuluk)
            
            # Sentinel-2 koleksiyonunu yükle
            koleksiyon = self.gee.sentinel2_koleksiyonu_yukle(
                onc_baslangic, sonr_bitis, bolge
            )
            
            # ΔNBR hesapla
            delta_nbr = self.gee.delta_nbr_hesapla(
                koleksiyon, onc_baslangic, yangin_tarihi
            )
            
            # Sınıflandırma yap
            yangin_sinifi = self.gee.siniflandirma_yap(delta_nbr)
            
            # İstatistikler
            istatistikler = self.gee.istatistik_hesapla(delta_nbr, bolge)
            
            self.son_delta_nbr = delta_nbr
            
            return {
                "status": "başarılı",
                "delta_nbr": delta_nbr,
                "yangin_sinifi": yangin_sinifi,
                "istatistikler": istatistikler,
                "koleksiyon_boyutu": koleksiyon.size().getInfo()
            }
            
        except Exception as e:
            return {"status": "error", "mesaj": str(e)}
    
    def orman_degisim_pipeline(
        self,
        komsuluk: Dict[str, float],
        baslangic_tarihi: str,
        bitis_tarihi: str
    ) -> Dict:
        """
        Orman değişim analizi pipeline'ı.
        
        Args:
            komsuluk: Çalışma bölgesi
            baslangic_tarihi: Başlangıç tarihi
            bitis_tarihi: Bitiş tarihi
            
        Returns:
            Dict: Analiz sonuçları
        """
        if not self.gee.authenticated:
            return {"status": "error", "mesaj": "GEE bağlantısı yok"}
        
        try:
            bolge = self.gee.bolge_sinirlari_olustur(komsuluk)
            
            koleksiyon = self.gee.sentinel2_koleksiyonu_yukle(
                baslangic_tarihi, bitis_tarihi, bolge
            )
            
            # Spektral indeksleri hesapla
            spektral = koleksiyon.map(self.gee.spektral_indeksler_hesapla)
            
            # Zaman serisi
            zaman_serisi = self.gee.zaman_serisi_analizi(spektral, bolge)
            
            self.son_goruntu = spektral
            
            return {
                "status": "başarılı",
                "zaman_serisi": zaman_serisi,
                "koleksiyon_boyutu": koleksiyon.size().getInfo()
            }
            
        except Exception as e:
            return {"status": "error", "mesaj": str(e)}
    
    def cok_spektral_analiz_pipeline(
        self,
        komsuluk: Dict[str, float],
        analiz_tarihi: str
    ) -> Dict:
        """
        Çok spektral analiz (NDVI, NDMI, NBR).
        
        Args:
            komsuluk: Çalışma bölgesi
            analiz_tarihi: Analiz tarihi
            
        Returns:
            Dict: Analiz sonuçları
        """
        if not self.gee.authenticated:
            return {"status": "error", "mesaj": "GEE bağlantısı yok"}
        
        try:
            bolge = self.gee.bolge_sinirlari_olustur(komsuluk)
            
            # Belirli tarih çevresinde görüntü al
            baslangic = pd.Timestamp(analiz_tarihi) - timedelta(days=30)
            bitis = pd.Timestamp(analiz_tarihi) + timedelta(days=30)
            
            koleksiyon = self.gee.sentinel2_koleksiyonu_yukle(
                baslangic.strftime('%Y-%m-%d'),
                bitis.strftime('%Y-%m-%d'),
                bolge
            )
            
            # Composite oluştur
            composite = koleksiyon.median()
            spektral_composite = self.gee.spektral_indeksler_hesapla(composite)
            
            # İstatistikler
            istatistikler = self.gee.istatistik_hesapla(spektral_composite, bolge)
            
            return {
                "status": "başarılı",
                "goruntu": spektral_composite,
                "istatistikler": istatistikler,
                "referans_tarihi": analiz_tarihi
            }
            
        except Exception as e:
            return {"status": "error", "mesaj": str(e)}


# Örnek kullanım fonksiyonu
def gee_pipeline_test():
    """GEE Pipeline test fonksiyonu"""
    
    # Pipeline başlat
    pipeline = Goruntu_Isleme_Pipeline()
    
    # Batı Karadeniz bölgesi koordinatları
    bolge = {
        "bati": 31.5,
        "dogu": 33.5,
        "guney": 40.8,
        "kuzey": 42.0
    }
    
    if pipeline.gee.authenticated:
        print("🌍 Orman değişim analizi pipeline'ı başlatılıyor...")
        
        # Örnek analiz (2023-2025)
        sonuc = pipeline.orman_degisim_pipeline(
            bolge,
            "2023-01-01",
            "2025-12-31"
        )
        
        print(f"Pipeline Sonucu: {sonuc['status']}")
        
    else:
        print("⚠️ GEE bağlantısı olmadan demo mode'de çalışıyor...")
        return {
            "status": "demo",
            "mesaj": "GEE credentials kurulumu için lütfen authenticate() çağırın"
        }


if __name__ == "__main__":
    gee_pipeline_test()
