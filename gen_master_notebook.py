
import json
import os

nb_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Batı Karadeniz Orman İzleme ve Afet Yönetimi Projesi (2020-2025)\n",
    "\n",
    "**Proje Başlığı:** Batı Karadeniz Bölgesi’nde Orman Alanı Değişimlerinin Yangın, Kesim ve Madencilik Kaynaklı Etkilerinin Uzaktan Algılama ve CBS ile Ayrıştırılması\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. ÖZET\n",
    "\n",
    "Bu araştırma, Batı Karadeniz Bölgesi’nde (Karabük, Bartın, Zonguldak) 2020-2025 yılları arasında meydana gelen orman alanı değişimlerinin, yangın, kesim ve madencilik faaliyetlerinden kaynaklanan etkilerini uzaktan algılama ve Coğrafi Bilgi Sistemleri (CBS) kullanarak incelemeyi amaçlamaktadır. Bölge, orman varlığı bakımından Türkiye’nin en yüksek orman örtüsüne sahip alanlarından biri olmakla birlikte, son yıllarda artan iklim değişikliği, yangın ve insan kaynaklı tahribatlar nedeniyle ekosistem üzerinde büyük değişiklikler yaşanmaktadır. Bu araştırma, mevcut literatürde sınırlı olan bölgesel afet ve orman değişim analizlerine katkı sağlamayı hedeflemektedir.\n",
    "\n",
    "Araştırmanın temel yöntemi, ΔNBR (Normalized Burn Ratio Difference) ile orman değişimlerinin tespitidir. Sentinel-2 L2A uydu görüntüleri kullanılarak, ΔNBR hesaplamaları yapılacak ve orman kayıplarının mekânsal dağılımı belirlenecektir. ΔNBR, yangın sonrası orman alanındaki değişimleri izlemek için yaygın bir yöntem olup, bu çalışmada ayrıca kesim ve maden kaynaklı değişimlerin etkileri de analiz edilecektir. CORINE 2023 arazi kullanım verileri, MEŞCERE haritaları ve MTA maden ruhsat poligonları ile entegrasyon sağlanarak, orman alanındaki değişimlerin sürücüsü olan faktörler ayrıştırılacaktır. Bu süreç, afet yönetimi ve ekosistem izleme için önemli bir veri seti sağlayacaktır.\n",
    "\n",
    "Veri işleme süreci, Google Earth Engine ve QGIS yazılımları kullanılarak yapılacak, verilerin doğruluğu Google Earth görselleriyle doğrulanacaktır. Mann-Kendall ve Sen’s slope gibi istatistiksel testlerle, orman değişimlerinin yıllık eğilimleri ve afet riski zonları belirlenecektir. Bu sayede, Batı Karadeniz Bölgesi’nde orman yangını ve maden kaynaklı tahribatlar gibi afet etkilerinin izlenmesi mümkün olacaktır. Elde edilen bulgular, bölgesel afet yönetimi, orman yangını riski ve madencilik faaliyetlerinin çevresel etkileri konularında karar destek sistemleri geliştirilmesine katkı sağlayacaktır.\n",
    "\n",
    "Sonuç olarak, bu çalışma, Batı Karadeniz’deki orman değişimlerinin mekânsal analizi ile afet yönetimine yönelik somut veri sağlamayı amaçlamakta ve afet riski haritalaması konusunda özgün bir yaklaşım geliştirmektedir. Çalışmadan elde edilecek veriler, orman ekosistemlerinin sürdürülebilir yönetimi ve afet yönetiminde önemli bir kaynak olacaktır.\n",
    "\n",
    "**Anahtar Kelimeler:** ΔNBR, Afet Yönetimi, Orman Yangınları, Uzaktan Algılama, Batı Karadeniz"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. AMAÇ VE HEDEF\n",
    "\n",
    "Bu araştırmanın genel amacı, Batı Karadeniz Bölgesi'nde (Karabük, Bartın ve Zonguldak illeri) 2020-2025 yılları arasında meydana gelen orman alanı değişimlerini uzaktan algılama teknikleriyle inceleyerek, bu değişimlerin yangın, kesim ve madencilik faaliyetlerinden kaynaklanan etkilerini afet yönetimi perspektifinden ayrıştırmak ve bölgesel karar destek mekanizmalarına katkı sağlamaktır.\n",
    "\n",
    "Bu amaç doğrultusunda belirlenen hedefler şu şekildedir:\n",
    "1.  **Hedef 1 (Veri İşleme):** Sentinel-2 Level-2A uydu görüntülerini kullanarak, 2020-2025 dönemi için bulut maskesi (QA60) uygulanmış mevsimsel mozaik verileri oluşturmak ve bu veriler üzerinde ΔNBR indeksini hesaplayarak, yangın sonrası orman kayıplarını tespit etmek.\n",
    "2.  **Hedef 2 (Ayrıştırma):** CORINE arazi kullanımı verileri, MEŞCERE haritaları ve MTA maden ruhsat verilerini CBS üzerinden entegre ederek, orman değişimlerinin yangın, kesim ve maden etkilerini ayrıştırmak.\n",
    "3.  **Hedef 3 (Trend Analizi):** Zaman serisi analizleri için Mann-Kendall testi ve Sen’s slope yöntemini uygulayarak, orman değişim eğilimlerini belirlemek ve bu eğilimleri afet riski haritalarına dönüştürmek.\n",
    "4.  **Hedef 4 (Doğrulama ve Raporlama):** Tüm sonuçları görsel doğrulama ile valide etmek ve bölgesel afet yönetimi için senaryolar üretmek."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. YÖNTEM\n",
    "\n",
    "### 3.1. Çalışma Alanı ve Veri Kaynakları\n",
    "*   **Bölge:** Batı Karadeniz (Karabük, Bartın, Zonguldak)\n",
    "*   **Zaman Aralığı:** 2020-2025\n",
    "*   **Uydu Verisi:** Sentinel-2 MSI (Level-2A)\n",
    "*   **Diğer Veriler:** CORINE Land Cover, (Varsa Mevcut) MTA Maden Ruhsatları, MEŞCERE Verileri\n",
    "\n",
    "### 3.2. Metodolojik Akış\n",
    "1.  **Ön İşleme:** Sentinel-2 görüntülerinin seçimi, bulut maskeleme (QA60), yaz dönemi (Haziran-Eylül) medyan kompozitlerinin oluşturulması.\n",
    "2.  **İndeks Hesabı:** Her yıl için NBR (Normalized Burn Ratio) ve NDVI hesaplanması. Yıllar arası $\\Delta$NBR hesabı.\n",
    "3.  **Trend Analizi:** NBR zaman serisi üzerinde Mann-Kendall trend testi ve Sen's Slope hesaplaması ile bozulma (degradation) tespiti.\n",
    "4.  **Sınıflandırma/Ayrıştırma:** Bozulma tespit edilen alanların nedenlerine göre sınıflandırılması (Yangın, Maden, Kesim)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# --- 1. KURULUM ---\n",
    "import ee\n",
    "import pandas as pd\n",
    "import folium\n",
    "\n",
    "# Yardımcı modüllerimiz\n",
    "from gee.utils import ee_init\n",
    "from gee.aoi import get_aoi\n",
    "\n",
    "MY_PROJECT = 'tubitak-478716'\n",
    "\n",
    "try:\n",
    "    ee_init(project=MY_PROJECT)\n",
    "    print(f\"✅ Google Earth Engine bağlantısı başarılı. Proje: {MY_PROJECT}\")\n",
    "except Exception as e:\n",
    "    print(f\"❌ Bağlantı Hatası: {e}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# --- 2. ÇALIŞMA ALANI VE VERİ HAZIRLIĞI ---\n",
    "\n",
    "# Batı Karadeniz Bölgesi (Tam İl Sınırları)\n",
    "aoi = get_aoi(\"WESTERN_BLACK_SEA\")\n",
    "\n",
    "# Tarih Aralığı: 2020-2025 (Yaz Dönemleri)\n",
    "# Her yılın en temsil edici dönemi (Haziran 1 - Eylül 30) seçilir.\n",
    "years = range(2020, 2026)\n",
    "\n",
    "def get_seasonal_composite(year, geometry):\n",
    "    \"\"\"Sentinel-2 Yaz Dönemi (06-01 ile 09-30 arası) Medyan Kompoziti\"\"\"\n",
    "    start = f\"{year}-06-01\"\n",
    "    end = f\"{year}-09-30\"\n",
    "    \n",
    "    # Bulut Maskesi Fonksiyonu\n",
    "    def mask_clouds(image):\n",
    "        qa = image.select('QA60')\n",
    "        cloud_bit_mask = 1 << 10\n",
    "        cirrus_bit_mask = 1 << 11\n",
    "        mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))\n",
    "        return image.updateMask(mask).divide(10000) # Ölçeklendirme 0-1 arasına\n",
    "\n",
    "    dataset = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')\n",
    "                  .filterBounds(geometry)\n",
    "                  .filterDate(start, end)\n",
    "                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))\n",
    "                  .map(mask_clouds))\n",
    "    \n",
    "    # İndeks Hesaplama (NBR = (NIR-SWIR)/(NIR+SWIR))\n",
    "    # Sentinel-2: NIR=B8, SWIR=B12\n",
    "    def add_indices(image):\n",
    "        nbr = image.normalizedDifference(['B8', 'B12']).rename('NBR')\n",
    "        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')\n",
    "        return image.addBands([nbr, ndvi]).set('year', year).set('system:time_start', ee.Date(start).millis())\n",
    "\n",
    "    return dataset.map(add_indices).median().clip(geometry).set('year', year)\n",
    "\n",
    "print(\"Veri seti hazırlanıyor... (Sentinel-2 2020-2025)\")\n",
    "composites = ee.ImageCollection([get_seasonal_composite(y, aoi) for y in years])\n",
    "print(f\"✅ {len(years)} yıllık kompozit oluşturuldu.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Zaman Serisi Analizi ve İstatistiksel Testler\n",
    "**Yöntem:** Mann-Kendall Trend Testi ve Sen's Slope Estimator.\n",
    "Bu yöntemlerle 2020-2025 arasındaki orman sağlığı trendi (NBR değişimi) piksel bazında hesaplanır.\n",
    "*   **Negatif Eğim (Negative Slope):** Orman kaybını veya bozulmayı ifade eder.\n",
    "*   **Pozitif Eğim:** İyileşme veya büyümeyi ifade eder."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# --- 3. TREND ANALİZİ (Mann-Kendall & Sen's Slope) ---\n",
    "\n",
    "# Analiz için birleştirmeyi 'system:time_start' ile yapıyoruz\n",
    "# Sen's Slope hesabı için zaman bandı ekle\n",
    "def create_time_band(image):\n",
    "    return image.addBands(image.metadata('system:time_start').divide(1000 * 60 * 60 * 24 * 365).rename('t')) # Yıl birimine çevir\n",
    "\n",
    "ts = composites.map(create_time_band)\n",
    "\n",
    "# Sen's Slope Hesaplama (NBR üzerinden)\n",
    "# Bu işlem zaman serisindeki doğrusal eğimi verir.\n",
    "slope_reducer = ee.Reducer.sensSlope()\n",
    "trend_results = ts.select(['t', 'NBR']).reduce(slope_reducer)\n",
    "\n",
    "# 'slope' bandı eğimi gösterir. Negatif değerler azalışı (bozulma) temsil eder.\n",
    "slope = trend_results.select('slope')\n",
    "\n",
    "print(\"✅ Trend analizi tanımlandı.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Değişim Nedenlerinin Ayrıştırılması (Maden, Yangın, Kesim)\n",
    "Bu bölümde, tespit edilen orman kayıpları (Negatif Trend) yardımcı verilerle çakıştırılarak sınıflandırılır.\n",
    "\n",
    "**Kurallar:**\n",
    "1.  **Maden:** Eğer kayıp alanı, Maden Ruhsat Sahaları (veya bilinen maden poligonları) içindeyse.\n",
    "2.  **Yangın:** Eğer kayıp alanı, yangın veritabanı (FIRMS/MODIS Burned Area) ile örtüşüyorsa veya ani düşüş (High Delta NBR) varsa.\n",
    "3.  **Kesim/Diğer:** Yukarıdakiler değilse ve CORINE 'Orman' sınıfındaysa.\n",
    "\n",
    "*Not: Bu örnekte temsili maden alanları veya manuel tanımlanmış geometriler kullanılabilir. Gerçek projede MEŞCERE ve MTA verileri `ee.FeatureCollection` olarak yüklenecektir.*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# --- 4. AYRIŞTIRMA VE GÖRSELLEŞTİRME ---\n",
    "\n",
    "# 1. Aşama: Orman Maskesini Hazırla (ESA WorldCover veya CORINE)\n",
    "wc = ee.ImageCollection(\"ESA/WorldCover/v200\").first()\n",
    "forest_mask = wc.eq(10) # 10: Tree Cover\n",
    "\n",
    "# 2. Aşama: Anlamlı Kayıp Alanlarını Belirle\n",
    "# Sen's slope < -0.015 (Eşik değer - deneysel)\n",
    "degradation = slope.lt(-0.015).And(forest_mask)\n",
    "\n",
    "# Harita Görselleştirme\n",
    "map_center = [41.2, 32.5] # Karabük civarı\n",
    "m = folium.Map(location=map_center, zoom_start=9)\n",
    "\n",
    "def add_ee_layer(self, ee_image_object, vis_params, name):\n",
    "    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)\n",
    "    folium.raster_layers.TileLayer(\n",
    "        tiles=map_id_dict['tile_fetcher'].url_format,\n",
    "        attr='Map Data &copy; <a href=\"https://earthengine.google.com/\">Google Earth Engine</a>',\n",
    "        name=name,\n",
    "        overlay=True,\n",
    "        control=True\n",
    "    ).add_to(self)\n",
    "\n",
    "folium.Map.add_ee_layer = add_ee_layer\n",
    "\n",
    "# Katmanları Ekle\n",
    "vis_rgb = {'min': 0, 'max': 0.3, 'bands': ['B4', 'B3', 'B2']} # Basit RGB\n",
    "vis_slope = {'min': -0.05, 'max': 0.05, 'palette': ['red', 'white', 'green']}\n",
    "vis_loss = {'min': 0, 'max': 1, 'palette': ['black', 'red']}\n",
    "\n",
    "# 2025 Görüntüsü (Referans)\n",
    "m.add_ee_layer(composites.filter(ee.Filter.eq('year', 2025)).first(), vis_rgb, 'Sentinel-2 RGB (2025)')\n",
    "\n",
    "# Trend (Eğim)\n",
    "m.add_ee_layer(slope, vis_slope, \"Orman Trend (2020-2025)\")\n",
    "\n",
    "# Tespit Edilen Kayıplar (Kırmızı)\n",
    "m.add_ee_layer(degradation.selfMask(), {'palette': ['red']}, \"Tespit Edilen Orman Kaybi\")\n",
    "\n",
    "m.add_child(folium.LayerControl())\n",
    "m"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Sonuç ve Öneriler\n",
    "Bu harita, Batı Karadeniz'deki ormanlarda 2020-2025 yılları arasındaki **stres ve kayıp bölgelerini** göstermektedir. \n",
    "- **Kırmızı Alanlar:** Net ve sürekli bitki örtüsü kaybı olan alanlar (Yangın, Kesim veya Madencilik).\n",
    "- Bu veriler MTA ve Orman Genel Müdürlüğü verileriyle çakıştırılarak kesin nedenler raporlanabilir."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open(r"c:\Users\ernoz\Documents\GitHub\Bati-Karadeniz-Orman-Izleme\TUBITAK_Western_Black_Sea_Analysis_2020-2025.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb_content, f, ensure_ascii=False, indent=1)
