import pandas as pd
import streamlit as st
from crown_dependencies import geocode_crown_dependencies as gcd

st.title('Postcode lookup')
#st.write("If entering multiple postcodes, add one per line")

if 'input' not in st.session_state:
    st.session_state.input = ''

text_input = st.text_area(label="Enter postcodes", placeholder="Add one postcode per line")

text_split = text_input.splitlines()

query_list = []

for i in text_split: 
    query_list.append(i.upper().strip())

crown_dep_pcds = ('JE', 'GY', 'IM')

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
            # process crown dependencies 
            df_crown_deps = results[results.pcds.str.startswith(crown_dep_pcds)]
            results_no_cd = results[~results.pcds.str.startswith(crown_dep_pcds)]
            df_crown_deps_gcd = gcd(list(df_crown_deps.pcds.values))
            df_crown_deps_gcd = df_crown_deps_gcd.reset_index().rename(columns={'index':'pcds'})
            results = pd.concat([results_no_cd, df_crown_deps_gcd])
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
        if results.pcds.str.startswith(crown_dep_pcds).any(): 
            st.write("Note: `GY`, `JE` and `IM` postcode locations are only approximate, accurate to the district level")
    else:
        st.markdown(results_title)
        st.write("No match found")


st.write("Data source: Office for National Statistics licensed under the [Open Government Licence v.3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)")
