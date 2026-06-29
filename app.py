# app.py

import streamlit as st

from src.intent_parser import parse_user_query


st.set_page_config(page_title="Fashion Outfit Recommender", layout="wide")
st.title("AI Fashion Outfit Recommendation System")

query = st.text_input("Ask for an outfit", "I need an outfit for a business meeting.")
if query:
    profile = parse_user_query(query)
    st.json(profile)

    st.info("Next pipeline steps:")
    st.code(
        """
1. Parse query into structured profile
2. Apply metadata filters
3. Run dense retrieval
4. Run sparse retrieval
5. Fuse ranks with RRF
6. Assemble outfit by category slots
7. Score compatibility
8. Generate explanation
        """.strip(),
        language="text",
    )