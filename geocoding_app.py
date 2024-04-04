import pandas as pd
import numpy as np
import streamlit as st
import time

st.title('Postcode lookup')
#st.write("If entering multiple postcodes, add one per line")

if 'input' not in st.session_state:
    st.session_state.input = ''

text_input = st.text_area(label="Enter postcodes", placeholder="Add one postcode per line")

text_split = text_input.splitlines()

query_list = []

for i in text_split: 
    query_list.append(i.strip())

# if text_input:
#     st.session_state.input = query_list

# strip whitespace and force uppercase 
#text_input = text_input.upper().replace(" ", "")

if st.button(label="Geocode", type="primary"): 
    if len(query_list) > 0: 
        with st.spinner('Loading data ...'):
        # if PCD starts with GY, JE, IM
        # load alt sources
        # display message about accuracy 
            df = pd.read_feather('./data/onspd_nov2023.feather')
            df = df[['pcds', 'lat', 'long']]
            # results = df[df.pcds.isin(query_list)]
            results = pd.DataFrame(query_list).rename(columns={0: 'pcds'}).merge(df, how='left') # this is slower but preserves the input order 
            if len(results) < 2: 
                results_title = "# Search result"
            else: 
                results_title = "# Search results"
    else: 
        st.write("No query entered")


    if len(results)> 0: 
        # TODO: Report how many records were matched out of how many inputs 
        st.markdown(results_title)
        st.dataframe(results, hide_index=True, use_container_width=True)
        st.write("_Select cells to copy and paste or click the download icon to download as CSV_")
    else:
        st.markdown(results_title)
        st.write("No match found")
