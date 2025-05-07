import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from math import ceil

# İngilizce-Türkçe ülke isimleri eşleştirmesi
country_tr_map = {
    "Albania": "Arnavutluk",
    "Austria": "Avusturya",
    "Belgium": "Belçika",
    "Bosnia and Herzegovina": "Bosna-Hersek",
    "Bulgaria": "Bulgaristan",
    "Croatia": "Hırvatistan",
    "Cyprus": "Kıbrıs",
    "Czechia": "Çekya",
    "Denmark": "Danimarka",
    "Estonia": "Estonya",
    "Faroe Islands": "Faroe Adaları",
    "Finland": "Finlandiya",
    "France": "Fransa",
    "Germany": "Almanya",
    "Gibraltar": "Cebelitarık",
    "Greece": "Yunanistan",
    "Hungary": "Macaristan",
    "Iceland": "İzlanda",
    "Ireland": "İrlanda",
    "Italy": "İtalya",
    "Kosovo": "Kosova",
    "Latvia": "Letonya",
    "Lithuania": "Litvanya",
    "Luxembourg": "Lüksemburg",
    "Malta": "Malta",
    "Montenegro": "Karadağ",
    "North Macedonia": "Kuzey Makedonya",
    "Netherlands": "Hollanda",
    "Norway": "Norveç",
    "Poland": "Polonya",
    "Portugal": "Portekiz",
    "Romania": "Romanya",
    "Serbia": "Sırbistan",
    "Slovakia": "Slovakya",
    "Slovenia": "Slovenya",
    "Spain": "İspanya",
    "Sweden": "İsveç",
    "Switzerland": "İsviçre",
    "Turkey": "Türkiye",
    "United Kingdom": "Birleşik Krallık"
}

df = pd.read_csv("Global Electricity Statistics.csv")

# Avrupa ülkelerini ve net üretim verilerini filtrele
europe_df = df[(df["Region"] == "Europe") & (df["Features"] == "net generation")].copy()

# 2020 yılı verilerini sayısal değerlere çevir
europe_df["2020"] = pd.to_numeric(europe_df["2020"], errors="coerce")
europe_df = europe_df.dropna(subset=["2020"])

# Orijinal ülke isimlerini korumadan önce yeni bir sütun ekle
europe_df["Country_EN"] = europe_df["Country"].copy()
# Ülke isimlerini Türkçeye çevir
europe_df["Country"] = europe_df["Country"].map(country_tr_map).fillna(europe_df["Country"])

# Histogram için aralıkları belirle
bins = [0, 100, 200, 300, 400, 700]
labels = ['0-100', '100-200', '200-300', '300-400', '400-700']
europe_df['bin'] = pd.cut(europe_df['2020'], bins=bins, labels=labels)

# Her aralıktaki ülkeleri bul
country_groups = {}
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']

def format_countries_grid(countries, cols=3):
    rows = ceil(len(countries) / cols)
    countries_padded = countries + [''] * (rows * cols - len(countries))
    grid = []
    for i in range(0, len(countries_padded), cols):
        row = countries_padded[i:i+cols]
        grid.append(' | '.join(filter(None, row)))
    return '<br>'.join(grid)

for label in labels:
    mask = europe_df['bin'] == label
    countries = sorted(europe_df[mask]['Country'].tolist())  # Türkçe isimler kullanılıyor
    if countries:
        country_groups[label] = {
            'countries': countries,
            'color': colors[labels.index(label)],
            'formatted_countries': format_countries_grid(countries)
        }

# Histogram çiz
fig = go.Figure()

for label in labels:
    mask = europe_df['bin'] == label
    count = len(europe_df[mask])
    if count > 0:
        fig.add_trace(go.Bar(
            x=[label],
            y=[count],
            name=f"{label} TWh<br>" + country_groups[label]['formatted_countries'],
            marker_color=country_groups[label]['color'],
            width=1
        ))

# Legend başlığını Türkçeye çevir ve diğer ayarları yap
fig.update_layout(
    title="2020 Yılı Avrupa Ülkelerinin Elektrik Üretim Dağılımı",
    title_x=0.5,
    width=1400,
    height=700,
    bargap=0,
    xaxis_title="Elektrik Üretimi (TWh)",
    yaxis_title="Ülke Sayısı",
    paper_bgcolor="white",
    plot_bgcolor="white",
    legend=dict(
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.01,
        bgcolor='rgba(255, 255, 255, 0.8)',
        title="Ülkeler ve Üretim Aralıkları",
        font=dict(size=15)
    )
)


fig.show()
pio.write_image(fig, "histogrampng.png")
