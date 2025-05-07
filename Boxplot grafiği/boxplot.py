import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Ülke isimlerini Türkçe'ye çeviren sözlük
country_tr = {
    'Albania': 'Arnavutluk',
    'Austria': 'Avusturya',
    'Belgium': 'Belçika',
    'Bosnia and Herzegovina': 'Bosna Hersek',
    'Bulgaria': 'Bulgaristan',
    'Croatia': 'Hırvatistan',
    'Cyprus': 'Kıbrıs',
    'Czech Republic': 'Çekya',
    'Denmark': 'Danimarka',
    'Estonia': 'Estonya',
    'Finland': 'Finlandiya',
    'France': 'Fransa',
    'Germany': 'Almanya',
    'Greece': 'Yunanistan',
    'Hungary': 'Macaristan',
    'Iceland': 'İzlanda',
    'Ireland': 'İrlanda',
    'Italy': 'İtalya',
    'Latvia': 'Letonya',
    'Lithuania': 'Litvanya',
    'Luxembourg': 'Lüksemburg',
    'Malta': 'Malta',
    'Montenegro': 'Karadağ',
    'Netherlands': 'Hollanda',
    'North Macedonia': 'Kuzey Makedonya',
    'Norway': 'Norveç',
    'Poland': 'Polonya',
    'Portugal': 'Portekiz',
    'Romania': 'Romanya',
    'Serbia': 'Sırbistan',
    'Slovakia': 'Slovakya',
    'Slovenia': 'Slovenya',
    'Spain': 'İspanya',
    'Sweden': 'İsveç',
    'Switzerland': 'İsviçre',
    'Turkey': 'Türkiye',
    'United Kingdom': 'Birleşik Krallık',
    'Argentina': 'Arjantin',
    'Bolivia': 'Bolivya',
    'Brazil': 'Brezilya',
    'Chile': 'Şili',
    'Colombia': 'Kolombiya',
    'Costa Rica': 'Kosta Rika',
    'Cuba': 'Küba',
    'Dominican Republic': 'Dominik Cumhuriyeti',
    'Ecuador': 'Ekvador',
    'El Salvador': 'El Salvador',
    'Guatemala': 'Guatemala',
    'Haiti': 'Haiti',
    'Honduras': 'Honduras',
    'Jamaica': 'Jamaika',
    'Mexico': 'Meksika',
    'Nicaragua': 'Nikaragua',
    'Panama': 'Panama',
    'Paraguay': 'Paraguay',
    'Peru': 'Peru',
    'Puerto Rico': 'Porto Riko',
    'Trinidad and Tobago': 'Trinidad ve Tobago',
    'Uruguay': 'Uruguay',
    'Venezuela': 'Venezuela'
}

df = pd.read_csv('Global Electricity Statistics.csv')

# Veri setini incele ve hazırla
# 2020
df_2020 = df[['Country', 'Features', 'Region', '2020']]

# Değer dönüşümlerini temizle
df_2020['2020'] = pd.to_numeric(df_2020['2020'], errors='coerce')

# Avrupa ve Güney Amerika verilerini filtrele
europe_data = df_2020[df_2020['Region'] == 'Europe'].dropna(subset=['2020'])
south_america_data = df_2020[df_2020['Region'] == 'Central & South America'].dropna(subset=['2020'])

# Sadece üretim (net generation) verilerini ayır
europe_generation = europe_data[europe_data['Features'] == 'net generation']['2020']
south_america_generation = south_america_data[south_america_data['Features'] == 'net generation']['2020']

# Aykırı değerleri kontrol et ve belirle
def get_outliers(data):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = [x for x in data if x < lower_bound or x > upper_bound]
    return outliers, lower_bound, upper_bound

europe_gen_outliers, eu_gen_lower, eu_gen_upper = get_outliers(europe_generation)
sa_gen_outliers, sa_gen_lower, sa_gen_upper = get_outliers(south_america_generation)

# Aykırı değerlerin ülkelerini bul
def get_outlier_countries(region_data, feature, outliers):
    outlier_countries = []
    for outlier in outliers:
        country = region_data[(region_data['Features'] == feature) & 
                             (region_data['2020'] == outlier)]['Country'].values
        if len(country) > 0:
    
            country_name = country[0].strip()
            tr_name = country_tr.get(country_name, country_name)
            outlier_countries.append((tr_name, outlier))
    return outlier_countries

europe_gen_outlier_countries = get_outlier_countries(europe_data, 'net generation', europe_gen_outliers)
sa_gen_outlier_countries = get_outlier_countries(south_america_data, 'net generation', sa_gen_outliers)

fig = go.Figure()

# Elektrik üretim verileri
fig.add_trace(go.Box(
    y=europe_generation,
    name="Avrupa",
    boxpoints='outliers',
    marker=dict(color='indianred'),
    hoverinfo='y',
    customdata=europe_gen_outlier_countries if europe_gen_outlier_countries else None,
    hovertemplate='%{y} kWh<br>%{customdata}' if europe_gen_outlier_countries else '%{y} kWh'
))

fig.add_trace(go.Box(
    y=south_america_generation,
    name="G.Amerika",
    boxpoints='outliers',
    marker=dict(color='royalblue'),
    hoverinfo='y',
    customdata=sa_gen_outlier_countries if sa_gen_outlier_countries else None,
    hovertemplate='%{y} kWh<br>%{customdata}' if sa_gen_outlier_countries else '%{y} kWh'
))


for country, value in europe_gen_outlier_countries:
    fig.add_annotation(
        x="Avrupa",
        y=value,
        text=country,
        font=dict(color="indianred", size=12),
        showarrow=False,
        xanchor="left",
        xshift=1
    )

for country, value in sa_gen_outlier_countries:
    fig.add_annotation(
        x="G.Amerika",
        y=value,
        text=country,
        font=dict(color="royalblue", size=12),
        showarrow=False,
        xanchor="right",
        xshift=-10
    )

# Layout
fig.update_layout(
    title="Avrupa ve Güney Amerika Elektrik Üretim Karşılaştırması (2020)",
    height=700,
    width=1000,
    boxmode='group',
    template='plotly_white',
    yaxis_title="Elektrik Üretim (kWh)",
    font=dict(
        family="Arial, sans-serif",
        size=12,
    ),
    margin=dict(t=100, b=80), 
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=12),
        tickmode='array',
        tickvals=[0, 1],
        ticktext=['', ''],
        showticklabels=False
    )
)

fig.add_annotation(
    x=0,
    y=0, 
    text="Avrupa",
    showarrow=False,
    font=dict(size=12),
    xanchor="center",  
    yanchor="top",
    yshift=-40  
)

fig.add_annotation(
    x=1,
    y=0,
    text="G.Amerika",
    showarrow=False,
    font=dict(size=12),
    xanchor="center",  
    yanchor="top",
    yshift=-40  
)

fig.write_html("avrupa_guney_amerika_elektrik_uretim_2020.html")
fig.show()
