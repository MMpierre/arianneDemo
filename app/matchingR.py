import streamlit as st
from streamlit_extras.colored_header import colored_header
import json
import random

def randomJob():
    domain = random.randint(0,5)
    domaineName = list(st.session_state.GEN.keys())[domain]
    family = random.randint(0,len(st.session_state.GEN[domaineName]["children"])-1)
    job = random.randint(0,len(st.session_state.GEN[domaineName]["children"][family]["children"])-1)
    return [domain,family,job]

def displayGraphG():
    job = randomJob()
    d,m,p = st.columns(3)
    d.selectbox("Domaine",st.session_state.GEN.keys(),index=job[0],format_func=lambda x : st.session_state.GEN[x]["prefLabel"][0]["@value"],key="domain")
    m.selectbox("Métier",st.session_state.GEN[st.session_state.domain]["children"],index=job[1],format_func=lambda x : x["prefLabel"][0]["@value"],key="job")
    indexJob = st.session_state.GEN[st.session_state.domain]["children"].index(st.session_state.job)
    p.selectbox("Poste",st.session_state.GEN[st.session_state.domain]["children"][indexJob]["children"],index=job[2],format_func=lambda x : x["prefLabel"][0]["@value"],key="occupation")
    
    indexOccupation = st.session_state.GEN[st.session_state.domain]["children"][indexJob]["children"].index(st.session_state.occupation)
    colored_header(st.session_state.GEN[st.session_state.domain]["children"][indexJob]["children"][indexOccupation]["prefLabel"][0]["@value"],"",color_name="blue-30")
    st.info(f'Le "{st.session_state.GEN[st.session_state.domain]["children"][indexJob]["children"][indexOccupation]["prefLabel"][0]["@value"]}" est un Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam molestie gravida turpis sit amet pellentesque. Aliquam suscipit posuere egestas. Quisque ac sapien eros. Sed gravida dictum dui ut condimentum. Integer accumsan turpis ut nulla iaculis pulvinar. Donec efficitur, odio quis dignissim consequat, urna magna mattis tellus, vel rutrum ipsum sem ac odio. Donec diam nibh, placerat ut risus a, lobortis blandit risus. Vestibulum ac mattis enim, sed sollicitudin justo. Duis eget pretium libero. Phasellus facilisis velit vel odio molestie, ut interdum nisi facilisis.')
    l,r = st.columns(2)
    l.button("Précédent",use_container_width=True)
    r.button("Suivant",use_container_width=True)

def displayGraphD():
    d,f,p = st.columns(3)
    d.multiselect("Filtre Domaine",["Domaine 1","Domaine 2","Domaine 3"])
    f.multiselect("Filtre Fiche Métier",["Fiche 1","Fiche 2","Fiche 3"])
    p.multiselect("Filtre apellation",["Appellation 1","Appelation 2","Appelation 3"])
    for i in range(3):
        with st.expander(f"Suggestion n°{i+1} / Domaine / Fiche métier /",expanded=True):
            t,m,v = st.columns([8,2,1])
            t.success("Métier du ROME correspondant")
            m.metric("Match",f"{100-7*i} %",label_visibility="collapsed")
            v.button("✅",key=f"valid_{i}")
    st.button("Voir plus",use_container_width=True)



def displaySidebar():
    with st.sidebar:
        st.header("EdTech ID",divider="red")
        st.info("Inokufu")
        file = st.file_uploader("Upload your file",label_visibility='collapsed')
        st.header("Votre référentiels",divider="red")
        st.info("Référentiel GEN")
        st.header("Référentiel à aligner",divider="red")
        st.info("Référentiel ROME")
        st.header("Validation automatique",divider="red")
        st.number_input("Seuil de validation automatique",0,100,95,1,key="seuil")
        _,l,r = st.columns([1,2,2])
        st.button("Validation Automatique",use_container_width=True)
        st.progress(100-st.session_state.seuil,f"Reste à évaluer {int( st.session_state.seuil * 1.35)}/{135}")
        


def displayMatching():
    with st.form("Matching"):
        st.header("Progression",divider="red")
        values = [55,32,20,28]
        levels = st.columns(4)
        colors = ["green","yellow","orange","red"]
        desc = ["Alignements validés à la main ou par validation automatique",
                "Alignements pour lesquels l'algorithme est confiant",
                "Alignements pour lesquels l'algorithme hésite entre plusieurs possibilités",
                "Alignements pour lesquels l'algorithme ne trouve pas de correspondance"]
        for i,level in enumerate(levels):
            with level:
                colored_header(f"Seuil de confiance {i+1} - {values[i]}",description=desc[i],color_name=f"{colors[i]}-70")
                st.form_submit_button(f"Accéder {i}",use_container_width=True)


def displayMatches():
    with st.expander("Matches"):
        st.header("Matches",divider="red")
        for i in range(5):
            with st.form(f"match  {i}"):
                l,r,t = st.columns([10,10,1])
                job = randomJob()
                domain = list(st.session_state.GEN.keys())[job[0]]
                domainName = st.session_state.GEN[domain]["prefLabel"][0]["@value"]
                family = st.session_state.GEN[domain]["children"][job[1]]["prefLabel"][0]["@value"]
                appelation = st.session_state.GEN[domain]["children"][job[1]]["children"][job[2]]["prefLabel"][0]["@value"]
                l.info(f"{domainName}  ---  {family}  ---  {appelation}")
                r.success("Domaine / Fiche métier / metier ROME")
                t.form_submit_button("🗑️",use_container_width=True)


def referentialMatching():
    st.session_state.GEN = json.load(open("app/data/GEN/transformed_referentielGEN.json","rb"))
    if "rules" not in st.session_state:
        st.session_state.rules = []
    displaySidebar()
    col1, col2 = st.columns([2,2])
    with col1:
        st.header("Référentiel GEN",divider="red")
        displayGraphG()
    with col2:
        st.header("Référentiel ROME",divider="red")
        displayGraphD()
    displayMatching()
    st.divider()
    displayMatches()

if __name__ == "__main__":
    st.set_page_config(page_title="matching tool",layout="wide")
    st.title("Outil de Matching de Référentiel")
    referentialMatching()