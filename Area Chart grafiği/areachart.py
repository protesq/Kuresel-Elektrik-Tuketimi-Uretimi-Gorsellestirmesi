import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv("Global Electricity Statistics.csv")

uretim_df = df[df["Features"] == "net generation"].copy()

yillar = [str(yil) for yil in range(1990, 2021)]  # Her yıl için
kitalar = ["Africa", "Asia & Oceania", "Europe", "North America", "South America"]

veri_listesi = []

for kita in kitalar:
    kita_df = uretim_df[uretim_df["Region"] == kita]
    
    for yil in yillar:
        kita_df[yil] = pd.to_numeric(kita_df[yil], errors="coerce")
        toplam = kita_df[yil].sum()
        
        veri_listesi.append({
            "Kıta": kita,
            "Yıl": int(yil),
            "Üretim": toplam
        })

veri_df = pd.DataFrame(veri_listesi)

kita_siralama = ["Asia & Oceania", "North America", "Europe", "South America", "Africa"]
veri_df["Kıta"] = pd.Categorical(veri_df["Kıta"], categories=kita_siralama, ordered=True)
veri_df = veri_df.sort_values(["Yıl", "Kıta"])

# Özel renk skalası
renk_skalasi = {
    "Asia & Oceania": "#4C78A8",   # Mavi
    "North America": "#72B7B2",    # Turkuaz
    "Europe": "#54A24B",           # Yeşil
    "South America": "#EECA3B",    # Sarı
    "Africa": "#E45756"            # Kırmızı
}

# Area chart oluştur
fig = px.area(
    veri_df, 
    x="Yıl", 
    y="Üretim", 
    color="Kıta",
    color_discrete_map=renk_skalasi,
    title="Kıtalara Göre Elektrik Üretimi (1990-2020)",
    labels={"Üretim": "Elektrik Üretimi (TWh)", "Yıl": "Yıl", "Kıta": "Kıta"},
    template="plotly_white"
)

# Grafik ayarları
fig.update_layout(
    title_x=0.5,
    legend=dict(
        title="Kıtalar",
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99,
        font=dict(size=14),
        bgcolor="rgba(255, 255, 255, 0.8)"
    ),
    width=1400,
    height=700,
    hovermode="x unified",  # X eksenindeki tüm değerleri aynı anda göster
    xaxis=dict(
        dtick=5,  # 5 yıllık aralıklarla etiketler
        tickangle=0
    )
)

# X ekseni düzenlemeleri
fig.update_xaxes(
    range=[1990, 2020],
    tickmode='linear',
    tick0=1990,
    dtick=5
)

# Çizgi kalınlığı ayarı
fig.update_traces(line=dict(width=0.5))

# Hover bilgisi düzenle
fig.update_traces(
    hovertemplate='<b>%{y:,.0f} TWh</b>'
)

fig.show()

fig.write_html("elektrik_alan_grafik.html")
fig.write_image("elektrik_alan_grafik.png", width=1400, height=700, scale=2) 