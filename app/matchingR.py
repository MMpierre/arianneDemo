import streamlit as st
from streamlit_extras.colored_header import colored_header
import json
import random
import pandas as pd



def displayGraphG():
    d,m,p = st.columns(3)
    description = st.container()

    d.selectbox("Domaine",st.session_state.GEN.keys(),index=0,format_func=lambda x : st.session_state.GEN[x]["prefLabel"][0]["@value"],key="domain")
    m.selectbox("Métier",st.session_state.GEN[st.session_state.domain]["children"],index=0,format_func=lambda x : x["prefLabel"][0]["@value"],key="job")
    p.selectbox("Poste",st.session_state.job["children"],index=0,format_func=lambda x : x["prefLabel"][0]["@value"],key="occupation")

    with description:
        occupation = st.session_state.occupation["prefLabel"][0]["@value"]
        colored_header(occupation,"",color_name="blue-30")
        st.info(f'The "{occupation}" is a- Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam molestie gravida turpis sit amet pellentesque. Aliquam suscipit posuere egestas. Quisque ac sapien eros. Sed gravida dictum dui ut condimentum. Integer accumsan turpis ut nulla iaculis pulvinar. Donec efficitur, odio quis dignissim consequat, urna magna mattis tellus, vel rutrum ipsum sem ac odio. Donec diam nibh, placerat ut risus a, lobortis blandit risus. Vestibulum ac mattis enim, sed sollicitudin justo. Duis eget pretium libero. Phasellus facilisis velit vel odio molestie, ut interdum nisi facilisis.')

def displayGraphD():
    df = st.session_state.matching.loc[st.session_state.matching["Libelle GEN"] == st.session_state.occupation["prefLabel"][0]["@value"],["V","Code ROME","Libelle ROME","score"]].sort_values(by='score', ascending=False)
    if len(df) == 0:
        st.warning("No proposed match for this particular occupation")
    else:
            
        filter = st.multiselect("Job Card Filter",df["Code ROME"].unique().tolist())
        if len(filter)>0:
            df = df[df["Code ROME"].isin(filter)]

        for rank,row in df.iterrows():
            
            if row["V"] == "Oui": 
                st.subheader(f'{row["score"]} % | {row["Code ROME"]} - {row["Libelle ROME"]}',divider="green")
                with st.expander("Description"):
                    st.info(st.session_state.defs[row["Libelle ROME"]])

                if st.button("Unmatch",use_container_width=True,key=f"{rank}submit"): 
                    st.session_state.matching.loc[rank,"V"] = "Non"
                    st.rerun()
                
            elif row["V"] == "Non" :  
                st.subheader(f'{row["score"]} % | {row["Code ROME"]} - {row["Libelle ROME"]}',divider="red")
                with st.expander("Description"):
                    st.info(st.session_state.defs[row["Libelle ROME"]])

                if st.button("Match",use_container_width=True,key=f"{rank}submit"): 
                    st.session_state.matching.loc[rank,"V"] = "Oui"
                    st.rerun()
            
            else:
                st.subheader(f'{row["score"]//0.1/10} % | {row["Code ROME"]} - {row["Libelle ROME"]}',divider="orange")
                with st.expander("Description"):
                    st.info(st.session_state.defs[row["Libelle ROME"]])

                l,r = st.columns(2)
                if l.button("Unmatch",use_container_width=True,key=f"{rank}rsubmit"): 
                    st.session_state.matching.loc[rank,"V"] = "Non"
                    st.rerun()
                if r.button("Match",use_container_width=True,key=f"{rank}lsubmit"): 
                    st.session_state.matching.loc[rank,"V"] = "Oui"
                    st.rerun()

            



def displaySidebar():
    with st.sidebar:
        st.header("Use Cases",divider="red")
        st.button("GEN Framework",use_container_width=True)
        st.header("EdTech ID",divider="red")
        st.info("GEN")
        st.header("Targeted Framework",divider="red")
        l,r = st.columns(2)
        l.button("ROME Framework",use_container_width=True)
        r.button("ESCO Framework",use_container_width=True)
        st.header("Automatic Validation",divider="red")
        st.slider("Automatic Validation Treshold",0,100,95,1,key="seuil")
        _,l,r = st.columns([1,2,2])
        st.button("Automatic Validation",use_container_width=True)
        st.progress(100-st.session_state.seuil,f"Reste à évaluer {((st.session_state.matching['score'] > 0) & (st.session_state.matching['score'] < st.session_state.seuil)).sum()}/{len(st.session_state.matching)}")
        file = st.file_uploader("Upload your file",label_visibility='collapsed',disabled=True)
        


def displayMatching():
    with st.form("Matching"):
        st.header("Progression",divider="red")
        st.session_state.bools = [ st.session_state.matching["score"] == 100,
                 (st.session_state.matching["score"] < 100) & (st.session_state.matching["score"] > st.session_state.seuil),
                 (st.session_state.matching["score"] > 0) & (st.session_state.matching["score"] < st.session_state.seuil),
                 st.session_state.matching["score"] == 0]
        values = [bool.sum() for bool in st.session_state.bools]
        levels = st.columns(4)
        colors = ["green","yellow","orange","red"]
        names = ["Valided",
                 "Automatic Validation",
                 "Automatic Rejection",
                 "Rejected"]
        desc = ["All validated Mappings",
                f"Mappings with a score above {st.session_state.seuil}%",
                f"Mappings with a score below {st.session_state.seuil}%",
                "All rejected Mappings"]
        for i,level in enumerate(levels):
            with level:
                colored_header(names[i],description=desc[i],color_name=f"{colors[i]}-70")
                if st.form_submit_button(f"Access ({values[i]})",use_container_width=True): st.session_state["confiance"] = i 


def displayMatches():
    with st.expander("Matches",expanded=True):
        colors = ["green","yellow","orange","red"]
        names = ["Valided",
                 "Automatic Validation",
                 "Manual Evaluation",
                 "Rejected"]
        colored_header(names[st.session_state.confiance],"",color_name=f"{colors[st.session_state.confiance]}-70")
        df = st.session_state.matching[st.session_state.bools[st.session_state.confiance] ].sort_values(by='Libelle GEN', ascending=True).sort_values(by='score', ascending=False)
        for rank,row in df[:20].iterrows():
            g,r,s = st.columns([5,5,1])
            g.info(row["Libelle GEN"])
            r.info(row["Libelle ROME"])
            s.success(f"{row['score']//0.1/10} %")

def initialization():
    st.session_state.GEN = json.load(open("app/data/GEN/transformed_referentielGEN.json","rb"))
    st.session_state.matching = pd.read_csv("app/data/GEN/GEN_ROME.csv")
    st.session_state.defs = json.load(open("app/data/ROME/descriptionsROME.json","r"))
    st.session_state["confiance"] = 0
    st.session_state.rules = []

def referentialMatching():
    if st.sidebar.button("Reset",use_container_width=True) or "GEN" not in st.session_state:
        with st.spinner("Loading Frameworks"):
            initialization()
    tabs = st.tabs(["Matching","Exploration"])
    displaySidebar()
    with tabs[0]:
        col1, col2 = st.columns([2,2])
        with col1:
            st.header("GEN Framework",divider="red")
            displayGraphG()
        with col2:
            st.header("ROME Framework",divider="red")
            displayGraphD()
    with tabs[1]:
        displayMatching()
        displayMatches()

if __name__ == "__main__":
    st.set_page_config(page_title="matching tool",layout="wide")
    st.title("Outil de Matching de Référentiel")
    referentialMatching()