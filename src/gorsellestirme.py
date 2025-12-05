# -*- coding: utf-8 -*-
"""
Görselleştirme Modülü
=====================

Grafik ve harita oluşturma fonksiyonları.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
import warnings

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    warnings.warn("matplotlib yüklü değil. Görselleştirme fonksiyonları çalışmayacak.")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from .config import ILLER, YILLAR, RENKLER, IL_KOORDINATLARI, GRAFIK_AYARLARI


class Gorsellestiric:
    """Görselleştirme sınıfı"""
    
    def __init__(self, orman_verileri: Dict, nbr_verileri: Dict, maden_verileri: Dict):
        """
        Görselleştirici başlat.
        
        Args:
            orman_verileri: Orman verileri
            nbr_verileri: NBR verileri
            maden_verileri: Maden verileri
        """
        self.orman_verileri = orman_verileri
        self.nbr_verileri = nbr_verileri
        self.maden_verileri = maden_verileri
        self.iller = ILLER
        self.yillar = YILLAR
        self.renkler = RENKLER
        
        if MATPLOTLIB_AVAILABLE:
            plt.style.use('seaborn-v0_8-darkgrid')
            plt.rcParams['font.family'] = 'DejaVu Sans'
            plt.rcParams['axes.unicode_minus'] = False
    
    def orman_alani_grafigi(self, figsize: Tuple = (12, 6), kaydet: Optional[str] = None) -> Optional[Figure]:
        """
        Orman alanı değişim grafiği oluştur.
        
        Args:
            figsize: Grafik boyutu
            kaydet: Kaydedilecek dosya yolu (opsiyonel)
            
        Returns:
            Figure: Matplotlib figure nesnesi
        """
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib yüklü değil!")
            return None
        
        fig, ax = plt.subplots(figsize=figsize, facecolor=self.renkler["arkaplan"])
        ax.set_facecolor(self.renkler["panel"])
        
        renkler_liste = [self.renkler["yesil"], self.renkler["mavi"], self.renkler["turuncu"]]
        
        for idx, il in enumerate(self.iller):
            alanlar = [self.orman_verileri[il][y]["toplam_alan"] for y in self.yillar]
            ax.plot(self.yillar, alanlar, marker='o', linewidth=2.5, 
                   label=il, color=renkler_liste[idx], markersize=8)
        
        ax.set_xlabel("Yıl", color="white", fontsize=12)
        ax.set_ylabel("Orman Alanı (ha)", color="white", fontsize=12)
        ax.set_title("Batı Karadeniz Bölgesi Orman Alanı Değişimi (2020-2025)", 
                    color="white", fontsize=14, fontweight="bold", pad=15)
        ax.legend(facecolor=self.renkler["panel"], labelcolor="white", fontsize=10)
        ax.tick_params(colors="white")
        ax.grid(True, alpha=0.3, color="white")
        
        for spine in ax.spines.values():
            spine.set_color("white")
            spine.set_alpha(0.3)
        
        plt.tight_layout()
        
        if kaydet:
            plt.savefig(kaydet, dpi=150, facecolor=self.renkler["arkaplan"], 
                       bbox_inches='tight')
        
        return fig
    
    def kayip_dagilim_pasta(self, figsize: Tuple = (10, 8), kaydet: Optional[str] = None) -> Optional[Figure]:
        """
        Orman kaybı dağılım pasta grafiği.
        
        Args:
            figsize: Grafik boyutu
            kaydet: Kaydedilecek dosya yolu
            
        Returns:
            Figure: Matplotlib figure nesnesi
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        fig, ax = plt.subplots(figsize=figsize, facecolor=self.renkler["arkaplan"])
        
        toplam_yangin = sum(
            self.orman_verileri[il][y]["yangin_kaybi"] 
            for il in self.iller for y in self.yillar
        )
        toplam_kesim = sum(
            self.orman_verileri[il][y]["kesim_kaybi"] 
            for il in self.iller for y in self.yillar
        )
        toplam_maden = sum(
            self.orman_verileri[il][y]["maden_kaybi"] 
            for il in self.iller for y in self.yillar
        )
        
        veriler = [toplam_yangin, toplam_kesim, toplam_maden]
        etiketler = [
            f"Yangın\n{toplam_yangin:,.0f} ha",
            f"Kesim\n{toplam_kesim:,.0f} ha",
            f"Madencilik\n{toplam_maden:,.0f} ha"
        ]
        renkler_pasta = [self.renkler["kirmizi"], self.renkler["turuncu"], self.renkler["sari"]]
        
        wedges, texts, autotexts = ax.pie(
            veriler, 
            labels=etiketler, 
            autopct='%1.1f%%',
            colors=renkler_pasta,
            explode=(0.05, 0.03, 0.03),
            shadow=True,
            startangle=90
        )
        
        for text in texts + autotexts:
            text.set_color("white")
            text.set_fontsize(11)
        
        ax.set_title("Orman Kaybı Nedenlerinin Dağılımı (2020-2025)", 
                    color="white", fontsize=14, fontweight="bold", pad=20)
        
        plt.tight_layout()
        
        if kaydet:
            plt.savefig(kaydet, dpi=150, facecolor=self.renkler["arkaplan"], 
                       bbox_inches='tight')
        
        return fig
    
    def nbr_zaman_serisi(self, il: Optional[str] = None, figsize: Tuple = (12, 6), 
                         kaydet: Optional[str] = None) -> Optional[Figure]:
        """
        ΔNBR zaman serisi grafiği.
        
        Args:
            il: Belirli bir il (None ise tüm iller)
            figsize: Grafik boyutu
            kaydet: Kaydedilecek dosya yolu
            
        Returns:
            Figure: Matplotlib figure nesnesi
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        fig, ax = plt.subplots(figsize=figsize, facecolor=self.renkler["arkaplan"])
        ax.set_facecolor(self.renkler["panel"])
        
        iller_goster = [il] if il else self.iller
        renkler_liste = [self.renkler["kirmizi"], self.renkler["turuncu"], self.renkler["sari"]]
        
        for idx, i in enumerate(iller_goster):
            degerler = [self.nbr_verileri[i][y]["delta_nbr"] for y in self.yillar]
            ax.plot(self.yillar, degerler, marker='s', linewidth=2.5, 
                   label=i, color=renkler_liste[idx % 3], markersize=8)
        
        # Eşik çizgileri
        ax.axhline(y=0.27, color='yellow', linestyle='--', alpha=0.7, 
                  label='Düşük-Orta Eşiği (0.27)')
        ax.axhline(y=0.44, color='orange', linestyle='--', alpha=0.7, 
                  label='Orta-Yüksek Eşiği (0.44)')
        ax.axhline(y=0.66, color='red', linestyle='--', alpha=0.7, 
                  label='Yüksek Şiddet Eşiği (0.66)')
        
        ax.set_xlabel("Yıl", color="white", fontsize=12)
        ax.set_ylabel("ΔNBR Değeri", color="white", fontsize=12)
        ax.set_title("ΔNBR Zaman Serisi Analizi", color="white", 
                    fontsize=14, fontweight="bold", pad=15)
        ax.legend(facecolor=self.renkler["panel"], labelcolor="white", 
                 fontsize=9, loc='upper right')
        ax.tick_params(colors="white")
        ax.grid(True, alpha=0.3, color="white")
        
        for spine in ax.spines.values():
            spine.set_color("white")
            spine.set_alpha(0.3)
        
        plt.tight_layout()
        
        if kaydet:
            plt.savefig(kaydet, dpi=150, facecolor=self.renkler["arkaplan"], 
                       bbox_inches='tight')
        
        return fig
    
    def yillik_kayip_bar(self, figsize: Tuple = (14, 7), kaydet: Optional[str] = None) -> Optional[Figure]:
        """
        Yıllık orman kaybı çubuk grafiği.
        
        Args:
            figsize: Grafik boyutu
            kaydet: Kaydedilecek dosya yolu
            
        Returns:
            Figure: Matplotlib figure nesnesi
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        fig, ax = plt.subplots(figsize=figsize, facecolor=self.renkler["arkaplan"])
        ax.set_facecolor(self.renkler["panel"])
        
        x = np.arange(len(self.yillar))
        width = 0.25
        
        renkler_liste = [self.renkler["yesil"], self.renkler["mavi"], self.renkler["turuncu"]]
        
        for idx, il in enumerate(self.iller):
            kayiplar = [
                self.orman_verileri[il][y]["yangin_kaybi"] + 
                self.orman_verileri[il][y]["kesim_kaybi"] + 
                self.orman_verileri[il][y]["maden_kaybi"]
                for y in self.yillar
            ]
            ax.bar(x + idx * width, kayiplar, width, label=il, 
                  color=renkler_liste[idx], alpha=0.8)
        
        ax.set_xlabel("Yıl", color="white", fontsize=12)
        ax.set_ylabel("Toplam Kayıp (ha)", color="white", fontsize=12)
        ax.set_title("Yıllık Orman Kaybı - İl Karşılaştırması", 
                    color="white", fontsize=14, fontweight="bold", pad=15)
        ax.set_xticks(x + width)
        ax.set_xticklabels(self.yillar)
        ax.legend(facecolor=self.renkler["panel"], labelcolor="white", fontsize=10)
        ax.tick_params(colors="white")
        ax.grid(True, alpha=0.3, axis='y', color="white")
        
        for spine in ax.spines.values():
            spine.set_color("white")
            spine.set_alpha(0.3)
        
        plt.tight_layout()
        
        if kaydet:
            plt.savefig(kaydet, dpi=150, facecolor=self.renkler["arkaplan"], 
                       bbox_inches='tight')
        
        return fig
    
    def risk_haritasi(self, risk_verileri: Dict, figsize: Tuple = (12, 10), 
                      kaydet: Optional[str] = None) -> Optional[Figure]:
        """
        Basitleştirilmiş risk haritası oluştur.
        
        Args:
            risk_verileri: İl bazında risk skorları
            figsize: Grafik boyutu
            kaydet: Kaydedilecek dosya yolu
            
        Returns:
            Figure: Matplotlib figure nesnesi
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        fig, ax = plt.subplots(figsize=figsize, facecolor=self.renkler["arkaplan"])
        ax.set_facecolor(self.renkler["panel"])
        
        for il in self.iller:
            koord = IL_KOORDINATLARI[il]
            risk = risk_verileri[il]["risk_skoru"]
            seviye = risk_verileri[il]["risk_seviyesi"]
            
            if seviye == "YÜKSEK":
                renk = self.renkler["kirmizi"]
            elif seviye == "ORTA":
                renk = self.renkler["turuncu"]
            else:
                renk = self.renkler["yesil"]
            
            # Daire çiz
            circle = plt.Circle((koord["lon"], koord["lat"]), 0.18, 
                               color=renk, alpha=0.7)
            ax.add_patch(circle)
            
            # İsim ve risk bilgisi
            ax.annotate(
                f"{il}\n{seviye}\n({risk:.0%})",
                (koord["lon"], koord["lat"]),
                ha='center', va='center',
                fontsize=11, fontweight='bold',
                color='white'
            )
        
        ax.set_xlim(31.0, 33.5)
        ax.set_ylim(40.8, 42.0)
        ax.set_xlabel("Boylam", color="white", fontsize=12)
        ax.set_ylabel("Enlem", color="white", fontsize=12)
        ax.set_title("Batı Karadeniz Bölgesi - Orman Yangını Risk Haritası", 
                    color="white", fontsize=14, fontweight="bold", pad=15)
        ax.tick_params(colors="white")
        ax.grid(True, alpha=0.3, color="white")
        
        for spine in ax.spines.values():
            spine.set_color("white")
            spine.set_alpha(0.3)
        
        # Legend
        yuksek = mpatches.Patch(color=self.renkler["kirmizi"], label='Yüksek Risk (>70%)')
        orta = mpatches.Patch(color=self.renkler["turuncu"], label='Orta Risk (50-70%)')
        dusuk = mpatches.Patch(color=self.renkler["yesil"], label='Düşük Risk (<50%)')
        ax.legend(handles=[yuksek, orta, dusuk], loc='lower right', 
                 facecolor=self.renkler["panel"], labelcolor='white', fontsize=10)
        
        plt.tight_layout()
        
        if kaydet:
            plt.savefig(kaydet, dpi=150, facecolor=self.renkler["arkaplan"], 
                       bbox_inches='tight')
        
        return fig
    
    def trend_grafigi(self, trend_sonuclari: Dict, figsize: Tuple = (14, 6), 
                      kaydet: Optional[str] = None) -> Optional[Figure]:
        """
        Trend analizi sonuçları grafiği.
        
        Args:
            trend_sonuclari: İl bazında trend sonuçları
            figsize: Grafik boyutu
            kaydet: Kaydedilecek dosya yolu
            
        Returns:
            Figure: Matplotlib figure nesnesi
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        fig, axes = plt.subplots(1, 3, figsize=figsize, facecolor=self.renkler["arkaplan"])
        
        renkler_liste = [self.renkler["yesil"], self.renkler["mavi"], self.renkler["turuncu"]]
        
        for idx, (il, ax) in enumerate(zip(self.iller, axes)):
            ax.set_facecolor(self.renkler["panel"])
            
            alanlar = [self.orman_verileri[il][y]["toplam_alan"] for y in self.yillar]
            sonuc = trend_sonuclari[il]
            
            # Veri noktaları
            ax.scatter(self.yillar, alanlar, color=renkler_liste[idx], 
                      s=100, zorder=3, label='Gerçek Veri')
            
            # Trend çizgisi (Sen's Slope ile)
            x_trend = np.array(self.yillar)
            y_trend = alanlar[0] + sonuc.sens_slope * (x_trend - x_trend[0])
            ax.plot(x_trend, y_trend, '--', color='white', linewidth=2, 
                   alpha=0.8, label=f"Trend: {sonuc.sens_slope:.1f} ha/yıl")
            
            ax.set_xlabel("Yıl", color="white", fontsize=10)
            ax.set_ylabel("Orman Alanı (ha)", color="white", fontsize=10)
            
            anlamli = "✓" if sonuc.anlamli_mi else "✗"
            ax.set_title(f"{il}\np={sonuc.p_degeri:.4f} {anlamli}", 
                        color="white", fontsize=12, fontweight="bold")
            ax.legend(facecolor=self.renkler["panel"], labelcolor="white", fontsize=9)
            ax.tick_params(colors="white")
            ax.grid(True, alpha=0.3, color="white")
            
            for spine in ax.spines.values():
                spine.set_color("white")
                spine.set_alpha(0.3)
        
        plt.suptitle("Mann-Kendall Trend Analizi ve Sen's Slope", 
                    color="white", fontsize=14, fontweight="bold", y=1.02)
        plt.tight_layout()
        
        if kaydet:
            plt.savefig(kaydet, dpi=150, facecolor=self.renkler["arkaplan"], 
                       bbox_inches='tight')
        
        return fig
    
    # Plotly interaktif grafikler
    def interaktif_orman_grafigi(self) -> Optional['go.Figure']:
        """
        Plotly ile interaktif orman alanı grafiği.
        
        Returns:
            go.Figure: Plotly figure nesnesi
        """
        if not PLOTLY_AVAILABLE:
            print("plotly yüklü değil!")
            return None
        
        fig = go.Figure()
        
        renkler_plotly = ['#2ecc71', '#3498db', '#e67e22']
        
        for idx, il in enumerate(self.iller):
            alanlar = [self.orman_verileri[il][y]["toplam_alan"] for y in self.yillar]
            
            fig.add_trace(go.Scatter(
                x=self.yillar,
                y=alanlar,
                mode='lines+markers',
                name=il,
                line=dict(color=renkler_plotly[idx], width=3),
                marker=dict(size=10)
            ))
        
        fig.update_layout(
            title="Batı Karadeniz Bölgesi Orman Alanı Değişimi (2020-2025)",
            xaxis_title="Yıl",
            yaxis_title="Orman Alanı (ha)",
            template="plotly_dark",
            hovermode="x unified"
        )
        
        return fig
    
    def interaktif_kayip_grafigi(self) -> Optional['go.Figure']:
        """
        Plotly ile interaktif kayıp dağılımı grafiği.
        
        Returns:
            go.Figure: Plotly figure nesnesi
        """
        if not PLOTLY_AVAILABLE:
            return None
        
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "pie"}, {"type": "bar"}]],
            subplot_titles=("Kayıp Dağılımı", "İl Bazında Kayıp")
        )
        
        # Pasta grafik
        toplam_yangin = sum(
            self.orman_verileri[il][y]["yangin_kaybi"] 
            for il in self.iller for y in self.yillar
        )
        toplam_kesim = sum(
            self.orman_verileri[il][y]["kesim_kaybi"] 
            for il in self.iller for y in self.yillar
        )
        toplam_maden = sum(
            self.orman_verileri[il][y]["maden_kaybi"] 
            for il in self.iller for y in self.yillar
        )
        
        fig.add_trace(go.Pie(
            labels=["Yangın", "Kesim", "Madencilik"],
            values=[toplam_yangin, toplam_kesim, toplam_maden],
            marker_colors=['#e74c3c', '#e67e22', '#f39c12']
        ), row=1, col=1)
        
        # Bar grafik
        for il in self.iller:
            kayiplar = [
                self.orman_verileri[il][y]["yangin_kaybi"] + 
                self.orman_verileri[il][y]["kesim_kaybi"] + 
                self.orman_verileri[il][y]["maden_kaybi"]
                for y in self.yillar
            ]
            fig.add_trace(go.Bar(
                name=il,
                x=self.yillar,
                y=kayiplar
            ), row=1, col=2)
        
        fig.update_layout(
            template="plotly_dark",
            showlegend=True,
            title_text="Orman Kaybı Analizi"
        )
        
        return fig
