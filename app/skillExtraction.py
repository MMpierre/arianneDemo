import streamlit as st
import json
import xml.etree.ElementTree as ET
import numpy as np

def displayFormation():
    with st.form("formation"):
        st.header(st.session_state.selectedFormation["title"],divider="red")
        
        l,m,r = st.columns(3)
        l.success(st.session_state.selectedFormation["job_trained_for"])
        m.success(st.session_state.selectedFormation["education_level_targeted"])
        r.success(st.session_state.selectedFormation["training_organization"])
        with st.expander("Description",expanded=True):
            st.write(st.session_state.selectedFormation["description"])
        l,r = st.columns(2)
        l.info(st.session_state.selectedFormation["duration"])
        r.info(st.session_state.selectedFormation["location"])
        if l.form_submit_button("Previous",use_container_width=True):
            update_index(-1)
            st.rerun()
        if r.form_submit_button("Next",use_container_width=True):
            update_index(1)
            st.rerun()

def getSkills(skillType):
    liste = st.session_state["jobSkills"][st.session_state.selectedFormation["title"]][skillType]
    return [skill for id in liste for skill in st.session_state[skillType] if skill["id"] == id]
    
def displayRome():
    st.header("Rome Skills",divider="red")
    st.selectbox("Skill type",["Savoir-faire","Savoirs"],format_func=lambda x:x,key="skillType")  
    with st.form("ROME"):  
        default = getSkills(st.session_state.skillType)
        st.multiselect(f"Selectionnez vos {st.session_state.skillType}",st.session_state[st.session_state.skillType],default=default,format_func=lambda x:x["prefLabel"][0]["value"])
        st.form_submit_button("Confirmer",use_container_width=True)

def displayRNCP():
    with st.form("RNCP"):
        st.header("RNCP Skills",divider="red")
        for i in range(3):
            with st.expander(f"Suggestion #{i}",expanded=True):
                s,t = st.columns([5,1])
                s.subheader(f"Skill Label #{i}",divider="blue")
                t.checkbox("valided",False,key = f"check2_{i}",label_visibility='collapsed')
        st.form_submit_button("Confirm",use_container_width=True)

def displaySidebar():

    st.sidebar.header("Use Cases",divider="red")
    st.sidebar.button("GEN",use_container_width=True,disabled=True)

    st.sidebar.header("Edtech ID",divider="red")
    st.sidebar.info("GEN")

    st.sidebar.header("Catalogue",divider="red")
    st.sidebar.selectbox("Select your Item",st.session_state.formations,index=st.session_state['current_index'],format_func=lambda x:x["title"],key="selectedFormation")
    if st.session_state.selectedFormation != st.session_state['formations'][st.session_state['current_index']]:
        st.session_state['current_index'] = st.session_state['formations'].index(st.session_state.selectedFormation)

def update_index(change):
    st.session_state['current_index'] += change
    st.session_state['current_index'] %= len(st.session_state['formations']) 


def update_multiselect_style():
    st.markdown(
        """
        <style>
            .stMultiSelect [data-baseweb="tag"] {
                height: fit-content;
            }
            .stMultiSelect [data-baseweb="tag"] span[title] {
                white-space: normal; max-width: 100%; overflow-wrap: anywhere;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def generate_hsl_colors(num_colors, lightness, saturation):
    # Generates colors with the same lightness and saturation, but varying hue
    return [f"hsl({h}, {saturation}%, {lightness}%)" for h in np.linspace(0, 360, num=num_colors, endpoint=False)]

st.cache_resource(show_spinner=True)
def update_multiselect_color():
    num_categories = len(st.session_state["KLC"])
    lightness = 40  # Lightness at 50% for a balanced brightness
    colors = generate_hsl_colors(num_categories, lightness, 60)
    css_rules = ""
    for categorie,color in zip(st.session_state["KLC"],colors):
        for knowledge in categorie["narrower"]:
            var = knowledge["prefLabel"][0]["value"]
            # Append each rule to the css_rules string
            css_rules += f"""
                span[data-baseweb="tag"][aria-label="{var}, close by backspace"] {{
                    background-color: {color};
                }}
            """

    num_categories = len(st.session_state["KHD"])
    lightness = 40  # Lightness at 50% for a balanced brightness
    colors = generate_hsl_colors(num_categories, lightness, 60)
    for categorie,color in zip(st.session_state["KHD"],colors):
        for knowledge in categorie["narrower"]:
            var = knowledge["prefLabel"][0]["value"]
            # Append each rule to the css_rules string
            css_rules += f"""
                span[data-baseweb="tag"][aria-label="{var}, close by backspace"] {{
                    background-color: {color};
                }}
            """

    # Inject the concatenated CSS rules into one style block
    css = f"<style>{css_rules}</style>"
    return css


def initialize():
    st.session_state["formations"] = json.load(open("app/data/formationGEN/sample.json","r"))
    st.session_state["Savoirs"] = [knowledge for knowledge in json.load(open("app/data/ROME/allKnowledges.json","r")) if len(knowledge["id"])==26]
    for word in ["Brevet","Certificat","Habilitation","CACES","Permis","Attestation","Qualification"]:
        st.session_state["Savoirs"] = [knowledge for knowledge in st.session_state["Savoirs"] if word not in knowledge["prefLabel"][0]["value"]]
    st.session_state["KLC"] = json.load(open("app/data/ROME/knowledgeCategories.json","r"))
    st.session_state["KHD"] = json.load(open("app/data/ROME/knowHowDomains.json","r"))
    st.session_state["Savoir-faire"] = json.load(open("app/data/ROME/allSkills.json","r"))
    st.session_state["jobSkills"] = json.load(open("app/data/jsons/jobSkills.json","r"))
    st.session_state.css = update_multiselect_color()
    st.session_state['current_index'] = 0



def skillExtraction():
    if "formations" not in st.session_state:
        initialize()
    update_multiselect_style()
    st.markdown(st.session_state.css, unsafe_allow_html=True)
    displaySidebar()
    displayFormation()
    
    displayRome()

if __name__ == "__main__":
    st.set_page_config(layout='wide')
    st.title("Skill Extraction Tool")
    skillExtraction()