# processing/comparator.py

import pandas as pd
from utils.helpers import fuzzy_match

def compare_restaurants(noon_data, talabat_data, threshold=90):
    """
    Compare restaurant data from Noon Food and Talabat UAE.

    Args:
        noon_data (list): List of restaurants from Noon Food.
        talabat_data (list): List of restaurants from Talabat UAE.
        threshold (int): Similarity threshold for fuzzy matching.

    Returns:
        dict: Dictionary containing matched, noon_only, and talabat_only dataframes.
    """
    noon_df = pd.DataFrame(noon_data)
    talabat_df = pd.DataFrame(talabat_data)
    
    noon_names = noon_df['name'].tolist()
    talabat_names = talabat_df['name'].tolist()
    
    matched = []
    noon_only = []
    talabat_only = []
    
    # Create a copy of Talabat data to track unmatched entries
    talabat_unmatched = talabat_df.copy()
    
    for index, noon_row in noon_df.iterrows():
        match, score = fuzzy_match(noon_row['name'], talabat_names, threshold)
        if match:
            talabat_offer = talabat_df[talabat_df['name'] == match]['offer'].values[0]
            matched.append({
                'name_noon': noon_row['name'],
                'offer_noon': noon_row['offer'],
                'name_talabat': match,
                'offer_talabat': talabat_offer,
                'similarity': score
            })
            # Remove the matched Talabat entry to prevent duplicate matches
            talabat_unmatched = talabat_unmatched[talabat_unmatched['name'] != match]
        else:
            noon_only.append({
                'name_noon': noon_row['name'],
                'offer_noon': noon_row['offer']
            })
    
    # Remaining Talabat entries are unmatched
    for index, talabat_row in talabat_unmatched.iterrows():
        talabat_only.append({
            'name_talabat': talabat_row['name'],
            'offer_talabat': talabat_row['offer']
        })
    
    matched_df = pd.DataFrame(matched)
    noon_only_df = pd.DataFrame(noon_only)
    talabat_only_df = pd.DataFrame(talabat_only)
    
    return {
        'matched': matched_df,
        'noon_only': noon_only_df,
        'talabat_only': talabat_only_df
    }
