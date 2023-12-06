import streamlit as st
import json
import random
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
    skilltypes = ["Hard Skills","Knowledges","Soft Skills"]
    for j,(skilltype,tab) in enumerate(zip(skilltypes,st.tabs(skilltypes))):
        if skilltype == "Soft Skills":
            default = [skill for skill,desc in st.session_state["Soft Skills"].items()]
        else:
            default = [skill["prefLabel"][0]["value"] for skill in getSkills(skilltype)]
        score = [random.randint(1,99) for skill in default]
        with tab:
            for i,(score,skill) in enumerate(sorted(zip(score, default), key=lambda x: x[0],reverse=True)):
                with st.form(f"ROME_{i},{j}"):  
                    s,t = st.columns([5,1])
                    s.subheader(f"{skill}",divider="green")
                    with s.expander("Description"):
                        st.info("Description")
                    t.metric("Score",f"{score} %",label_visibility="hidden")
                    t.form_submit_button("Confirm",use_container_width=True)


def displayRNCP():
        st.header("RNCP Skills",divider="red")
        default = random.choices(st.session_state["RNCP"],k=20)
        score = [random.randint(1,99) for skill in default]
        for i,(score,skillBlock) in enumerate(sorted(zip(score, default), key=lambda x: x[0],reverse=True)):
            with st.form(f"RNCP {i}"):
                s,t = st.columns([5,1])
                s.subheader(f'{skillBlock["prefLabel"][0]}'    ,divider="green")
                with s.expander("Skills",expanded=False):
                    if "competency" in skillBlock.keys() and len(skillBlock["competency"])>0:
                        for skill in skillBlock["competency"]:
                            st.info(skill["prefLabel"][0])
                    else:
                        st.info("No sub-skills for this block")
                t.metric("Score",f"{score} %",label_visibility="hidden")
                t.form_submit_button("Confirm",use_container_width=True)

def displaySidebar():

    st.sidebar.header("Use Cases",divider="red")
    st.sidebar.button("GEN",use_container_width=True,disabled=True)

    st.sidebar.header("Data Provider",divider="red")
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

    st.session_state["Knowledges"] = [knowledge for knowledge in json.load(open("app/data/ROME/allKnowledges.json","r")) if len(knowledge["id"])==26]
    for word in ["Brevet","Certificat","Habilitation","CACES","Permis","Attestation","Qualification"]:
        st.session_state["Knowledges"] = [knowledge for knowledge in st.session_state["Knowledges"] if word not in knowledge["prefLabel"][0]["value"]]
    st.session_state["Hard Skills"] = json.load(open("app/data/ROME/allSkills.json","r"))

    st.session_state["KLC"] = json.load(open("app/data/ROME/knowledgeCategories.json","r"))
    st.session_state["KHD"] = json.load(open("app/data/ROME/knowHowDomains.json","r"))

    st.session_state["jobSkills"] = json.load(open("app/data/jsons/jobSkills.json","r"))

    st.session_state["RNCP"] = json.load(open("app/data/RNCP/RNCPblocks.json"))

    st.session_state["Soft Skills"] = json.load(open("app/data/ROME/allProfesionnalBehaviors.json","r"))
    st.session_state.css = update_multiselect_color()

    st.session_state['current_index'] = 0



def skillExtraction():
    if "formations" not in st.session_state:
        initialize()
    # st.markdown(st.session_state.css, unsafe_allow_html=True)
    displaySidebar()
    displayFormation()
    rome,rncp = st.tabs(["ROME","RNCP"])
    with rome:
        displayRome()
    with rncp:
        displayRNCP()

if __name__ == "__main__":
    st.set_page_config(layout='wide')
    st.title("Training Enhancing")
    skillExtraction()