import streamlit as st
import requests

st.set_page_config(page_title="Talent Scount")

left_co, cent_co,last_co = st.columns(3)
#st.title("TalentScout")

with cent_co:
      new_title = '<p style="font-family:fantasy; color:#DAA520; font-size: 42px;">TalentScout</p>'
      st.markdown(new_title, unsafe_allow_html=True)

api_key = st.secrets["google"]["api_key"]
cx = st.secrets["google"]["cx"]
queryx = st.text_input("Search Query",placeholder="Python Developer Bengaluru").strip()
query = f'site:linkedin.com/in "{queryx}"'

if st.button("Search"):
    if not api_key or not cx or not query:
        st.error("Please provide API Key, Search Engine ID, and Query")
    else:
        query = f'site:linkedin.com/in "{query}"'
        
        st.write("Searching for:", queryx)

        all_results = []
        for start in range(1, 101, 10): 
            params = {"key": api_key, "cx": cx, "q": query , "num": 10, "start": start}
            response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)

            if response.status_code == 429:
                 st.warning("Daily quota exceeded for the current API key. Try again tomorrow or use another key.")
                 break
            if response.status_code != 200:
                st.error(f"Error: {response.status_code} - {response.text}")
                break
            
            items = response.json().get("items", [])
            if not items:
                break  # No more results
            all_results.extend(items)

        if not all_results:
            st.warning("No results found")
        else:
            st.success(f"Found {len(all_results)} results for: {queryx}")
            for i, item in enumerate(all_results, start=1):
                st.subheader(f"{i}. {item.get('title')}")
                st.write(item.get("link"))
                snippet = item.get("snippet", "")
                if snippet:
                    st.write(snippet)
