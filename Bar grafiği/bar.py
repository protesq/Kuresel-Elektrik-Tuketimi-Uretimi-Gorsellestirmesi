import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("Global Electricity Statistics.csv")

uretim_df = df[df['Features'] == 'net generation'].copy()
tuketim_df = df[df['Features'] == 'net consumption'].copy()

uretim_df['2020'] = pd.to_numeric(uretim_df['2020'], errors='coerce')
tuketim_df['2020'] = pd.to_numeric(tuketim_df['2020'], errors='coerce')

top10_uretim = uretim_df.nlargest(10, '2020')[['Country', '2020']]
top10_tuketim = tuketim_df.nlargest(10, '2020')[['Country', '2020']]

top10_uretim = top10_uretim.rename(columns={'2020': 'Uretim'})
top10_tuketim = top10_tuketim.rename(columns={'2020': 'Tuketim'})
top10_data = pd.merge(top10_uretim, top10_tuketim, on='Country', how='outer')

top10_data['Country'] = top10_data['Country'].str.strip()

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

fig.write_html("top10_elektrik_uretim_tuketim.html")
fig.show()
