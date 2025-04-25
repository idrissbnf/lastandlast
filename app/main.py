import streamlit as st
import os
import sys
from importlib import import_module
import base64

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import utility functions
from utils import add_custom_css, add_navbar, add_bg_from_file, create_enhanced_sidebar_navigation

# Import authentication functions and database initialization
from db_utils import authenticate_user, init_database
from utils import check_authentication
from pages.login import show_login_page

# Initialize authentication session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "db_initialized" not in st.session_state:
    st.session_state.db_initialized = False

# Initialize database on app startup
if not st.session_state.db_initialized:
    st.session_state.db_initialized = init_database()

# Page configuration
st.set_page_config(
    page_title="Analyse, Nettoyage et Préparation des Données", 
    layout="wide"
)

# Check if user is authenticated
if not check_authentication():
    show_login_page()
else:
    # User is authenticated, continue with normal app flow
    
    # Add custom CSS and navbar
    add_custom_css()
    add_navbar()
    
    # Add background image - update path as needed
    try:
        add_bg_from_file("C:/Users/surface/Desktop/app/images/2.jpeg")
    except:
        st.warning("Background image not found. Please update the path.")
    
    # Initialize session state variables
    if "df" not in st.session_state:
        st.session_state["df"] = None
    if "df_filtered" not in st.session_state:
        st.session_state["df_filtered"] = None
    if "db_path" not in st.session_state:
        st.session_state["db_path"] = None
    if "tables" not in st.session_state:
        st.session_state["tables"] = []
    if "show_cleaning" not in st.session_state:
        st.session_state["show_cleaning"] = False
    if "show_filtering" not in st.session_state:
        st.session_state["show_filtering"] = False
    if "show_filter_category" not in st.session_state:
        st.session_state["show_filter_category"] = False
    if "show_filter_numeric" not in st.session_state:
        st.session_state["show_filter_numeric"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "🏠 Accueil"
    
    # Create enhanced sidebar navigation with logout option
    sidebar_container = st.sidebar.container()
    with sidebar_container:
        st.write(f"Connecté en tant que: {st.session_state.username}")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()

    # Create enhanced sidebar navigation
    page = create_enhanced_sidebar_navigation()
    
    # Import and display the selected page module
    if page == "🏠 Accueil":
        from pages.home import show_page
    elif page == "🔀 Fusion":
        from pages.merge import show_page
    elif page == "📊 Visualisation":
        from pages.visualization import show_page
    elif page == "Analyse stratégique":
        from pages.strategic import show_page
    elif page == "🤖 Prédiction":
        from pages.prediction import show_page
    
    # Call the show_page function from the selected module
    show_page()