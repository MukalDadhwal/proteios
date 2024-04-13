import streamlit as st
import py3Dmol
import requests
import biotite.structure.io as bsio
import py3Dmol
from Bio.PDB import PDBParser
import matplotlib.pyplot as plt
from graphein.protein.analysis import plot_residue_composition
from graphein.protein.graphs import construct_graph
from graphein.protein.config import ProteinGraphConfig, DSSPConfig
from graphein.protein.edges.distance import (
    add_aromatic_interactions,
    add_disulfide_interactions,
    add_hydrophobic_interactions,
    add_peptide_bonds,
)
from graphein.protein.visualisation import plotly_protein_structure_graph
from graphein.protein.analysis import plot_edge_type_distribution
from graphein.protein.analysis import plot_degree_by_residue_type
from stmol import showmol
from tempfile import NamedTemporaryFile
import os
# from PIL import Image
# from fpdf import FPDF
# import base64


tab1, tab2, tab3, tab4 = st.tabs(["3-D Model Visualization", "Insights", "About the Project", "Analysis"])

with st.sidebar.container(height=250,border=False):
    logo_url = "proteios\logo_1.png"
    st.image(logo_url)


st.sidebar.write("A one option tool to Visualise Protein Compound by using libraries like Graphene and BioPython to generate 3D views of proteins and provide in-depth information about their structure and constituents.\n")

# stmol
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'cartoon':{'color':'spectrum'}})
    pdbview.setBackgroundColor('white')#('0xeeeeee')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height = 500,width=800)


def generate_visual_graphein(pdb_file):
    config = ProteinGraphConfig(
     edge_construction_functions=[       # List of functions to call to construct edges.
         add_hydrophobic_interactions,
         add_aromatic_interactions,
         add_disulfide_interactions,
         add_peptide_bonds,
     ],
     #graph_metadata_functions=[asa, rsa],  # Add ASA and RSA features.
     #dssp_config=DSSPConfig(),             # Add DSSP config in order to compute ASA and RSA.
    )  
    g = construct_graph(path=pdb_file, config=config)

    return g


# Protein sequence input
txt1 = "MKPALVVVDMVNEFIHGRLATPEAMKTVGPARKVIETFRRSGLPVVYVNDSHYPDDPEIRIWGRHSMKGDDGSEVIDEIRPSAGDYVLEKHAYSGFYGTNLDMILRANGIDTVVLIGLDADICVRHTAADALYRNYRIIVVEDAVAARIDPNWKDYFTRVYGATVKRSDEIEGMLQEDQIET"
txt = st.sidebar.text_input('Input sequence',txt1)
#if not txt:
    #txt = "SNAGGSATGTGLVYVDAFTRFHCLWDASHPECPARVSTVMEMLETEGLLGRCVQVEARAVTEDELLLVHTKEYVELMKSTQNMTEEELKTLAEKYDSVYLHPGFFSSACLSVGSVLQLVDKVMTSQLRNGFSINRPPGHHAQADKMNGFCMFNNLAIAARYAQKRHRVQRVLIVDWDVHHGQGIQYIFEEDPSVLYFSVHRYEDGSFWPHLKESDSSSVGSGAGQGYNINLPWNKVGMESGDYITAFQQLLLPVAYEFQPQLVLVAAGFDAVIGDPKGGMQVSPECFSILTHMLKGVAQGRLVLALEGGYNLQSTAEGVCASMRSLLGDPCPHLPSSGAPCESALKSISKTISDLYPFWKSLQTFE"
        

#st.set_page_config(page_title='Proteios', layout = 'wide', page_icon = 'proteios.png', initial_sidebar_state = 'auto')

# ESMfold
def update(condition,sequence = txt):
    with tab1:
        
        # headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded',
        # }

        # response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence,verify = False)
        # #name = sequence[:3] + sequence[-3:]
        # pdb_string = response.content.decode('utf-8')

        # with open('predicted.pdb', 'w') as f:
        #    f.write(pdb_string)

        # ##global file_name
        # #file_name ="predicted.pdb"

        # g = generate_visual_graphein("predicted.pdb")

        if condition == True:

            headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            }   

            response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence,verify = False)
            #name = sequence[:3] + sequence[-3:]
            pdb_string = response.content.decode('utf-8')

            with open('predicted.pdb', 'w') as f:
                f.write(pdb_string)

            g = generate_visual_graphein("predicted.pdb")
            
            struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
            b_value = round(struct.b_factor.mean(), 4)

            st.subheader('Visualization of predicted protein structure')
            #render_mol(pdb_string)
            st.write(plotly_protein_structure_graph(g, node_size_multiplier=1))

            st.subheader('plDDT')
            st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.')
            st.info(f'plDDT: {b_value}')

            st.download_button(
                label="Download PDB",
                data=pdb_string,
                file_name='predicted.pdb',
                mime='text/plain',
            )
            
        else:
            g = generate_visual_graphein("predicted.pdb")
            return g


#file_name = "predicted.pdb"
#graph = generate_visual_graphein(file_name)

predict = st.sidebar.button('Predict', on_click=update(condition=True))

graph = update(condition = False)

#if not predict:
  #          st.warning('👈 Enter protein sequence data!')


def about_us():
    st.title("Proteios: A Protein Behavior Prediction Web Application")
    st.write("""
    This web application predicts and visualizes the behavior of known and unknown proteins.
    It utilizes Graphene and BioPython modules to generate 3D views of proteins and provide in-depth information about their structure and constituents.
    """)

    st.header("Mukal Dhadhwal:")
    st.write("""
    LinkedIn: [Mukal's Link](https://www.linkedin.com/in/mukal-dadhwal/)
    """)

    st.header("Brahamdeep Singh.")
    st.write("""
    LinkedIn: [Brahamdeep's Link](https://www.linkedin.com/in/brahamdeep-singh-sabharwal-14a914256/)
    """)

    st.header("Ishwardeep Singh.")
    st.write("""
    LinkedIn: [Ishwardeep's Link](https://www.linkedin.com/in/ishwardeep-singh-405a9324a/)
    """)

    st.header("Prabhsurat Singh.")
    st.write("""
    LinkedIn: [Prabhsurat's Link](https://www.linkedin.com/in/prabhsurat-singh-1868052ab/)
    """)


with tab2:
    st.title("Residue Composition")
    fig = plot_residue_composition(graph, sort_by="count", plot_type="pie") # Can also sort by "alphabetical"
    st.write("Residue composition in proteins refers to the types and quantities of amino acid residues present in a protein molecule. Amino acids are the building blocks of proteins, and each amino acid has its own unique chemical properties.")
    st.write(fig)

    st.title("Edge Type Distribution")
    fig2 = plot_edge_type_distribution(graph, plot_type="bar", title="Edge Type Distribution")
    st.write("Edge Type Distribution in proteins refers to the proportion and variety of interactions between amino acid residues within the protein structure, including covalent bonds, hydrogen bonds, van der Waals forces, hydrophobic interactions, and electrostatic interactions. Analyzing this distribution provides insights into the protein's structural stability, folding pattern, and functional properties")
    st.write(fig2)

    st.title("Total Degree by Residue Type:- Type-1")
    fig3 = plot_degree_by_residue_type(graph, normalise_by_residue_occurrence=False)
    st.write("It refers to the sum of connections or interactions that each type of amino acid residue forms within a protein structure. In other words, it quantifies how many bonds or interactions each amino acid type participates in within the protein.")
    st.write(fig3)

    st.title("Total Degree by Residue Type:- Type-2")
    fig4 = plot_degree_by_residue_type(graph, normalise_by_residue_occurrence=True)
    st.write("The following refers to a calculation that takes into account both the number of interactions formed by each type of amino acid residue and the frequency of occurrence of each residue type within the protein structure.")
    st.write(fig4)


with tab3:
    about_us()

with tab4:
    st.title("Generate Protein Structure from PDB file")

    col1,col2 = st.columns(2)
    disp_col2 = False
    
    
    st.header("File Generated Structure")
    file = st.file_uploader("Please add PDB file", type=['pdb'])
    result = st.button("Add File")
    
    if result and file is None:
        st.warning("Please add a valid file!!!!")
            
            
    if result and file is not None:
        # Save uploaded file temporarily
        with open("analyze.pdb", "wb") as f:
            f.write(file.getvalue())
        graph_analysis = generate_visual_graphein("analyze.pdb")
            
        st.write(plotly_protein_structure_graph(graph_analysis, node_size_multiplier=1))
        disp_col2 = True

        os.unlink("analyze.pdb")


    st.divider()


    if result: 
        st.header("Standard Structure")

        g = generate_visual_graphein("predicted.pdb")
        st.write(plotly_protein_structure_graph(g, node_size_multiplier=1))

    





        
        
    





    

