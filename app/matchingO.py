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
    st.session_state.propertyList = ["Experience Id","Experience Label","Associated Hard Skills","Associated Soft Skills","Suggested Missions","Liked Missons"]
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
        if b.button("Career Paths",use_container_width=True): st.session_state.data = getJobsong()
        if c.button("Avaiblable Courses",use_container_width=True): st.session_state.data = getInokufu()

        colored_header("EdTech ID",description="",color_name="red-70")
        st.info(st.session_state.edTechID)
        colored_header("Uploadez votre fichier",description="",color_name="red-70")
    uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type='json',label_visibility="collapsed",disabled=True)
    if st.sidebar.button("Reset",use_container_width=True): 
        st.session_state.submitted = False
        st.session_state.submitted2 = False
        st.session_state.propertyForm = False
        st.session_state.mappingForm = False
        st.session_state.exps = []
        st.session_state.comps = []
        st.session_state.rules = []
        if "new_list" in st.session_state:
            del st.session_state.new_list


    # Initialize an empty dictionary to hold your JSON data
    data = {}

    # Load the JSON file if uploaded
    if uploaded_file is not None:
        uploaded_data_read = uploaded_file.read()
        data = json.loads(uploaded_data_read)
            

def matchingTool():
    l,r = st.columns([1,2])
    with l,st.form("Item type"):
        colored_header("Add a new item:",description="",color_name="red-50")
        st.selectbox("Select your Object type",["Experience","Competency","Individual Choice"],key="selectedType")
        st.text_input("Name your Object",f"{st.session_state.edTechID} - Objet {len(st.session_state.comps)+len(st.session_state.exps)}",help="Name your Object",key="objectName")
        if st.form_submit_button("Confirmer",use_container_width=True): st.session_state.submitted = True
    if st.session_state.submitted:
        with r,st.form("property match"):
            colored_header("Define mandatory properties",description="Add each field which is an experience, a competency or an individual choice",color_name="red-50")
            if st.session_state.selectedType == "Experience":
                l,r = st.columns(2)
                l.info("Experience Type")
                r.selectbox("objectFields",["Professional","Vocationnal","Educational","Test","Custom"],label_visibility="collapsed",key="selected")
                l,r = st.columns(2)
                l.info("Experience Status")
                r.selectbox("objectFields",["Past","Ongoing","Suggested"],label_visibility="collapsed",key="selected2")
                if st.form_submit_button("Confirmer",use_container_width=True) : 
                    st.session_state.exps.append((st.session_state.selectedType,st.session_state.objectName,st.session_state.selected,st.session_state.selected2))
                    st.session_state.submitted = False
                    st.rerun()
            elif st.session_state.selectedType == "Competency":
                l,r = st.columns(2)
                l.info("Skill Type")
                r.selectbox("objectFields",["Hard Skill","Soft Skill","Personality Trait","Mixed"],label_visibility="collapsed",key="selected")
                l,r = st.columns(2)
                l.info("Experience")
                if len(st.session_state.exps)>0:
                    r.selectbox("objectFields",st.session_state.exps,format_func=lambda x : x[1],label_visibility="collapsed",key="selected2")
                else:
                    r.error("First create an experience")
                if st.form_submit_button("Confirmer",use_container_width=True) : 
                    st.session_state.comps.append((st.session_state.selectedType,st.session_state.objectName,st.session_state.selected,st.session_state.selected2[1]))
                    st.session_state.submitted = False
                    st.rerun()
            elif st.session_state.selectedType == "Individual Choice":
                l,r = st.columns(2)
                l.info("Polarity")
                r.selectbox("objectFields",["Like","Level"],label_visibility="collapsed",key="selected")
                l,r = st.columns(2)
                l.info("Experience")
                if len(st.session_state.exps)>0:
                    r.selectbox("objectFields",st.session_state.exps,format_func=lambda x : x[1],label_visibility="collapsed",key="selected2")
                else:
                    r.error("First create an experience")
                if st.form_submit_button("Confirmer",use_container_width=True) : 
                    st.session_state.comps.append((st.session_state.selectedType,st.session_state.objectName,st.session_state.selected,st.session_state.selected2[1]))
                    st.session_state.submitted = False
                    st.rerun()
    for object in st.session_state.exps:
        st.info(object)
    for object in st.session_state.comps:
        st.info(object)
    colored_header("Matching",description="",color_name="red-70") 
    if len(st.session_state.exps) > 0:
        
        o,_,_ = st.columns(3)
        with o,st.form("Map your properties"):
            colored_header("Select your Object",description="",color_name="red-50")
            st.selectbox("Select your object",st.session_state.exps + st.session_state.comps,format_func=lambda x: x[1],key="currentObject",label_visibility="collapsed")
            if st.form_submit_button("Confirmer",use_container_width=True) : st.session_state.submitted2 = True
        if st.session_state.submitted2:
            with st.form("Property match"):
                colored_header(f"Map '{st.session_state.currentObject[1]}' properties",description="",color_name="red-50")

                l,r = st.columns(2)
                l.header("Your fields")
                r.header("Ontology Properties")
                if "new_list" in st.session_state:
                    liste = st.session_state.new_list
                else:
                    liste = list(st.session_state.propertyList) 
                for propriete in liste:
                    l,r = st.columns(2)
                    l.info(propriete)
                    r.selectbox("propriete",[f"Is not a property of '{st.session_state.currentObject[1]}'"]  + st.session_state.ontology[st.session_state.currentObject[0]]["Properties"],key = f"property4{propriete}",label_visibility="collapsed")
                if st.form_submit_button("Confirmer",use_container_width=True) : 
                    new_list = []
                    i=0
                    for propriete in liste:
                        st.write(st.session_state[f"property4{propriete}"])
                        st.write(f"Is not a property of '{st.session_state.currentObject[1]}'")
                        if st.session_state[f"property4{propriete}"] != f"Is not a property of '{st.session_state.currentObject[1]}'":
                            st.session_state.rules.append(f"{st.session_state.currentObject[1]} / {propriete} a été associée à {st.session_state[f'property4{propriete}']}")
                        else:
                            new_list.append(propriete)
                    if len(new_list)!=len(st.session_state.new_list):
                        st.session_state.new_list = new_list
                        st.rerun()

        if len(st.session_state.rules)>0:
            for i,rule in enumerate(st.session_state.rules):
                st.success(f"Rule {i} : " + rule)

                            
                


def ontologyMatching():
    st.title("Outil de Mapping d'ontologie")
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
        st.session_state.submitted2 = False
        st.session_state.propertyForm = False
        st.session_state.mappingForm = False
        st.session_state.exps = []
        st.session_state.comps = []
        st.session_state.rules = []
        if "new_list" in st.session_state:
            del st.session_state.new_list
        getGaming()
    getReferentiel()
    displaySidebar()
    st.session_state.col2M, st.session_state.col3M = st.columns(2)

    with st.expander("Schéma",expanded=True):
        colored_header("ARIANE pivot ontology","",color_name="red-70")
        st.image("app/ressources/ontologyVisualization.png",use_column_width=True)

    colored_header("Your Objects",description="",color_name="red-70")
    matchingTool()

    if st.session_state.propertyForm and st.session_state.mappingForm:
        if st.button("Confirmer le Mapping",use_container_width=True) : st.success("Le mapping a été sauvegardé !")

if __name__ == "__main__":

    st.set_page_config(layout='wide')
    st.title("Outil de Matching d'Ontologie")
    ontologyMatching()


