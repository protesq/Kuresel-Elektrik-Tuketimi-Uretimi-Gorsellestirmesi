import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots

df = pd.read_csv("Global Electricity Statistics.csv")

#2020
year = "2020"
if year not in df.columns:
    numeric_cols = [c for c in df.columns if c.isdigit()]
    year = numeric_cols[-1]

#  Üretim ve tüketim verilerini ayır
gen_df  = df[df["Features"] == "net generation"].copy()
cons_df = df[df["Features"] == "net consumption"].copy()

def to_float(x):
    if isinstance(x, str) and x.lower() in ["ie", "--", "nan", ""]:
        return np.nan
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan

gen_df[year]  = gen_df[year].apply(to_float)
cons_df[year] = cons_df[year].apply(to_float)

# Kıta isimlerini Türkçeleştirme sözlüğü
kita_cevirisi = {
    'Africa': 'Afrika',
    'Asia & Oceania': 'Asya & Okyanusya',
    'Central & South America': 'Orta & Güney Amerika',
    'Eurasia': 'Avrasya',
    'Europe': 'Avrupa',
    'Middle East': 'Orta Doğu',
    'North America': 'Kuzey Amerika'
}

# Kıta isimlerini Türkçeleştir
gen_df['Region'] = gen_df['Region'].map(kita_cevirisi)
cons_df['Region'] = cons_df['Region'].map(kita_cevirisi)

gen_df  = gen_df.dropna(subset=[year])[["Region", year]].assign(Type="Üretim")
cons_df = cons_df.dropna(subset=[year])[["Region", year]].assign(Type="Tüketim")

long_df = pd.concat([gen_df, cons_df], ignore_index=True).rename(columns={year: "Value"})

# İki grup için veri setlerini ayır
buyuk_kitalar = ['Asya & Okyanusya', 'Kuzey Amerika']
diger_kitalar = ['Avrasya', 'Orta & Güney Amerika', 'Avrupa', 'Orta Doğu', 'Afrika']

buyuk_df = long_df[long_df['Region'].isin(buyuk_kitalar)]
diger_df = long_df[long_df['Region'].isin(diger_kitalar)]

# Alt grafikler oluştur
fig = make_subplots(rows=2, cols=1, 
                    subplot_titles=("Büyük Kıtalar", "Diğer Kıtalar"),
                    vertical_spacing=0.15)

# Büyük kıtalar için boxplot
fig1 = px.box(buyuk_df, x="Region", y="Value", color="Type",
              points=False,
              category_orders={"Region": buyuk_kitalar},
              color_discrete_map={"Üretim": "#1f77b4", "Tüketim": "#2ca02c"})

# Diğer kıtalar için boxplot
fig2 = px.box(diger_df, x="Region", y="Value", color="Type",
              points=False,
              category_orders={"Region": diger_kitalar},
              color_discrete_map={"Üretim": "#1f77b4", "Tüketim": "#2ca02c"})

# Grafikleri alt grafiklere ekle
for trace in fig1.data:
    fig.add_trace(trace, row=1, col=1)
for trace in fig2.data:
    fig.add_trace(trace, row=2, col=1)

# Grafik düzenini ayarla
fig.update_layout(
    title_text=f"Kıtalara Göre Elektrik Üretimi ve Tüketimi ({year})",
    height=1200,
    width=1200,
    showlegend=True,
    template="plotly_white",
    boxmode="group"
)

# Y eksenlerini düzenle
fig.update_yaxes(title_text="Elektrik (TWh)", row=1, col=1)
fig.update_yaxes(title_text="Elektrik (TWh)", row=2, col=1)

# X eksenlerini düzenle
fig.update_xaxes(title_text="", row=1, col=1)
fig.update_xaxes(title_text="", row=2, col=1)

# Grafiği kaydet ve göster
fig.write_html("elektrik_boxplot.html")
fig.write_image("elektrik_boxplot.png", scale=2)
fig.show()
