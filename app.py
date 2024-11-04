# app.py

import streamlit as st
from scraping.noon_scraper import scrape_noon_food
from scraping.talabat_scraper import scrape_talabat
from processing.comparator import compare_restaurants
from exporting.google_sheets_exporter import export_to_google_sheets

def main():
    st.set_page_config(page_title="Restaurant Listings Comparator", layout="wide")
    st.title("🍽️ Restaurant Listings Comparison Tool")
    
    st.markdown("""
    This tool compares restaurant listings between [Noon Food](https://food.noon.com/) and [Talabat UAE](https://www.talabat.com/uae).
    Enter the area name and click "Compare" to fetch and compare the data.
    """)
    
    # Input field for area name
    area = st.text_input("Enter the area name (e.g., dubai-marina):", value="")
    
    # Trigger button
    if st.button("Compare"):
        if not area:
            st.error("Please enter an area name.")
            st.stop()
        
        with st.spinner("Scraping data from Noon Food..."):
            noon_data = scrape_noon_food(area)
            if not noon_data:
                st.warning("No data found for Noon Food.")
        
        with st.spinner("Scraping data from Talabat UAE..."):
            talabat_data = scrape_talabat(area)
            if not talabat_data:
                st.warning("No data found for Talabat UAE.")
        
        if not noon_data and not talabat_data:
            st.error("No data fetched from both platforms. Please check the area name and try again.")
            st.stop()
        
        with st.spinner("Comparing data..."):
            comparison_results = compare_restaurants(noon_data, talabat_data)
        
        with st.spinner("Exporting results to Google Sheets..."):
            export_to_google_sheets(comparison_results['matched'], 'Matched')
            export_to_google_sheets(comparison_results['noon_only'], 'Noon Only')
            export_to_google_sheets(comparison_results['talabat_only'], 'Talabat Only')
        
        st.success("✅ Comparison complete and results exported to Google Sheets.")
        
        # Display results in the app
        st.subheader("📊 Matched Restaurants")
        if not comparison_results['matched'].empty:
            st.dataframe(comparison_results['matched'])
        else:
            st.info("No matched restaurants found.")
        
        st.subheader("📌 Restaurants Only on Noon Food")
        if not comparison_results['noon_only'].empty:
            st.dataframe(comparison_results['noon_only'])
        else:
            st.info("No exclusive restaurants on Noon Food.")
        
        st.subheader("📌 Restaurants Only on Talabat UAE")
        if not comparison_results['talabat_only'].empty:
            st.dataframe(comparison_results['talabat_only'])
        else:
            st.info("No exclusive restaurants on Talabat UAE.")

if __name__ == "__main__":
    main()
