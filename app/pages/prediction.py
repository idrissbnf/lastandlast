# pages/prediction.py
import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import plotly.express as px

def show_page():
    st.title("🤖 Modèles Prédictifs")
    
    if st.session_state["df"] is not None:
        df = st.session_state["df"].copy()
        
        # Section de sélection des paramètres du modèle
        st.sidebar.markdown("## 🎛️ Paramètres du modèle")
        
        # Sélection de la variable cible
        target_col = st.sidebar.selectbox(
            "📌 Variable cible (Y)",
            df.columns
        )
        
        # Sélection des caractéristiques
        feature_cols = st.sidebar.multiselect(
            "📊 Caractéristiques (X)",
            [col for col in df.columns if col != target_col],
            default=[col for col in df.columns if col != target_col][:3]  # Par défaut, sélectionner les 3 premières colonnes
        )
        
        # Option pour le traitement des valeurs catégorielles
        handle_categorical = st.sidebar.checkbox("Encoder les variables catégorielles", value=True)
        
        # Type de modèle à utiliser
        model_type = st.sidebar.selectbox(
            "🧠 Type de modèle",
            ["Régression linéaire", "Classification logistique", "Arbre de décision"]
        )
        
        # Paramètres de validation
        test_size = st.sidebar.slider("Taille de l'ensemble de test (%)", 10, 50, 20) / 100
        
        # Affichage des informations et sélections
        st.markdown("""
        <div style="background-color:#1E3A8A; padding:15px; border-radius:10px; margin-bottom:20px;">
            <h1 style="color:white; text-align:center;">🤖 Modèles Prédictifs</h1>
            <p style="color:white; text-align:center;">Prédisez des résultats à partir de vos données</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Prévisualisation du jeu de données
        st.markdown("""
        <div style="background-color:#f8f9fa; padding:10px; border-radius:10px; margin-bottom:10px;">
            <h3 style="color:#1E3A8A; margin:0;">📊 Aperçu des données</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(df.head())
        
        # Section: Préparation des données
        st.markdown("""
        <div style="background-color:#f8f9fa; padding:10px; border-radius:10px; margin:20px 0 10px 0;">
            <h3 style="color:#1E3A8A; margin:0;">⚙️ Préparation des données</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Variable cible**: {target_col}")
            if target_col in df.columns:
                if pd.api.types.is_numeric_dtype(df[target_col].dtype):
                    st.write(f"Type: Numérique (moyenne: {df[target_col].mean():.2f})")
                else:
                    st.write(f"Type: Catégoriel ({len(df[target_col].unique())} catégories)")
        
        with col2:
            st.markdown(f"**Caractéristiques**: {len(feature_cols)} sélectionnées")
            st.write(f"Taille du jeu d'entraînement: {int((1-test_size)*100)}%")
            st.write(f"Taille du jeu de test: {int(test_size*100)}%")
        
        # Bouton pour lancer l'entraînement du modèle
        train_model = st.button("🚀 Entraîner le modèle", use_container_width=True)
        
        if train_model:
            st.markdown("""
            <div style="background-color:#f8f9fa; padding:10px; border-radius:10px; margin:20px 0 10px 0;">
                <h3 style="color:#1E3A8A; margin:0;">📈 Résultats du modèle</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulation de résultats (dans une application réelle, cette partie implémentera scikit-learn)
            with st.spinner("Entraînement du modèle en cours..."):
                time.sleep(2)  # Simule le temps d'entraînement
                
                # Affichage des métriques simulées
                met_col1, met_col2, met_col3, met_col4 = st.columns(4)
                
                with met_col1:
                    if model_type == "Régression linéaire":
                        st.metric("R² Score", "0.85")
                    else:
                        st.metric("Précision", "87%")
                
                with met_col2:
                    if model_type == "Régression linéaire":
                        st.metric("Erreur moyenne", "1.25")
                    else:
                        st.metric("Rappel", "0.82")
                
                with met_col3:
                    if model_type == "Régression linéaire":
                        st.metric("Erreur abs. moyenne", "0.95")
                    else:
                        st.metric("F1-Score", "0.84")
                
                with met_col4:
                    st.metric("Temps d'entraînement", "1.8s")
                
                # Graphique de résultats simulés
                st.markdown("### 📊 Visualisation des résultats")
                
                # Créer des données simulées pour les graphiques
                if model_type == "Régression linéaire":
                    x = np.linspace(0, 10, 100)
                    y_true = 2 * x + 1 + np.random.normal(0, 1, 100)
                    y_pred = 1.8 * x + 1.2
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x, y=y_true, mode='markers', name='Données réelles', marker=dict(color='blue')))
                    fig.add_trace(go.Scatter(x=x, y=y_pred, mode='lines', name='Prédictions', line=dict(color='red')))
                    
                    fig.update_layout(
                        title="Régression: Valeurs réelles vs prédites",
                        xaxis_title="Caractéristique",
                        yaxis_title="Valeur cible",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Afficher les erreurs de prédiction
                    errors = y_true - y_pred
                    fig_error = go.Figure()
                    fig_error.add_trace(go.Histogram(x=errors, marker_color='red'))
                    
                    fig_error.update_layout(
                        title="Distribution des erreurs",
                        xaxis_title="Erreur",
                        yaxis_title="Fréquence",
                        height=300
                    )
                    
                    st.plotly_chart(fig_error, use_container_width=True)
                    
                elif model_type in ["Classification logistique", "Arbre de décision"]:
                    # Simuler une matrice de confusion
                    conf_matrix = np.array([[42, 8], [6, 44]])
                    
                    fig = px.imshow(
                        conf_matrix,
                        text_auto=True,
                        labels=dict(x="Prédiction", y="Réalité"),
                        x=["Négatif", "Positif"],
                        y=["Négatif", "Positif"],
                        color_continuous_scale="Blues"
                    )
                    
                    fig.update_layout(
                        title="Matrice de confusion",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Simuler une courbe ROC
                    fpr = np.linspace(0, 1, 100)
                    tpr = np.sqrt(fpr)  # Courbe ROC simplifié (mieux que aléatoire)
                    
                    fig_roc = go.Figure()
                    fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name='Modèle', line=dict(color='blue', width=3)))
                    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Aléatoire', line=dict(color='red', dash='dash')))
                    
                    fig_roc.update_layout(
                        title="Courbe ROC",
                        xaxis_title="Taux de faux positifs",
                        yaxis_title="Taux de vrais positifs",
                        height=400,
                        xaxis=dict(range=[0, 1]),
                        yaxis=dict(range=[0, 1])
                    )
                    
                    st.plotly_chart(fig_roc, use_container_width=True)
                    
                    # Simuler l'importance des caractéristiques
                    feature_importance = np.random.uniform(0, 1, len(feature_cols))
                    feature_imp_df = pd.DataFrame({
                        'Caractéristique': feature_cols,
                        'Importance': feature_importance
                    }).sort_values('Importance', ascending=False)
                    
                    fig_imp = px.bar(
                        feature_imp_df,
                        x='Importance',
                        y='Caractéristique',
                        orientation='h',
                        title="Importance des caractéristiques",
                        color='Importance',
                        color_continuous_scale="Blues"
                    )
                    
                    st.plotly_chart(fig_imp, use_container_width=True)
                
                # Section: Faire une prédiction avec le modèle
                st.markdown("""
                <div style="background-color:#f8f9fa; padding:10px; border-radius:10px; margin:20px 0 10px 0;">
                    <h3 style="color:#1E3A8A; margin:0;">🔮 Faire une prédiction</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Création d'un formulaire pour les prédictions
                predict_col1, predict_col2 = st.columns(2)
                
                prediction_inputs = {}
                
                with predict_col1:
                    st.markdown("#### Entrez les valeurs des caractéristiques")
                    
                    # Pour chaque caractéristique sélectionnée, créer un champ d'entrée approprié
                    for feature in feature_cols[:len(feature_cols)//2 + len(feature_cols)%2]:
                        if feature in df.columns:
                            if pd.api.types.is_numeric_dtype(df[feature].dtype):
                                # Pour les caractéristiques numériques
                                min_val = float(df[feature].min())
                                max_val = float(df[feature].max())
                                default_val = float(df[feature].mean())
                                
                                prediction_inputs[feature] = st.number_input(
                                    f"{feature}",
                                    min_value=min_val,
                                    max_value=max_val,
                                    value=default_val,
                                    format="%.2f"
                                )
                            else:
                                # Pour les caractéristiques catégorielles
                                options = df[feature].unique().tolist()
                                prediction_inputs[feature] = st.selectbox(
                                    f"{feature}",
                                    options=options
                                )
                
                with predict_col2:
                    if len(feature_cols) > 1:
                        st.markdown("#### Entrez les valeurs des caractéristiques (suite)")
                        
                        # Continuer avec les caractéristiques restantes
                        for feature in feature_cols[len(feature_cols)//2 + len(feature_cols)%2:]:
                            if feature in df.columns:
                                if pd.api.types.is_numeric_dtype(df[feature].dtype):
                                    # Pour les caractéristiques numériques
                                    min_val = float(df[feature].min())
                                    max_val = float(df[feature].max())
                                    default_val = float(df[feature].mean())
                                    
                                    prediction_inputs[feature] = st.number_input(
                                        f"{feature}",
                                        min_value=min_val,
                                        max_value=max_val,
                                        value=default_val,
                                        format="%.2f"
                                    )
                                else:
                                    # Pour les caractéristiques catégorielles
                                    options = df[feature].unique().tolist()
                                    prediction_inputs[feature] = st.selectbox(
                                        f"{feature}",
                                        options=options
                                    )
                
                # Bouton pour effectuer la prédiction
                if st.button("🔮 Prédire", use_container_width=True):
                    with st.spinner("Calcul de la prédiction en cours..."):
                        time.sleep(1)  # Simuler le temps de calcul
                        
                        # Simulation d'une prédiction (dans une application réelle, utiliser le modèle entraîné)
                        if model_type == "Régression linéaire":
                            prediction_value = np.random.normal(df[target_col].mean(), df[target_col].std() / 3, 1)[0]
                            
                            st.success(f"**Prédiction**: {prediction_value:.2f}")
                            
                            # Afficher où se situe la prédiction dans la distribution des valeurs
                            fig_dist = go.Figure()
                            fig_dist.add_trace(go.Histogram(x=df[target_col], name="Distribution", marker_color="blue", opacity=0.7))
                            fig_dist.add_trace(go.Scatter(x=[prediction_value, prediction_value], y=[0, df[target_col].value_counts().max() / 2],
                                            mode="lines", name="Prédiction", line=dict(color="red", width=3, dash="dash")))
                            
                            fig_dist.update_layout(
                                title=f"Positionnement de la prédiction ({prediction_value:.2f})",
                                xaxis_title=target_col,
                                yaxis_title="Fréquence",
                                height=300
                            )
                            
                            st.plotly_chart(fig_dist, use_container_width=True)
                            
                        else:  # Pour les modèles de classification
                            # Simulation d'une classification avec probabilités
                            classes = ["Classe A", "Classe B"] if len(df[target_col].unique()) <= 2 else ["Classe A", "Classe B", "Classe C"]
                            probs = np.random.dirichlet(np.ones(len(classes)), size=1)[0]
                            predicted_class = classes[np.argmax(probs)]
                            
                            st.success(f"**Classe prédite**: {predicted_class}")
                            
                            # Afficher les probabilités de chaque classe
                            fig_probs = go.Figure()
                            fig_probs.add_trace(go.Bar(
                                x=classes,
                                y=probs,
                                marker_color=["blue" if i == np.argmax(probs) else "lightblue" for i in range(len(classes))],
                                text=[f"{p:.1%}" for p in probs],
                                textposition="auto"
                            ))
                            
                            fig_probs.update_layout(
                                title="Probabilités par classe",
                                xaxis_title="Classe",
                                yaxis_title="Probabilité",
                                height=300,
                                yaxis=dict(range=[0, 1])
                            )
                            
                            st.plotly_chart(fig_probs, use_container_width=True)
                
                # Section: Exportation du modèle (simulée)
                st.markdown("""
                <div style="background-color:#f8f9fa; padding:10px; border-radius:10px; margin:20px 0 10px 0;">
                    <h3 style="color:#1E3A8A; margin:0;">💾 Exporter le modèle</h3>
                </div>
                """, unsafe_allow_html=True)
                
                export_options = st.radio("Format d'exportation:", ["Fichier pickle (.pkl)", "ONNX (.onnx)", "TensorFlow SavedModel (.tf)"], horizontal=True)
                
                if st.button("📥 Télécharger le modèle"):
                    # Simuler un téléchargement
                    st.success("Le modèle a été préparé pour le téléchargement!")
                    
                    st.download_button(
                        label="Télécharger le modèle",
                        data="Ceci est un modèle fictif",  # Dans une application réelle, ce serait le modèle sérialisé
                        file_name=f"modele_{model_type.lower().replace(' ', '_')}.pkl",
                        mime="application/octet-stream"
                    )
    else:
        st.info("Aucune donnée chargée. Veuillez charger un fichier depuis la page d'accueil.")