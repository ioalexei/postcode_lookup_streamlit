import pandas as pd
import numpy as np
import streamlit as st
import time

st.title('Postcode lookup')
#st.write("If entering multiple postcodes, add one per line")

if 'input' not in st.session_state:
    st.session_state.input = ''

text_input = st.text_area(label="Enter a postcode", placeholder="Add one postcode per line")

text_split = text_input.splitlines()

query_list = []

for i in text_split: 
    query_list.append(i.strip())

#if text_input:
#    st.session_state.input = query_list

# strip whitespace and force uppercase 
#text_input = text_input.upper().replace(" ", "")

if st.button(label="Geocode", type="primary"): 
    st.markdown("# Search result")

    # if PCD starts with GY, JE, IM
    # load alt sources
    # display message about accuracy 

    df = pd.read_feather('./data/onspd_nov2023.feather')

    if df.pcds.isin(query_list).any(): 
        st.dataframe(df[df.pcds.isin(query_list)], hide_index=True, use_container_width=True)
    else:
        st.write("No match found")
