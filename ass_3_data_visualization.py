import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

try:
    df = pd.read_csv("covid_19_clean_complete.csv")
except FileNotFoundError:
    st.error("Dataset 'covid_19_clean_complete.csv' not found. Please upload the file.")
    st.stop()

if 'Country/Region' not in df.columns:
    st.error(f"Column 'Country/Region' not found. Available columns: {df.columns.tolist()}")
    st.stop()
else:
    df.rename(columns={'Country/Region': 'Country_Region'}, inplace=True)

required_columns = ['density', 'avgtemp', 'avghumidity', 'sexratio', 'days_from_firstcase']
for col in required_columns:
    if col not in df.columns:
        st.warning(f"Column '{col}' not found in dataset. Some visualizations may not work. Available columns: {df.columns.tolist()}")

st.title("COVID-19 Interactive Dashboard")
st.markdown("An interactive dashboard to explore COVID-19 and demographic data")

st.sidebar.header("Filter Options")
countries = df['Country_Region'].unique()
selected_country = st.sidebar.selectbox("Select a Country", sorted(countries))

show_density = st.sidebar.checkbox("Show Population Density Distribution")
show_temp_humidity = st.sidebar.checkbox("Show Temperature vs Humidity")
show_days_dist = st.sidebar.checkbox("Show Days from First Case Histogram")

filtered_df = df[df['Country_Region'] == selected_country]

st.subheader(f"Summary Statistics for {selected_country}")
if {'density', 'avgtemp', 'avghumidity'}.issubset(filtered_df.columns):
    st.write(filtered_df[['density', 'avgtemp', 'avghumidity']].describe())
else:
    st.warning("Some columns (density, avgtemp, avghumidity) are missing in the dataset.")

st.subheader("Line Chart: Average Temperature Over Time")
if 'Date' in filtered_df.columns and 'avgtemp' in filtered_df.columns:
    line_data = filtered_df[['Date', 'avgtemp']].copy()
    line_data['Date'] = pd.to_datetime(line_data['Date'], errors='coerce')
    line_data = line_data.dropna().sort_values('Date')
    if not line_data.empty:
        st.line_chart(line_data.set_index('Date')['avgtemp'])
    else:
        st.warning("No valid data available for the line chart.")
else:
    st.warning("Required columns (Date, avgtemp) are missing for the line chart.")

st.subheader("Pie Chart: Approximate Gender Distribution")
if 'sexratio' in filtered_df.columns:
    male_ratio = filtered_df['sexratio'].mean() / (1 + filtered_df['sexratio'].mean())
    female_ratio = 1 - male_ratio
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(
        [male_ratio, female_ratio],
        labels=["Male", "Female"],
        autopct='%1.1f%%',
        colors=["lightblue", "pink"]
    )
    st.pyplot(fig_pie)
    plt.close(fig_pie)
else:
    st.warning("Column 'sexratio' is missing for the pie chart.")

if show_density and 'density' in filtered_df.columns:
    st.subheader("Population Density Distribution")
    fig1, ax1 = plt.subplots()
    sns.histplot(filtered_df['density'], bins=20, ax=ax1, color="green")
    ax1.set_xlabel("Population Density")
    ax1.set_ylabel("Count")
    st.pyplot(fig1)
    plt.close(fig1)
elif show_density:
    st.warning("Column 'density' is missing for the density distribution.")

if show_temp_humidity and {'avgtemp', 'avghumidity'}.issubset(filtered_df.columns):
    st.subheader("Scatter Plot: Temperature vs Humidity")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(data=filtered_df, x='avgtemp', y='avghumidity', ax=ax2)
    ax2.set_xlabel("Average Temperature")
    ax2.set_ylabel("Average Humidity")
    st.pyplot(fig2)
    plt.close(fig2)
elif show_temp_humidity:
    st.warning("Columns 'avgtemp' or 'avghumidity' are missing for the scatter plot.")

if show_days_dist and 'days_from_firstcase' in filtered_df.columns:
    st.subheader("Histogram: Days from First Case")
    fig3, ax3 = plt.subplots()
    sns.histplot(filtered_df['days_from_firstcase'], bins=30, ax=ax3, color="orange")
    ax3.set_xlabel("Days from First Case")
    ax3.set_ylabel("Count")
    st.pyplot(fig3)
    plt.close(fig3)
elif show_days_dist:
    st.warning("Column 'days_from_firstcase' is missing for the histogram.")

# Footer
st.markdown("---")
st.markdown("Dashboard created using *Streamlit* and *Seaborn*")