import streamlit as st
from streamlit_extras.colored_header import colored_header
import json
import random
from rdflib import Graph,SKOS,Literal


def randomJob():
    domain = random.randint(0,5)
    domaineName = list(st.session_state.GEN.keys())[domain]
    family = random.randint(0,len(st.session_state.GEN[domaineName]["children"])-1)
    job = random.randint(0,len(st.session_state.GEN[domaineName]["children"][family]["children"])-1)
    return [domain,family,job]

def displayGraphG():
    d,m,p = st.columns(3)
    description = st.container()
    l,r = st.columns(2)

    if l.button("Précédent",use_container_width=True) : st.session_state.rjob = randomJob()
    if r.button("Suivant",use_container_width=True) :  st.session_state.rjob = randomJob()
    
    job = st.session_state["rjob"]

    d.selectbox("Domaine",st.session_state.GEN.keys(),index=job[0],format_func=lambda x : st.session_state.GEN[x]["prefLabel"][0]["@value"],key="domain")
    m.selectbox("Métier",st.session_state.GEN[st.session_state.domain]["children"],index=min(job[1],len(st.session_state.GEN[st.session_state.domain]["children"])-1),format_func=lambda x : x["prefLabel"][0]["@value"],key="job")
    indexJob = st.session_state.GEN[st.session_state.domain]["children"].index(st.session_state.job)
    p.selectbox("Poste",st.session_state.GEN[st.session_state.domain]["children"][indexJob]["children"],index=min(job[2],len(st.session_state.GEN[st.session_state.domain]["children"][indexJob]["children"])-1),format_func=lambda x : x["prefLabel"][0]["@value"],key="occupation")
    indexOccupation = st.session_state.GEN[st.session_state.domain]["children"][indexJob]["children"].index(st.session_state.occupation)

    with description:
        colored_header(st.session_state.GEN[st.session_state.domain]["children"][indexJob]["children"][indexOccupation]["prefLabel"][0]["@value"],"",color_name="blue-30")
        st.info(f'The "{st.session_state.GEN[st.session_state.domain]["children"][indexJob]["children"][indexOccupation]["prefLabel"][0]["@value"]}" is a- Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam molestie gravida turpis sit amet pellentesque. Aliquam suscipit posuere egestas. Quisque ac sapien eros. Sed gravida dictum dui ut condimentum. Integer accumsan turpis ut nulla iaculis pulvinar. Donec efficitur, odio quis dignissim consequat, urna magna mattis tellus, vel rutrum ipsum sem ac odio. Donec diam nibh, placerat ut risus a, lobortis blandit risus. Vestibulum ac mattis enim, sed sollicitudin justo. Duis eget pretium libero. Phasellus facilisis velit vel odio molestie, ut interdum nisi facilisis.')

def getRandomPosition():
    return random.choice(list(st.session_state.ROME_jobs))

def getJobCard(position):
    subject = st.session_state.graph.value(predicate=SKOS.prefLabel,object=Literal(position, lang="fr"))
    jobCard = st.session_state.graph.value(subject=subject,predicate=SKOS.broader)
    return st.session_state.graph.value(subject=jobCard,predicate=SKOS.prefLabel)

def getDomain(jobCard):
    subject = st.session_state.graph.value(predicate=SKOS.prefLabel,object=Literal(jobCard, lang="fr"))
    domain = st.session_state.graph.value(object=subject,predicate=SKOS.narrower)
    return st.session_state.graph.value(subject=domain,predicate=SKOS.prefLabel)

def displayGraphD():
    d,f,p = st.columns(3)
    d.multiselect("Domain Filter",["Domain 1","Domain 2","Domain 3"])
    f.multiselect("Job Card Filter",["Job Card 1","Job Card 2","Job Card 3"])
    p.multiselect("Position Filter",["Position 1","Position 2","Position 3"])
    for i in range(3):
        position = getRandomPosition()
        jobCard = getJobCard(position) 
        domain = getDomain(jobCard) 
        with st.expander(f"{domain} / {jobCard} /",expanded=True):
            t,m = st.columns([8,2])
            t.success(position)
            m.metric("Match",f"{100-7*i} %",label_visibility="collapsed")
            st.button("Confirm",key=f"valid_{i}",use_container_width=True)
    st.button("See More",use_container_width=True)



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
        st.number_input("Automatic Validation Treshold",0,100,95,1,key="seuil")
        _,l,r = st.columns([1,2,2])
        st.button("Automatic Validation",use_container_width=True)
        st.progress(100-st.session_state.seuil,f"Reste à évaluer {int( st.session_state.seuil * 1.35)}/{135}")
        file = st.file_uploader("Upload your file",label_visibility='collapsed',disabled=True)
        


def displayMatching():
    with st.form("Matching"):
        st.header("Progression",divider="red")
        values = [55,32,20,28]
        levels = st.columns(4)
        colors = ["green","yellow","orange","red"]
        desc = ["Items mapped by hand or by automatic validation",
                "Items that have a 'probable' mapping by the algorithm",
                "Items that have several possible mappings",
                "Items that dont have satisfactory mappings"]
        for i,level in enumerate(levels):
            with level:
                colored_header(f"Seuil de confiance {i+1} - {((1-i/5)*st.session_state.seuil):.1f}%",description=desc[i],color_name=f"{colors[i]}-70")
                if st.form_submit_button(f"Accéder ({values[i]})",use_container_width=True): st.session_state["confiance"] = i 


def displayMatches():
    with st.expander("Matches"):
        colors = ["green","yellow","orange","red"]
        colored_header(f"Matches - Seuil de confiance {st.session_state.confiance+1}","",color_name=f"{colors[st.session_state.confiance]}-70")
        for i in range(5):
            with st.form(f"match  {i}"):
                l,r,t = st.columns([10,10,1])
                job = randomJob()
                domain = list(st.session_state.GEN.keys())[job[0]]
                domainName = st.session_state.GEN[domain]["prefLabel"][0]["@value"]
                family = st.session_state.GEN[domain]["children"][job[1]]["prefLabel"][0]["@value"]
                appelation = st.session_state.GEN[domain]["children"][job[1]]["children"][job[2]]["prefLabel"][0]["@value"]
                l.info(f"{domainName}  ---  {family}  ---  {appelation}")
                position = getRandomPosition()
                jobCard = getJobCard(position) 
                domain = getDomain(jobCard) 
                r.success(f"{domain} --- {jobCard} --- {position}")
                t.form_submit_button("🗑️",use_container_width=True)


def referentialMatching():
    
    if "rjob" not in st.session_state:
        with st.spinner("Loading Frameworks"):
            st.session_state.GEN = json.load(open("app/data/GEN/transformed_referentielGEN.json","rb"))
            st.session_state.ROME_jobs = json.load(open("app/data/ROME/descriptionsROME.json","rb"))
            st.session_state.graph = Graph()
            st.session_state.graph.parse("app/data/ROME/referentielROME.jsonld")

        st.session_state["rjob"] = randomJob()
        st.session_state["confiance"] = 0
    if "rules" not in st.session_state:
        st.session_state.rules = []
    displaySidebar()
    col1, col2 = st.columns([2,2])
    with col1:
        st.header("GEN Framework",divider="red")
        displayGraphG()
    with col2:
        st.header("ROME Framework",divider="red")
        displayGraphD()
    displayMatching()
    st.divider()
    displayMatches()

if __name__ == "__main__":
    st.set_page_config(page_title="matching tool",layout="wide")
    st.title("Outil de Matching de Référentiel")
    referentialMatching()