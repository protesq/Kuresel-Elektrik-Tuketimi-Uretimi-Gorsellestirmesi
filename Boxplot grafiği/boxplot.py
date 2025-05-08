import pandas as pd
import numpy as np
import plotly.express as px

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

# Manuel kıta sıralaması
order = [
    'Asya & Okyanusya',
    'Kuzey Amerika',
    'Avrasya',
    'Orta & Güney Amerika',
    'Avrupa',
    'Orta Doğu',
    'Afrika'
]

fig = px.box(
    long_df,
    x="Region",
    y="Value",
    color="Type",
    points=False,
    category_orders={"Region": order},  # Kıtaları belirtilen sırada göster
    labels={"Value": "Elektrik (TWh)", "Region": "Kıtalar"},
    title=f"Kıtalara Göre Elektrik Üretimi ve Tüketimi ({year})",
    color_discrete_map={"Üretim": "#1f77b4", "Tüketim": "#2ca02c"}
)

fig.update_layout(
    boxmode="group",
    legend_title_text="",
    template="plotly_white",
    height=800,
    width=1200
)

# Y eksenini daha okunaklı hale getir
fig.update_yaxes(title_font=dict(size=14), tickfont=dict(size=12))

# X eksenini daha okunaklı hale getir
fig.update_xaxes(title_font=dict(size=14), tickfont=dict(size=12))

# Grafiği kaydet ve göster
fig.write_html("kitalar_elektrik_boxplot.html")
fig.write_image("kitalar_elektrik_boxplot.png", scale=2)
fig.show()
