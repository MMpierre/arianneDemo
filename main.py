import streamlit as st
st.set_page_config(layout="wide")
from app.matchingO import ontologyMatching
from app.matchingR import referentialMatching

def main():
    st.sidebar.title("ARIANE Interoperability")
    st.sidebar.image("app/ressources/logoMM.png")
    st.sidebar.divider()
    l,r = st.sidebar.columns(2)
    if "selector" not in st.session_state:
        st.session_state.selector = ""
    if l.button("Ontology Mapping",use_container_width=True): st.session_state.selector = "Interface Ontologie"
    if r.button("Framework Mapping",use_container_width=True): st.session_state.selector = "Interface Référentiel"

    # Direct to the appropriate page
    if st.session_state.selector == "Interface Ontologie":
        ontologyMatching()
    if st.session_state.selector== "Interface Référentiel":
        referentialMatching()


    
       
if __name__ == "__main__":
    main()
