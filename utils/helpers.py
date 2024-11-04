# utils/helpers.py

from rapidfuzz import process, fuzz

def fuzzy_match(name, name_list, threshold=90):
    """
    Perform fuzzy matching on a given name against a list of names.

    Args:
        name (str): The name to match.
        name_list (list): List of names to compare against.
        threshold (int): Similarity threshold for matching.

    Returns:
        tuple: Matched name and similarity score if above threshold, else (None, 0).
    """
    match, score, _ = process.extractOne(name, name_list, scorer=fuzz.ratio)
    if score >= threshold:
        return match, score
    return None, 0
