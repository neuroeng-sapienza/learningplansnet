from collections import deque
from loguru import logger
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network as VisNetwork  # type: ignore[import-untyped]

# Set up logging
LOG_FILE_PATH = Path("logs/app.log")
logger.add(LOG_FILE_PATH, rotation="10 MB", backtrace=True,
           diagnose=True, level="DEBUG")
logger.info(f"Executing Streamlit app {__file__}")

# Paths
CURRENT_DIR = Path(__file__).resolve().parent
HTML_DIR = (hdir if (hdir := CURRENT_DIR / 'html_files').exists()
            else Path('/tmp')).absolute()

logger.debug(f'CURRENT_DIR: {CURRENT_DIR}')
logger.debug(f'HTML_DIR: {HTML_DIR}')

# GUI: Use wide layout
st.set_page_config(layout="wide")

# GUI: Title
st.title("Network Graph Visualization of Students' Learning Plans")

st.caption(
    "Drag an empty area of the graph to pan. "
    "Scroll with the mouse wheel to zoom in/out. "
    "Drag nodes to rearrang them."
)
st.caption("Hover over nodes to view a summary of the learning plan. "
           "Hover over edges to view the difference between learning plans.")

st.sidebar.title("Settings")

# GUI: Disclamimer
st.sidebar.warning(
    "This is a *static* demo . User interaction is limited.")

if False:  # Define list of curricula options
    st_curricula_list = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
    # GUI: Multiselect reference curricula
    student_curricula = st.sidebar.multiselect(
        "Select curricula of learning plans to visualize",
        st_curricula_list, default=st_curricula_list[:])
    logger.debug(f"Selected curricula: {student_curricula}")

# Define list of distance options
distance_list = ['6', '12', '15', '18', '21', '24']
# GUI: Select distance
selected_distance = st.sidebar.selectbox(
    'Select max distance for arcs (the higher, the denser the graph)',
    distance_list, index=distance_list.index('18'))
logger.debug(f"Selected distance: {selected_distance}")

if False:  # Set info message on initial site load
    if len(student_curricula) == 0:
        # GUI: Info
        st.text('Choose at least 1 curriculum to start')

# Read dataset (CSV)
# ...

# Create network graph when user selects >= 1 item
# Filter dataset based on selected curricula
# ...

# Create networkx graph object
G: nx.DiGraph = nx.DiGraph()
# ...

logger.debug(f"Generated netwokx graph: {G}")

# Initiate PyVis network object
vis_net: VisNetwork = VisNetwork(
    height='100%',
    width='100%',
)
vis_net.from_nx(G)

logger.debug(f"Generated PyVis network graph: {vis_net}")

# # Save the HTML file
html_path = HTML_DIR / f'lplans_graph_dist-{selected_distance}.html'
if False:  # work with a pre-computed file for now
    vis_net.save_graph(str(html_path))

logger.debug(f"Saved HTML file: {html_path}")

# Load HTML file in HTML component for display on Streamlit page
with open(html_path, 'r', encoding='utf-8') as f_html:
    components.html(f_html.read(), height=800, width=1200, scrolling=True)

logger.debug(f"Displayed iframe with HTML file: {html_path}")

# Add a horizontal rule (separator)
st.markdown("---")

# add an accordion containing the last lines of the log file
NLINES = 20
with st.sidebar.expander("Log file", expanded=False, icon=":material/terminal:"):
    with open("logs/app.log", "r") as f:
        # st.code(f.read(), language="log")
        lines = deque(f, NLINES)
    st.code(''.join(lines), language="log")

logger.info(f"Finished executing Streamlit app {__file__}")
