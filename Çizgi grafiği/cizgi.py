import pandas as pd
import plotly.express as px 
import numpy as np


df = pd.read_csv('Global Electricity Statistics.csv')

# Sadece Afrika ve net generation verisini al
afrika_df = df[(df['Region'] == 'Africa') & (df['Features'] == 'net generation')]

# Ülke isimlerindeki boşlukları temizle
afrika_df['Country'] = afrika_df['Country'].str.strip()

# 2020 yılına göre en çok elektrik üreten 6 ülkeyi seç
afrika_df['2020'] = pd.to_numeric(afrika_df['2020'], errors='coerce')
top_ulkeler_en = afrika_df.sort_values(by='2020', ascending=False).head(6)['Country'].values

# Ülke isimlerini Türkçeleştir
ulkeler_tr = {
    "South Africa": "Güney Afrika",
    "Egypt": "Mısır",
    "Algeria": "Cezayir",
    "Morocco": "Fas",
    "Libya": "Libya",
    "Nigeria": "Nijerya"
}

# Sadece seçilen ülkeleri filtrele ve isimleri Türkçeleştir
secilen_df = afrika_df[afrika_df['Country'].isin(top_ulkeler_en)].copy()
secilen_df['Country'] = secilen_df['Country'].replace(ulkeler_tr)

yillar = ['1980', '1985', '1990', '1995', '2000', '2005', '2010', '2015', '2020']

veri_dict = {'Ülke': [], 'Yıl': [], 'Elektrik Üretimi (TWh)': []}

# Ülkeleri Türkçe isimle al
for ulke in secilen_df['Country'].unique():
    ulke_verisi = secilen_df[secilen_df['Country'] == ulke]
    if not ulke_verisi.empty:
        for yil in yillar:
            deger = ulke_verisi[yil].values[0]
            if isinstance(deger, str) and deger.strip() == '--':
                deger = np.nan
            else:
                try:
                    deger = float(deger)
                except:
                    deger = np.nan
            
            veri_dict['Ülke'].append(ulke)
            veri_dict['Yıl'].append(yil)
            veri_dict['Elektrik Üretimi (TWh)'].append(deger)

veri_df = pd.DataFrame(veri_dict)

fig = px.line(
    veri_df, 
    x='Yıl', 
    y='Elektrik Üretimi (TWh)', 
    color='Ülke',
    markers=True, 
    line_shape='linear',
    title='Afrika\'daki Başlıca Ülkelerin Elektrik Üretimi (1980-2020)'
)

fig.update_layout(
    title={
        'text': 'Afrika\'daki Başlıca Ülkelerin Elektrik Üretimi (1980-2020)',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    xaxis_title='Yıl',
    yaxis_title='Elektrik Üretimi (TWh)',
    legend_title='Ülke',
    font=dict(
        family="Arial, sans-serif",
        size=14
    ),
    height=700,
    template='plotly_white',
    hovermode='x unified'
)

fig.update_traces(
    marker=dict(size=10),
    line=dict(width=3)
)

fig.update_yaxes(rangemode='tozero')

fig.write_html('afrika_elektrik_uretim_grafik.html')
fig.show()
