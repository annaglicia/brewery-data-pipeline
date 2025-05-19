import pandas as pd
import streamlit as st

bronze_layer_parquet_path = './airflow/db/bronze_layer_data.json'

st.title("Brewery Report in the United States")

st.write("The data for this report was extracted " \
        "from the Open Brewery DB API. Below are the raw " \
        "data provided by the API, filtered to the United States.")

df_silver = pd.read_parquet('./airflow/db/silver_layer_data.parquet')
st.dataframe(df_silver)

st.subheader("Data grouped by city and brewery type")
df_gold_city = pd.read_parquet('./airflow/db/gold_layer_data/city_type_grouped_data.parquet')
st.dataframe(df_gold_city)

st.subheader("Number of breweries by state")
df_gold_state = pd.read_parquet('./airflow/db/gold_layer_data/state_grouped_data.parquet')
st.dataframe(df_gold_state)
st.bar_chart(df_gold_state)

st.subheader("Types of breweries in the country")
df_gold_type = pd.read_parquet('./airflow/db/gold_layer_data/type_grouped_data.parquet')
st.dataframe(df_gold_type)
st.bar_chart(df_gold_type)
