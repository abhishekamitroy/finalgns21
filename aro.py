import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Use local file paths after uploading the datasets
gii_file_path = "gender_inequality_index.csv"  # Update with the actual uploaded file path
climate_vulnerability_file_path = "climate_vulnerability_index.csv"  # Update with the actual uploaded file path

# Load datasets
gii_df = pd.read_csv(gii_file_path)
climate_vulnerability_df = pd.read_csv(climate_vulnerability_file_path)

# Merge datasets on country codes
df = pd.merge(gii_df, climate_vulnerability_df, left_on="Country Code", right_on="Country Code", how="inner")

# Streamlit app layout and visualization (same as before)
st.set_page_config(page_title="Gender Equality and Climate Action Dashboard", layout="wide")
st.title("Gender Equality and Climate Action Dashboard")

st.markdown("""
This dashboard showcases the relationship between gender inequality and climate change vulnerability.
Select a country from the dropdown menu to view more detailed data.
""")

# Sidebar for country selection
dropdown_options = df['Country Name'].unique()
selected_country = st.sidebar.selectbox("Select a Country", dropdown_options)
filtered_df = df[df['Country Name'] == selected_country] if selected_country else df

# Add more interactive elements in sidebar
st.sidebar.markdown("### Filter Options")
show_gii = st.sidebar.checkbox("Show Gender Inequality Index", True)
show_cvi = st.sidebar.checkbox("Show Climate Vulnerability Index", True)

# Choropleth map to show gender inequality index
if show_gii:
    fig_gii = px.choropleth(
        df,
        locations="Country Code",
        color="Gender Inequality Index",
        hover_name="Country Name",
        title="Gender Inequality Index by Country",
        labels={"Gender Inequality Index": "Gender Inequality Index"},
        color_continuous_scale=px.colors.sequential.Sunset
    )
    fig_gii.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0}, geo=dict(showframe=False, showcoastlines=True))
    st.plotly_chart(fig_gii, use_container_width=True)

# Choropleth map to show climate vulnerability index
if show_cvi:
    fig_cvi = px.choropleth(
        df,
        locations="Country Code",
        color="Climate Vulnerability Index",
        hover_name="Country Name",
        title="Climate Vulnerability Index by Country",
        labels={"Climate Vulnerability Index": "Climate Vulnerability Index"},
        color_continuous_scale=px.colors.sequential.Plasma
    )
    fig_cvi.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0}, geo=dict(showframe=False, showcoastlines=True))
    st.plotly_chart(fig_cvi, use_container_width=True)

# Time-series analysis for labor hours by women
st.subheader(f"Increasing Labor Hours for Women Over Time - {selected_country}")
years = ['2018', '2019', '2020', '2021', '2022']
labor_hours = [2, 3, 4, 5, 7]  # Placeholder data
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=years,
    y=labor_hours,
    mode='lines+markers',
    name='Labor Hours by Women',
    line=dict(color='#2980B9', width=3),
    marker=dict(size=8)
))
fig.update_layout(
    xaxis={'title': 'Year'},
    yaxis={'title': 'Labor Hours (in millions)'},
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(fig, use_container_width=True)

# Bar chart for economic impact
st.subheader(f"Economic Impact by Country - {selected_country}")
bar_fig = px.bar(
    filtered_df,
    x='Country Name',
    y='GDP (Billions)',
    title='Economic Impact by Country',
    labels={'GDP (Billions)': 'GDP (Billions)', 'Country Name': 'Country'},
    color='GDP (Billions)',
    color_continuous_scale='Bluered'
)
bar_fig.update_layout(
    yaxis=dict(range=[0, 2000]),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(bar_fig, use_container_width=True)

# Climate Vulnerability Index chart
st.subheader(f"Climate Vulnerability Index by Country - {selected_country}")
vuln_fig = px.bar(
    filtered_df,
    x='Country Name',
    y='Climate Vulnerability Index',
    title='Climate Vulnerability Index by Country',
    labels={'Climate Vulnerability Index': 'Climate Vulnerability Index', 'Country Name': 'Country'},
    color='Climate Vulnerability Index',
    color_continuous_scale='Viridis'
)
vuln_fig.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(vuln_fig, use_container_width=True)

# Key Performance Indicators (KPIs)
st.sidebar.subheader("Key Performance Indicators")
avg_gii = filtered_df['Gender Inequality Index'].mean()
avg_cvi = filtered_df['Climate Vulnerability Index'].mean()
st.sidebar.metric(label="Average Gender Inequality Index", value=f"{avg_gii:.2f}")
st.sidebar.metric(label="Average Climate Vulnerability Index", value=f"{avg_cvi:.2f}")

# Add country comparison section
st.markdown("## Country Comparison")
comparison_countries = st.multiselect("Select Countries to Compare", df['Country Name'].unique(), default=[selected_country])
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
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(comparison_fig, use_container_width=True)

# Conclusion
st.markdown("### Conclusion")
st.markdown("This dashboard provides insights into the intersection between gender inequality and climate vulnerability. By exploring country-specific data, we can identify regions where action is needed most, and compare performance across different metrics.")
