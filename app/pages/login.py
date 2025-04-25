import streamlit as st
import base64
import os
import time
from db_utils import authenticate_user, register_user, init_database
from utils import add_login_page_css

def add_login_bg_from_url(url):
    """
    Add a background image from URL to the login page
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({url});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def add_login_bg_from_local(image_file):
    """
    Add a background image from a local file to the login page
    """
    try:
        with open(image_file, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{data}");
                background-size: cover;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.warning(f"Error loading background image: {e}")
        # Fall back to a default URL
        add_login_bg_from_url("https://cdn.pixabay.com/photo/2020/07/08/04/12/work-5382501_1280.jpg")

def create_login_card_style():
    """
    Create a card-like container for the login form
    """
    st.markdown(
        """
        <style>
       /* Main Background and Application Styling */
.stApp {
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}

/* Add a subtle overlay to improve text readability over background */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.5) 100%);
    z-index: -1;
}

/* Login Card Styling with Glass Effect */
div[data-testid="stForm"] {
    background-color: rgba(0, 0, 0, 0.75) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
    padding: 30px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    margin-bottom: 20px !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stForm"]:hover {
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3) !important;
    transform: translateY(-2px) !important;
}

/* Form Input Fields */
div[data-testid="stTextInput"] input, 
div[data-testid="stTextInput"] textarea {
    background-color: rgba(255, 255, 255, 0.07) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 6px !important;
    color: white !important;
    padding: 12px !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stTextInput"] input:focus, 
div[data-testid="stTextInput"] textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
}

/* Label Text */
div[data-testid="stTextInput"] label {
    color: #E5E7EB !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
}

/* Form Submit Button */
div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    height: 48px !important;
    text-transform: uppercase !important;
    font-size: 0.9rem !important;
}

div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stForm"] button[kind="primaryFormSubmit"]:active {
    transform: translateY(1px) !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4) !important;
}

/* Checkbox styling */
div[data-testid="stCheckbox"] {
    color: #E5E7EB !important;
}

div[data-testid="stCheckbox"] label {
    color: #E5E7EB !important;
    font-size: 0.95rem !important;
}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    background-color: rgba(0, 0, 0, 0.5) !important;
    backdrop-filter: blur(8px) !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 5px 5px 0 5px !important;
    border-bottom: none !important;
}

.stTabs [data-baseweb="tab"] {
    height: 50px !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    color: #E5E7EB !important;
    background-color: rgba(0, 0, 0, 0.2) !important;
    margin-right: 4px !important;
    transition: all 0.2s ease !important;
    border: none !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: rgba(0, 0, 0, 0.75) !important;
    color: white !important;
    border-bottom: 3px solid #3B82F6 !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(0, 0, 0, 0.4) !important;
    color: white !important;
}

/* Header styling */
h1 {
    font-family: 'Poppins', sans-serif !important;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8) !important;
    letter-spacing: 1px !important;
}

h1, h2, h3, .stSubheader {
    color: white !important;
    font-weight: 600 !important;
}

.stSubheader {
    font-size: 1.3rem !important;
    margin-bottom: 20px !important;
    text-align: center !important;
    color: #E5E7EB !important;
}

/* Success and Error Messages */
.stSuccess, .stError {
    border-radius: 8px !important;
    padding: 12px 16px !important;
    font-weight: 500 !important;
    margin: 10px 0 !important;
}

.stSuccess {
    background-color: rgba(16, 185, 129, 0.2) !important;
    border-left: 4px solid #10B981 !important;
}

.stError {
    background-color: rgba(239, 68, 68, 0.2) !important;
    border-left: 4px solid #EF4444 !important;
}

/* Spinner customization */
.stSpinner > div {
    border-color: #3B82F6 transparent transparent !important;
}

/* Footer styling */
footer {
    color: rgba(255, 255, 255, 0.7) !important;
    text-align: center !important;
    margin-top: 30px !important;
    padding: 15px !important;
    font-size: 0.9rem !important;
    border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* Remove default Streamlit footer */
footer.css-1lsmgbg,
footer.css-12ttj6m {
    display: none !important;
}

/* Responsiveness */
@media (max-width: 768px) {
    div[data-testid="stForm"] {
        padding: 20px !important;
    }
    
    h1 {
        font-size: 1.8rem !important;
    }
    
    .stSubheader {
        font-size: 1.1rem !important;
    }
}
        </style>
        """,
        unsafe_allow_html=True
    )

def show_login_page():
    # Initialize database if it hasn't been already
    if "db_initialized" not in st.session_state:
        db_init_success = init_database()
        st.session_state.db_initialized = db_init_success
        
        # If database initialization failed, show a retry button
        if not db_init_success:
            st.error("La connexion à la base de données a échoué.")
            if st.button("Réessayer"):
                st.session_state.db_initialized = init_database()
                st.rerun()
    
    # Add custom CSS to hide sidebar only on login page
    add_login_page_css()
    
    # Try to use local background image with relative path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bg_image_path = os.path.join(parent_dir, "images", "3139256.jpg")
    
    try:
        add_login_bg_from_local(bg_image_path)
    except:
        # Fallback to a URL
        add_login_bg_from_url("https://cdn.pixabay.com/photo/2020/07/08/04/12/work-5382501_1280.jpg")
    
    # Add card-like styling for the login container
    create_login_card_style()
    
    # App layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Add a logo or title image if available
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">Analyse de Données</h1>
            <p style="color: #ffffff; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">Application professionnelle d'analyse et préparation des données</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for login and sign up
        tab1, tab2 = st.tabs(["Connexion", "Créer un compte"])
        
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                st.subheader("Veuillez vous connecter")
                username = st.text_input("Nom d'utilisateur", key="login_username")
                password = st.text_input("Mot de passe", type="password", key="login_password")
                cols = st.columns([3, 1])
                
                with cols[0]:
                    submitted = st.form_submit_button("Se connecter")
                with cols[1]:
                    remember_me = st.checkbox("Se souvenir de moi")
                
                if submitted:
                    if not username or not password:
                        st.error("Veuillez saisir votre nom d'utilisateur et mot de passe.")
                    else:
                        # Show a spinner while authenticating
                        with st.spinner("Connexion en cours..."):
                            # Add a small delay to show the spinner (optional)
                            time.sleep(0.5)
                            auth_result = authenticate_user(username, password)
                        
                        if auth_result:
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.success("Connexion réussie!")
                            # Use javascript to reload the page without showing "rerun" message
                            st.markdown(
                                """
                                <script>
                                    setTimeout(function() {
                                        window.location.reload();
                                    }, 1000);
                                </script>
                                """,
                                unsafe_allow_html=True
                            )
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Nom d'utilisateur ou mot de passe invalide")
        
        with tab2:
            with st.form("signup_form", clear_on_submit=True):
                st.subheader("Créer un nouveau compte")
                new_username = st.text_input("Choisir un nom d'utilisateur", key="signup_username")
                new_password = st.text_input("Choisir un mot de passe", type="password", key="signup_password")
                confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="confirm_password")
                email = st.text_input("Email (optionnel)", key="signup_email")
                submitted_signup = st.form_submit_button("S'inscrire")
                
                if submitted_signup:
                    if not new_username or not new_password:
                        st.error("Veuillez remplir tous les champs obligatoires")
                    elif new_password != confirm_password:
                        st.error("Les mots de passe ne correspondent pas")
                    else:
                        with st.spinner("Création du compte..."):
                            time.sleep(0.5)
                            result = register_user(new_username, new_password, email)
                        
                        if result == "success":
                            st.success("Compte créé avec succès! Vous pouvez maintenant vous connecter.")
                            # Switch to login tab
                            st.markdown(
                                """
                                <script>
                                    setTimeout(function() {
                                        document.querySelector('[data-baseweb="tab"] div').click();
                                    }, 1500);
                                </script>
                                """,
                                unsafe_allow_html=True
                            )
                        elif result == "exists":
                            st.error("Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
                        else:
                            st.error("Une erreur s'est produite lors de la création du compte.")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 20px; color: white; text-shadow: 1px 1px 2px black;">
            <p>© 2025 Analyse de Données | Tous droits réservés</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display database connection status for debugging (can be removed in production)
        if os.environ.get("APP_ENV") == "development":
            if st.session_state.db_initialized:
                st.markdown('<div style="text-align: center; margin-top: 10px; color: #4CAF50; font-size: 0.8em;">Base de données connectée</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align: center; margin-top: 10px; color: #F44336; font-size: 0.8em;">Problème de connexion à la base de données</div>', unsafe_allow_html=True)