import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('Global Electricity Statistics.csv')

production = df[df['Features'] == 'net generation']
consumption = df[df['Features'] == 'net consumption']

production_2020 = production[['Country', 'Region', '2020']].rename(columns={'2020': 'Production_2020'})
consumption_2020 = consumption[['Country', 'Region', '2020']].rename(columns={'2020': 'Consumption_2020'})

merged_df = pd.merge(production_2020, consumption_2020, on=['Country', 'Region'], how='inner')

merged_df = merged_df.dropna()

merged_df = merged_df.replace('--', np.nan).dropna()

merged_df['Production_2020'] = pd.to_numeric(merged_df['Production_2020'], errors='coerce')
merged_df['Consumption_2020'] = pd.to_numeric(merged_df['Consumption_2020'], errors='coerce')
merged_df = merged_df.dropna()

region_map = {
    'Africa': 'Afrika',
    'Asia & Oceania': 'Asya & Okyanusya',
    'Central & South America': 'Orta & Güney Amerika',
    'Eurasia': 'Avrasya',
    'Europe': 'Avrupa',
    'Middle East': 'Orta Doğu',
    'North America': 'Kuzey Amerika'
}

merged_df['Region_TR'] = merged_df['Region'].map(region_map)

region_data = merged_df.groupby('Region_TR').agg({
    'Production_2020': 'sum',
    'Consumption_2020': 'sum'
}).reset_index()

region_data['Energy_Balance'] = region_data['Production_2020'] - region_data['Consumption_2020']

fig = px.scatter(
    region_data,
    x='Consumption_2020',
    y='Production_2020',
    size='Production_2020',
    color='Region_TR',
    hover_name='Region_TR',
    hover_data={
        'Region_TR': True,
        'Production_2020': ':.2f',
        'Consumption_2020': ':.2f',
        'Energy_Balance': ':.2f'
    },
    labels={
        'Consumption_2020': 'Elektrik Tüketimi (2020, TWh)',
        'Production_2020': 'Elektrik Üretimi (2020, TWh)',
        'Region_TR': 'Kıta/Bölge'
    },
    title='Kıta/Bölgelere Göre Elektrik Üretimi ve Tüketimi (2020)',
    template='plotly_white'
)

max_val = max(region_data['Production_2020'].max(), region_data['Consumption_2020'].max())
fig.add_shape(
    type='line',
    x0=0, y0=0,
    x1=max_val, y1=max_val,
    line=dict(color='gray', dash='dash')
)

fig.update_layout(
    width=800,
    height=600,
    xaxis_title='Elektrik Tüketimi (2020, TWh)',
    yaxis_title='Elektrik Üretimi (2020, TWh)',
    legend_title='Kıta/Bölge',
    plot_bgcolor='white',
    paper_bgcolor='white'
)

fig.write_html("bolge_elektrik_uretim_tuketim.html")
fig.show()
