import streamlit as st
st.set_page_config(layout="wide")
from app.matchingO import ontologyMatching
from app.matchingR import referentialMatching

def main():
    st.sidebar.title("Arianne Demo")
    st.sidebar.image("app/ressources/logoMM.png")
    
    page_selector = st.sidebar.selectbox("Choisissez une page:", ["Choisissez une page","Interface Ontologie",  "Interface Référentiel"],label_visibility="collapsed")
    st.sidebar.divider()
    # Direct to the appropriate page
    if page_selector == "Interface Ontologie":
        ontologyMatching()
    elif page_selector == "Interface Référentiel":
        referentialMatching()


    
       
if __name__ == "__main__":
    main()
