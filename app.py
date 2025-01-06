from collections import deque
from loguru import logger
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network as VisNetwork  # type: ignore[import-untyped]

logger.add(f"logs/app.log", rotation="10 MB", backtrace=True,
           diagnose=True, level="DEBUG")
logger.info(f"Executing Streamlit app {__file__}")

CURRENT_DIR = Path(__file__).resolve().parent
HTML_DIR = (hdir if (hdir := CURRENT_DIR / 'html_files').exists()
            else Path('/tmp')).absolute()

logger.info(f'HTML_DIR: {HTML_DIR}')

# GUI: Title
st.title("Network Graph Visualization of Students' Learning Plans")

# Define list of selection options and sort alphabetically
curricula_list = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']

# GUI: Multiselect dropdown menu for option selection (returns a list)
selected_curricula = st.multiselect(
    'Select curricula to visualize', curricula_list, default=curricula_list[:])

logger.debug(f"Selected curricula: {selected_curricula}")

# Set info message on initial site load
if len(selected_curricula) == 0:
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
    height='800px',
    width='95%',
)
vis_net.from_nx(G)

logger.debug(f"Generated PyVis network graph: {vis_net}")

# # Save the HTML file
html_path = HTML_DIR / 'lplans_graph.html'
if False:  # work with a pre-computed file for now
    vis_net.save_graph(str(html_path))

logger.debug(f"Saved HTML file: {html_path}")

# Load HTML file in HTML component for display on Streamlit page
with open(html_path, 'r', encoding='utf-8') as f_html:
    components.html(f_html.read(), height=800)

logger.debug(f"Displayed iframe with HTML file: {html_path}")

# GUI: Disclamimer
st.warning(
    "This is a *static* demo of a network graph visualization of students' "
    "learning plans.")

# add an accordion containing the last lines of the log file
NLINES = 20
with st.expander("Log file", expanded=False, icon=":material/terminal:"):
    with open("logs/app.log", "r") as f:
        # st.code(f.read(), language="log")
        lines = deque(f, NLINES)
    st.code(''.join(lines), language="log")
logger.info(f"Finished executing Streamlit app {__file__}")
