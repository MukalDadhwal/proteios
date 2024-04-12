import streamlit as st
import py3Dmol
from stmol import showmol

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

tab1, tab2, tab3 = st.tabs(["3-D Model Visualization", "Insights", "About the Project"])

def render_model():
    xyzview = py3Dmol.view(query='pdb:'+protein)
    xyzview.setStyle({style:{'color':'spectrum'}})
    xyzview.setBackgroundColor(bcolor)

    if spin:
        xyzview.spin(True)
    else:
        xyzview.spin(False)

    xyzview.zoomTo()
    showmol(xyzview,height=500,width=800)

    
st.sidebar.title('Show Proteins')
prot_str='1A2C,1BML,1D5M,1D5X,1D5Z,1D6E,1DEE,1E9F,1FC2,1FCC,1G4U,1GZS,1HE1,1HEZ,1HQR,1HXY,1IBX,1JBU,1JWM,1JWS'
prot_list=prot_str.split(',')
bcolor = st.sidebar.color_picker('Pick A Color', '#00f900')
protein=st.sidebar.selectbox('select protein',prot_list)
style = st.sidebar.selectbox('style',['line','cross','stick','sphere','cartoon','clicksphere'])
spin = st.sidebar.checkbox('Spin', value = False)

with tab1:
    render_model()
with tab3:
    about_us()
