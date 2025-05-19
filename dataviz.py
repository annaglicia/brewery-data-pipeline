import pandas as pd
import streamlit as st

gold_layer_parquet_path = './airflow/db/gold_layer_data.parquet'

df_gold = pd.read_parquet(gold_layer_parquet_path)
st.write(df_gold)
