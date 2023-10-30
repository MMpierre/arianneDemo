import streamlit as st
from streamlit_extras.colored_header import colored_header
import json


def getReferentiel():
    st.session_state.ontology = json.load(open("app/ressources/smart.json"))["SmartOntology"]

def getGaming():
    st.session_state["edTechID"] = "Gaming Tests"
    st.session_state.propertyList = ["Experience Name", "User ID", "Date", "Associated Soft Skill Block", "Results"]
    return None

def getJobsong():
    st.session_state["edTechID"] = "Jobsong"
    st.session_state.propertyList = ["Id Profil","Nom","Prénom","Mail","Adresse","Rayon","Expérience 1 - ID","Expérience 2 - ID","Expérience 3 - ID","Suggested Missions","Liked Missions "]
    return None

def getInokufu():
    st.session_state["edTechID"] = "Inokufu"
    st.session_state.propertyList = ["Nom","Url","Image","Keywords","Date"]
    return None

def displaySidebar():
    with st.sidebar:
        st.header("Use Cases",divider="red")
        a,b,c = st.columns(3)
        if a.button("Gaming Tests",use_container_width=True): st.session_state.data = getGaming()
        if b.button("User Profiles",use_container_width=True): st.session_state.data = getJobsong()
        if c.button("Avaiblable Courses",use_container_width=True): st.session_state.data = getInokufu()

        colored_header("EdTech ID",description="",color_name="red-70")
        st.info(st.session_state.edTechID)
        colored_header("Uploadez votre fichier",description="",color_name="red-70")
    uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type='json',label_visibility="collapsed")
    if st.sidebar.button("Reset",use_container_width=True): 
        st.session_state.submitted = False
        st.session_state.submitted2 = False
        st.session_state.propertyForm = False
        st.session_state.mappingForm = False

    # Initialize an empty dictionary to hold your JSON data
    data = {}

    # Load the JSON file if uploaded
    if uploaded_file is not None:
        uploaded_data_read = uploaded_file.read()
        data = json.loads(uploaded_data_read)
            

def matchingTool():
    l,r = st.columns([1,2])
    with l,st.form("Item type"):
        colored_header("Select you item type :",description='You can check your object type in the table above',color_name="red-50")
        st.selectbox("type",st.session_state.ontology.keys(),key="selectedType",label_visibility="collapsed")
        if st.form_submit_button("Confirmer",use_container_width=True): st.session_state.submitted = True
    if st.session_state.submitted:
        with r,st.form("property match"):
            colored_header("Select the objects in the fields",description="Add each field which is an experience, a competency or an individual choice",color_name="red-50")
            st.multiselect("objectFields",st.session_state.propertyList,label_visibility="collapsed",key="selected")
            if st.form_submit_button("Confirmer",use_container_width=True) : st.session_state.submitted2 = True
   
    colored_header("Matching",description="",color_name="red-70") 
    if st.session_state.submitted2 == True:
        
        o,p = st.columns(2)
        with o,st.form("Object match"):
            colored_header("Match the Objects",description="",color_name="red-50")
            for object in st.session_state.selected:
                l,r = st.columns(2)
                l.info(object)
                r.selectbox("propriete",list(st.session_state.ontology[st.session_state.selectedType]["Objects"]) + ["New Object"],key = f"object4{object}",label_visibility="collapsed")
            if st.form_submit_button("Confirmer",use_container_width=True) : st.session_state.mappingForm = True
        with p,st.form("Property match"):
            colored_header("Match the Properties",description="",color_name="red-50")
            for propriete in set(st.session_state.propertyList).difference(set(st.session_state.selected)):
                l,r = st.columns(2)
                l.info(propriete)
                r.selectbox("propriete",list(st.session_state.ontology[st.session_state.selectedType]["Properties"]) + ["New Property"],key = f"property4{propriete}",label_visibility="collapsed")
            if st.form_submit_button("Confirmer",use_container_width=True) : st.session_state.propertyForm = True
        if st.session_state.mappingForm : o.success("Object Mapping Done")
        if st.session_state.propertyForm : p.success("Property Mapping Done")


def ontologyMatching():
    st.title("Outil de Mapping d'ontologie")
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
        st.session_state.submitted2 = False
        st.session_state.propertyForm = False
        st.session_state.mappingForm = False
        getGaming()
    getReferentiel()
    displaySidebar()
    st.session_state.col2M, st.session_state.col3M = st.columns(2)

    with st.expander("Schéma",expanded=True):
        colored_header("L'ontologie SMART","",color_name="red-70")
        st.image("app/ressources/ontologyVisualization.png",use_column_width=True)

    colored_header("Mapping",description="",color_name="red-70")
    matchingTool()

    if st.session_state.propertyForm and st.session_state.mappingForm:
        if st.button("Confirmer le Mapping",use_container_width=True) : st.success("Le mapping a été sauvegardé !")

if __name__ == "__main__":

    st.set_page_config(layout='wide')
    st.title("Outil de Matching d'Ontologie")
    ontologyMatching()