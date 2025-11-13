# app_bacteries_souchier.py
# Application Streamlit pour consulter le souchier de bactéries
# Chargement des données depuis GitHub

import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Souchier Bactéries",
    page_icon="🧫",
    layout="wide"
)

# Titre principal
st.title("🧫 Souchier de Bactéries - Gestion des Souches")
st.markdown("---")

# URL du fichier CSV sur GitHub (version Raw)
CSV_URL = "https://raw.githubusercontent.com/Phoenix4012/Souchier/main/bacteries_souchier.csv"

@st.cache_data
def load_data():
    """Charge les données des bactéries depuis GitHub"""
    try:
        df = pd.read_csv(CSV_URL, encoding='utf-8')
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

# Charger les données
df = load_data()

# Vérifier que les données ont été chargées
if df.empty:
    st.error("⚠️ Impossible de charger les données. Vérifiez l'URL du fichier CSV.")
    st.stop()

# Section des filtres dans la barre latérale
st.sidebar.header("🔍 Filtres de recherche")

# Filtre par type de bactérie
type_selection = st.sidebar.multiselect(
    "**Sélectionner le type de micro-organisme:**",
    options=sorted(df['Type'].unique().tolist()),
    default=[],
    help="Choisissez un ou plusieurs types pour filtrer les résultats"
)

# Filtre par besoin de repiquage
st.sidebar.markdown("---")
repiquage_options = st.sidebar.radio(
    "**Besoin de repiquage:**",
    options=["Tous", "Oui", "Non"],
    index=0,
    help="Filtrer selon le besoin de repiquage"
)

# Filtre de recherche par nom
st.sidebar.markdown("---")
search_term = st.sidebar.text_input(
    "**Rechercher par nom:**",
    placeholder="Ex: Escherichia, Candida...",
    help="Recherche partielle dans le nom de la bactérie"
)

# Application des filtres
df_filtered = df.copy()

# Filtre par type
if type_selection:
    df_filtered = df_filtered[df_filtered['Type'].isin(type_selection)]

# Filtre par repiquage
if repiquage_options != "Tous":
    df_filtered = df_filtered[df_filtered['Repiquage_Necessaire'] == repiquage_options]

# Filtre par nom
if search_term:
    df_filtered = df_filtered[
        df_filtered['Nom_Bacterie'].str.contains(search_term, case=False, na=False)
    ]

# Affichage des statistiques
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Statistiques")
st.sidebar.metric("Souches totales dans la base", len(df))
st.sidebar.metric("Souches filtrées", len(df_filtered))

# Lien vers le dépôt GitHub
st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 Source des données")
st.sidebar.markdown("[Voir le fichier CSV sur GitHub](https://github.com/Phoenix4012/Souchier)")

# Section principale - Résultats
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Résultats de la recherche")

with col2:
    if len(df_filtered) > 0:
        # Bouton pour télécharger les résultats
        csv = df_filtered.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Télécharger (CSV)",
            data=csv,
            file_name="souches_filtrees.csv",
            mime="text/csv"
        )

# Affichage conditionnel
if len(type_selection) == 0 and search_term == "" and repiquage_options == "Tous":
    st.info("👈 **Utilisez les filtres dans la barre latérale** pour afficher les souches du souchier.")
    
    # Afficher un aperçu des statistiques globales
    st.markdown("### 📊 Vue d'ensemble du souchier")
    
    # Calculer les statistiques par type
    type_counts = df['Type'].value_counts().to_dict()
    
    # Créer des colonnes dynamiques selon les types disponibles
    types_disponibles = sorted(df['Type'].unique())
    cols = st.columns(len(types_disponibles))
    
    for idx, type_name in enumerate(types_disponibles):
        with cols[idx]:
            st.metric(type_name, type_counts.get(type_name, 0))
    
elif len(df_filtered) == 0:
    st.warning("⚠️ Aucune souche ne correspond à vos critères de recherche.")
    st.info("Essayez de modifier vos filtres pour élargir la recherche.")
    
else:
    # Afficher le nombre de résultats
    st.success(f"✅ **{len(df_filtered)} souche(s)** trouvée(s)")
    
    # Afficher le tableau de résultats avec style
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Type": st.column_config.TextColumn(
                "Type",
                width="small",
            ),
            "Nom_Bacterie": st.column_config.TextColumn(
                "Nom de la bactérie",
                width="large",
            ),
            "Lieu_Souchier": st.column_config.TextColumn(
                "Emplacement",
                width="small",
            ),
            "Repiquage_Necessaire": st.column_config.TextColumn(
                "Repiquage",
                width="small",
            ),
        }
    )
    
    # Section d'informations détaillées
    with st.expander("📖 Informations détaillées sur les souches affichées"):
        repiquage_oui = len(df_filtered[df_filtered['Repiquage_Necessaire'] == 'Oui'])
        repiquage_non = len(df_filtered[df_filtered['Repiquage_Necessaire'] == 'Non'])
        
        st.markdown(f"""
        **Résumé:**
        - Souches nécessitant un repiquage: **{repiquage_oui}**
        - Souches ne nécessitant pas de repiquage: **{repiquage_non}**
        """)
        
        if type_selection:
            st.markdown(f"**Types sélectionnés:** {', '.join(type_selection)}")

# Pied de page
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    Application de gestion du souchier de bactéries - Version 2.0<br>
    💡 Astuce: Utilisez plusieurs filtres simultanément pour affiner votre recherche<br>
    📡 Données chargées depuis GitHub
</div>
""", unsafe_allow_html=True)
