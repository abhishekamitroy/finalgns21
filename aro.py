import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Streamlit app layout
st.set_page_config(page_title="Gender Equality and Climate Action Dashboard", layout="wide")
st.title("Gender Equality and Climate Action Dashboard")

st.markdown("""
This dashboard showcases the relationship between gender inequality and climate change vulnerability.
Upload the dataset and select a country from the dropdown menu to view more detailed data.
""")

# File uploader for the dataset
uploaded_file = st.file_uploader("Upload the Rural Access Index CSV file", type="csv")

if uploaded_file is not None:
    # Load datasets
    # Dataset 1: Rural Access Index from SEDAC (uploaded by user)
    rai_df = pd.read_csv(uploaded_file)

    # Rename column for merging consistency
    rai_df.rename(columns={'NAME_0': 'Country', 'ISO3': 'Country Code', 'SDG911pct': 'Rural Access Index (RAI)'}, inplace=True)

    # Ensure the 'Country' column exists and remove unnecessary columns
    rai_df = rai_df[['Country', 'Rural Access Index (RAI)', 'Country Code']]

    # Dataset 2: Climate Vulnerability Index
    climate_vulnerability_data = {
        "Country": ["Kenya", "India", "Brazil", "China", "USA"],
        "Climate Vulnerability Index": [8.2, 6.7, 7.0, 8.0, 7.5]
    }
    climate_vulnerability_df = pd.DataFrame(climate_vulnerability_data)

    # Dataset 3: Gender Inequality Index (Dummy Data for Example)
    gii_data = {
        "Country": ["Kenya", "India", "Brazil", "China", "USA"],
        "Gender Inequality Index": [0.55, 0.49, 0.42, 0.38, 0.27]
    }
    gii_df = pd.DataFrame(gii_data)

    # Merge datasets for easier comparison
    df = pd.merge(gii_df, climate_vulnerability_df, on="Country")
    df = pd.merge(df, rai_df, on="Country", how="inner")

    # Sidebar for country selection
    selected_country = st.sidebar.selectbox("Select a Country", df['Country'].unique())
    selected_metric = st.sidebar.radio("Select Metric to Highlight:", [
        'Climate Vulnerability Index',
        'Gender Inequality Index',
        'Rural Access Index (RAI)'
    ])

    # Plot 1: Climate Vulnerability Index by Country
    fig_vulnerability = px.bar(
        df,
        x='Country',
        y='Climate Vulnerability Index',
        title='Climate Vulnerability Index by Country',
        labels={'Climate Vulnerability Index': 'Climate Vulnerability Index', 'Country': 'Country'},
        color='Climate Vulnerability Index',
        color_continuous_scale=px.colors.sequential.Blues
    )
    fig_vulnerability.update_traces(
        marker=dict(opacity=[0.3 if country != selected_country else 1.0 for country in df['Country']], line=dict(width=2)),
        selector=dict(type='bar')
    )
    fig_vulnerability.update_layout(
        template='plotly_dark',
        xaxis_tickangle=-45,
        hovermode='x unified',
        font=dict(family='Roboto, sans-serif', color='#ffffff', size=20),
        plot_bgcolor='#1f2c56',
        paper_bgcolor='#1f2c56',
        title_font=dict(size=30),
        legend_font=dict(size=22),
        coloraxis_colorbar=dict(title_font=dict(size=24), tickfont=dict(size=20))
    )

    st.plotly_chart(fig_vulnerability, use_container_width=True)

    # Plot 2: Gender Inequality Index by Country
    fig_gender_inequality = px.bar(
        df,
        x='Country',
        y='Gender Inequality Index',
        title='Gender Inequality Index by Country',
        labels={'Gender Inequality Index': 'Gender Inequality Index', 'Country': 'Country'},
        color='Gender Inequality Index',
        color_continuous_scale=px.colors.sequential.Peach
    )
    fig_gender_inequality.update_traces(
        marker=dict(opacity=[0.3 if country != selected_country else 1.0 for country in df['Country']], line=dict(width=2)),
        selector=dict(type='bar')
    )
    fig_gender_inequality.update_layout(
        template='plotly_dark',
        xaxis_tickangle=-45,
        hovermode='x unified',
        font=dict(family='Roboto, sans-serif', color='#ffffff', size=20),
        plot_bgcolor='#1f2c56',
        paper_bgcolor='#1f2c56',
        title_font=dict(size=28),
        legend_font=dict(size=20),
        coloraxis_colorbar=dict(title_font=dict(size=22), tickfont=dict(size=18))
    )

    st.plotly_chart(fig_gender_inequality, use_container_width=True)

    # Plot 3: Rural Access Index by Country (Percentage of Population with Access to Roads)
    fig_rural_access = px.choropleth(
        df,
        locations="Country Code",
        color=selected_metric,
        hover_name="Country",
        title=f"{selected_metric} by Country",
        labels={selected_metric: selected_metric},
        color_continuous_scale=px.colors.sequential.Plasma
    )
    fig_rural_access.update_layout(
        template='plotly_dark',
        geo=dict(showframe=False, showcoastlines=True),
        font=dict(family='Roboto, sans-serif', color='#ffffff', size=16),
        plot_bgcolor='#1f2c56',
        paper_bgcolor='#1f2c56',
        title_font=dict(size=24),
        legend_font=dict(size=16),
        coloraxis_colorbar=dict(title_font=dict(size=18), tickfont=dict(size=14))
    )

    st.plotly_chart(fig_rural_access, use_container_width=True)

    # Plot 4: Relationship between Gender Inequality and Climate Vulnerability
    fig_relationship = px.scatter(
        df,
        x='Gender Inequality Index',
        y='Climate Vulnerability Index',
        color='Country',
        title='Relationship between Gender Inequality Index and Climate Vulnerability Index',
        labels={'Gender Inequality Index': 'Gender Inequality Index', 'Climate Vulnerability Index': 'Climate Vulnerability Index'},
        size_max=15,
        color_continuous_scale='Plasma'
    )
    fig_relationship.update_traces(marker=dict(size=15, opacity=0.8, line=dict(width=3, color='DarkSlateGrey')))
    fig_relationship.update_layout(
        template='plotly_dark',
        hovermode='closest',
        font=dict(family='Roboto, sans-serif', color='#ffffff', size=16),
        plot_bgcolor='#1f2c56',
        paper_bgcolor='#1f2c56',
        title_font=dict(size=24),
        legend_font=dict(size=16),
        coloraxis_colorbar=dict(title_font=dict(size=18), tickfont=dict(size=14))
    )

    st.plotly_chart(fig_relationship, use_container_width=True)

    # Placeholder data: Time spent collecting water and distance
    water_collection_data = {
        "Country": ["Kenya", "India", "Brazil", "China", "USA"],
        "Time Spent Collecting Water (hrs/week)": [15, 12, 10, 8, 6],
        "Average Distance to Water Source (km)": [4.5, 3.8, 2.9, 2.5, 1.8]
    }
    water_df = pd.DataFrame(water_collection_data)

    # Scatter Plot for Water Collection
    fig_water_collection = px.scatter(
        water_df,
        x='Average Distance to Water Source (km)',
        y='Time Spent Collecting Water (hrs/week)',
        color='Country',
        size='Time Spent Collecting Water (hrs/week)',
        title='Water Collection Efforts by Country',
        labels={
            'Average Distance to Water Source (km)': 'Average Distance to Water Source (km)',
            'Time Spent Collecting Water (hrs/week)': 'Time Spent Collecting Water (hrs/week)'
        }
    )
    fig_water_collection.update_traces(marker=dict(symbol='diamond', size=20, opacity=0.8))
    fig_water_collection.update_layout(
        template='plotly_dark',
        hovermode='closest',
        font=dict(family='Roboto, sans-serif', color='#ffffff', size=16),
        plot_bgcolor='#1f2c56',
        paper_bgcolor='#1f2c56',
        title_font=dict(size=24),
        legend_font=dict(size=16),
        coloraxis_colorbar=dict(title_font=dict(size=18), tickfont=dict(size=14))
    )

    st.plotly_chart(fig_water_collection, use_container_width=True)
else:
    st.warning("Please upload the Rural Access Index CSV file to proceed.")