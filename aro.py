import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load datasets (using recommended datasets from NASA's SEDAC and other sources)

# Load gender inequality index data from NASA SEDAC (assuming CSV files are available from NASA SEDAC)
gii_url = "https://sedac.ciesin.columbia.edu/downloads/data/undp-human-development-index/gender-inequality-index.csv"
gii_df = pd.read_csv(gii_url)

# Load climate vulnerability index data from NASA SEDAC
climate_vulnerability_url = "https://sedac.ciesin.columbia.edu/downloads/data/climate-vulnerability-index/climate-vulnerability-index.csv"
climate_vulnerability_df = pd.read_csv(climate_vulnerability_url)

# Merge datasets on country codes
df = pd.merge(gii_df, climate_vulnerability_df, left_on="Country Code", right_on="Country Code", how="inner")

# Filter the data to match the context of gender inequality and climate vulnerability
# Assume 'Gender Inequality Index' and 'Climate Vulnerability Index' are columns in the respective datasets

# Streamlit app layout
st.set_page_config(page_title="Gender Equality and Climate Action Dashboard", layout="wide")
st.title("Gender Equality and Climate Action Dashboard")

st.markdown("""
This dashboard showcases the relationship between gender inequality and climate change vulnerability.
Below, you can view various visualizations for all countries at once.
""")

# Choropleth map to show gender inequality index
fig_gii = px.choropleth(
    df,
    locations="Country Code",
    color="Gender Inequality Index",
    hover_name="Country Name",
    title="Gender Inequality Index by Country",
    labels={"Gender Inequality Index": "Gender Inequality Index"},
    color_continuous_scale=px.colors.sequential.Sunset
)
fig_gii.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, geo=dict(showframe=False, showcoastlines=True))
st.plotly_chart(fig_gii, use_container_width=True)

# Choropleth map to show climate vulnerability index
fig_cvi = px.choropleth(
    df,
    locations="Country Code",
    color="Climate Vulnerability Index",
    hover_name="Country Name",
    title="Climate Vulnerability Index by Country",
    labels={"Climate Vulnerability Index": "Climate Vulnerability Index"},
    color_continuous_scale=px.colors.sequential.Plasma
)
fig_cvi.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, geo=dict(showframe=False, showcoastlines=True))
st.plotly_chart(fig_cvi, use_container_width=True)

# Time-series analysis for labor hours by women (placeholder for all countries)
st.subheader("Increasing Labor Hours for Women Over Time (Placeholder Data)")
years = ['2018', '2019', '2020', '2021', '2022']
fig = go.Figure()
for country in df['Country Name'].unique():
    labor_hours = [2, 3, 4, 5, 7]  # Placeholder data
    fig.add_trace(go.Scatter(
        x=years,
        y=labor_hours,
        mode='lines+markers',
        name=country,
        line=dict(width=2),
        marker=dict(size=6)
    ))
fig.update_layout(
    xaxis={'title': 'Year'},
    yaxis={'title': 'Labor Hours (in millions)'},
    margin={"r":0,"t":50,"l":0,"b":0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(fig, use_container_width=True)

# Bar chart for economic impact for all countries
st.subheader("Economic Impact by Country")
bar_fig = px.bar(
    df,
    x='Country Name',
    y='GDP (Billions)',
    title='Economic Impact by Country',
    labels={'GDP (Billions)': 'GDP (Billions)', 'Country Name': 'Country'},
    color='GDP (Billions)',
    color_continuous_scale='Bluered'
)
bar_fig.update_layout(
    yaxis=dict(range=[0, 2000]),
    margin={"r":0,"t":50,"l":0,"b":0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(bar_fig, use_container_width=True)

# Climate Vulnerability Index chart for all countries
st.subheader("Climate Vulnerability Index by Country")
vuln_fig = px.bar(
    df,
    x='Country Name',
    y='Climate Vulnerability Index',
    title='Climate Vulnerability Index by Country',
    labels={'Climate Vulnerability Index': 'Climate Vulnerability Index', 'Country Name': 'Country'},
    color='Climate Vulnerability Index',
    color_continuous_scale='Viridis'
)
vuln_fig.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(vuln_fig, use_container_width=True)

# Key Performance Indicators (KPIs) for all countries
st.sidebar.subheader("Key Performance Indicators (Global)")
avg_gii = df['Gender Inequality Index'].mean()
avg_cvi = df['Climate Vulnerability Index'].mean()
st.sidebar.metric(label="Average Gender Inequality Index", value=f"{avg_gii:.2f}")
st.sidebar.metric(label="Average Climate Vulnerability Index", value=f"{avg_cvi:.2f}")

# Add country comparison section
st.markdown("## Country Comparison")
comparison_countries = st.multiselect("Select Countries to Compare", df['Country Name'].unique(), default=df['Country Name'].unique())
comparison_df = df[df['Country Name'].isin(comparison_countries)]

# Comparison Bar Chart
st.subheader("Comparison of Gender Inequality and Climate Vulnerability Indices")
comparison_fig = px.bar(
    comparison_df,
    x='Country Name',
    y=['Gender Inequality Index', 'Climate Vulnerability Index'],
    barmode='group',
    title='Comparison of Gender Inequality and Climate Vulnerability Indices by Country',
    labels={'value': 'Index Value', 'Country Name': 'Country', 'variable': 'Index Type'},
    color_discrete_map={'Gender Inequality Index': 'orange', 'Climate Vulnerability Index': 'purple'}
)
comparison_fig.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(comparison_fig, use_container_width=True)

# Conclusion
st.markdown("### Conclusion")
st.markdown("This dashboard provides insights into the intersection between gender inequality and climate vulnerability. By exploring country-specific data, we can identify regions where action is needed most, and compare performance across different metrics.")