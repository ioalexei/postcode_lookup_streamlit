def geocode_crown_dependencies(postcodes_list=[]): 
    """Geocodes postcodes in UK Crown Dependencies: Channel Islands and Isle of Man

    Arguments: 
    - postcodes_list -- a list of postcodes 
    """
    import re
    import pandas as pd
    # open the geocoding CSV - must be in the same directory as the script. 
    postcode_ref = pd.read_csv("./data/crown_dependencies_geocoding.csv")
    # Make a list of regex patterns from the column in the spreadsheet
    regexes = postcode_ref['Regex']
    # Turn these into a list of `re` regex queries 
    reg_list = []
    for i in regexes.values: reg_list.append(re.compile(i))
    # create an empy dict to hold the geocoding results (is this better as a df? it's easy to swap)
    results_dict = {}
    # for each postcode, run each regex query in turn until there is a match. When there is a match, add the lat, long and parish name to the results dict. 
    for i in postcodes_list: 
        for j in reg_list: 
            result = re.search(j, i)
            if  result == None: 
                pass
            else: 
                results_dict[i] = result.re.pattern
                results_dict[i] = {'lat': postcode_ref.loc[postcode_ref["Regex"] == j.pattern].Lat.values[0], 
                                   'long': postcode_ref.loc[postcode_ref["Regex"] == j.pattern].Long.values[0]
                                   }
    geocoded_df = pd.DataFrame(results_dict).T
    return geocoded_df