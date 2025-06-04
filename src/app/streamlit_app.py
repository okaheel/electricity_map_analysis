import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="EIA-930 Hourly Data Preview", layout="wide")
st.title("EIA-930 Hourly Data Preview for CA, TX, VA")

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/parquet')

state_files = {
    'California (CA)': 'eia930_hourly_CA.parquet',
    'Texas (TX)': 'eia930_hourly_TX.parquet',
    'Virginia (VA)': 'eia930_hourly_VA.parquet',
}

for state, fname in state_files.items():
    st.header(state)
    fpath = os.path.join(DATA_PATH, fname)
    if os.path.exists(fpath):
        df = pd.read_parquet(fpath)
        st.write(f"Rows: {len(df):,}")
        # Show min/max timestamp
        if 'period' in df.columns:
            min_ts = df['period'].min()
            max_ts = df['period'].max()
            st.info(f"Earliest timestamp: {min_ts}")
            st.info(f"Latest timestamp: {max_ts}")
        st.dataframe(df.head(100))
        with st.expander("Show all columns"):
            st.write(list(df.columns))
        with st.expander("Show sample statistics"):
            st.write(df.describe(include='all'))
    else:
        st.warning(f"File not found: {fname}")
