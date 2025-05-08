import pandas as pd
import plotly.graph_objects as go

# Veriyi oku
df = pd.read_csv("Global Electricity Statistics.csv")

# 2020 yılı için üretim ve tüketim verilerini filtrele
uretim_df = df[df['Features'] == 'net generation'].copy()
tuketim_df = df[df['Features'] == 'net consumption'].copy()

# 2020 yılı verilerini al ve sayısal değerlere dönüştür
uretim_df['2020'] = pd.to_numeric(uretim_df['2020'], errors='coerce')
tuketim_df['2020'] = pd.to_numeric(tuketim_df['2020'], errors='coerce')

# En çok üreten ve tüketen 10 ülkeyi bul
top10_uretim = uretim_df.nlargest(10, '2020')[['Country', '2020']]
top10_tuketim = tuketim_df.nlargest(10, '2020')[['Country', '2020']]

# Üretim ve tüketim verilerini birleştir
top10_uretim = top10_uretim.rename(columns={'2020': 'Uretim'})
top10_tuketim = top10_tuketim.rename(columns={'2020': 'Tuketim'})
top10_data = pd.merge(top10_uretim, top10_tuketim, on='Country', how='outer')

# Ülke isimlerini temizle (boşluk, büyük/küçük harf hatası vs.)
top10_data['Country'] = top10_data['Country'].str.strip()

# Ülke isimlerini Türkçeleştir, yazım hatalarını da ekle
ulkeler_tr = {
    "United States": "Amerika Birleşik Devletleri",
    "China": "Çin",
    "India": "Hindistan",
    "Russia": "Rusya",
    "Japan": "Japonya",
    "Germany": "Almanya",
    "Canada": "Kanada",
    "Brazil": "Brezilya",
    "Brazi": "Brezilya",      # Yazım hatası için
    "France": "Fransa",
    "South Korea": "Güney Kore",
    "Japar": "Japonya"        # Yazım hatası için
}

top10_data['Country'] = top10_data['Country'].replace(ulkeler_tr)

# İstenilen sıralama için ülke listesi
ulke_sirasi = [
    'Çin',
    'Amerika Birleşik Devletleri',
    'Hindistan',
    'Rusya',
    'Japonya',
    'Kanada',
    'Brezilya',
    'Güney Kore',
    'Almanya',
    'Fransa'
]

# Ülkeleri istenilen sıraya göre sırala
top10_data['siralama'] = top10_data['Country'].map({ulke: i for i, ulke in enumerate(ulke_sirasi)})
top10_data = top10_data.sort_values('siralama')
top10_data = top10_data.drop('siralama', axis=1)

# Bar grafiği oluştur
fig = go.Figure()

# Üretim barları
fig.add_trace(go.Bar(
    y=top10_data['Country'],
    x=top10_data['Uretim'],
    name='Üretim',
    marker_color='blue',
    orientation='h'
))

# Tüketim barları
fig.add_trace(go.Bar(
    y=top10_data['Country'],
    x=top10_data['Tuketim'],
    name='Tüketim',
    marker_color='red',
    orientation='h'
))

# Grafik düzenini ayarla
fig.update_layout(
    barmode='group',
    title_text="2020 Yılı En Çok Elektrik Üreten ve Tüketen 10 Ülke",
    yaxis_title="Ülke",
    xaxis_title="Elektrik Miktarı (TWh)",
    height=800,
    width=1200,
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        autorange="reversed",
        tickfont=dict(size=12)
    )
)

# Grafiği kaydet ve göster
fig.write_html("top10_elektrik_uretim_tuketim.html")
fig.show()
