# app_bacteries_souchier.py
# Application Streamlit pour consulter le souchier de bactéries
# Filtrage par type (GRAM+, GRAM-, Champignon, Levure)

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

# Charger les données depuis le CSV
# Si vous utilisez un fichier local, remplacez par le chemin de votre fichier
# Pour cet exemple, nous recréons les données directement dans le code

@st.cache_data
def load_data():
    """Charge les données des bactéries"""
    bacteria_data = {
        "Type": [
            # Gram positif - Cocci
            "GRAM+", "GRAM+", "GRAM+", "GRAM+", "GRAM+", "GRAM+",
            # Gram positif - Bacilles
            "GRAM+", "GRAM+", "GRAM+", "GRAM+", "GRAM+", "GRAM+", "GRAM+", "GRAM+",
            # Gram négatif - Cocci
            "GRAM-", "GRAM-",
            # Gram négatif - Bacilles (Entérobactéries)
            "GRAM-", "GRAM-", "GRAM-", "GRAM-", "GRAM-", "GRAM-", "GRAM-", "GRAM-",
            # Gram négatif - Bacilles (Autres)
            "GRAM-", "GRAM-", "GRAM-", "GRAM-", "GRAM-",
            # Levures
            "Levure", "Levure", "Levure", "Levure", "Levure", "Levure",
            # Champignons
            "Champignon", "Champignon", "Champignon", "Champignon", "Champignon"
        ],
        "Nom_Bacterie": [
            # Gram positif - Cocci
            "Staphylococcus aureus",
            "Staphylococcus epidermidis",
            "Streptococcus pneumoniae",
            "Streptococcus pyogenes",
            "Enterococcus faecalis",
            "Enterococcus faecium",
            # Gram positif - Bacilles
            "Bacillus anthracis",
            "Bacillus cereus",
            "Bacillus subtilis",
            "Listeria monocytogenes",
            "Corynebacterium diphtheriae",
            "Clostridium tetani",
            "Clostridium botulinum",
            "Clostridium perfringens",
            # Gram négatif - Cocci
            "Neisseria meningitidis",
            "Neisseria gonorrhoeae",
            # Gram négatif - Bacilles (Entérobactéries)
            "Escherichia coli",
            "Salmonella typhimurium",
            "Shigella sonnei",
            "Klebsiella pneumoniae",
            "Proteus mirabilis",
            "Enterobacter cloacae",
            "Serratia marcescens",
            "Yersinia enterocolitica",
            # Gram négatif - Bacilles (Autres)
            "Pseudomonas aeruginosa",
            "Acinetobacter baumannii",
            "Legionella pneumophila",
            "Haemophilus influenzae",
            "Campylobacter jejuni",
            # Levures
            "Saccharomyces cerevisiae",
            "Candida albicans",
            "Candida glabrata",
            "Cryptococcus neoformans",
            "Pichia pastoris",
            "Debaryomyces hansenii",
            # Champignons
            "Aspergillus fumigatus",
            "Aspergillus niger",
            "Penicillium chrysogenum",
            "Fusarium oxysporum",
            "Trichoderma reesei"
        ],
        "Lieu_Souchier": [
            # Gram positif
            "A-1", "A-2", "A-3", "A-4", "A-5", "A-6",
            "B-1", "B-2", "B-3", "B-4", "B-5", "B-6", "B-7", "B-8",
            # Gram négatif
            "C-1", "C-2",
            "D-1", "D-2", "D-3", "D-4", "D-5", "D-6", "D-7", "D-8",
            "E-1", "E-2", "E-3", "E-4", "E-5",
            # Levures
            "F-1", "F-2", "F-3", "F-4", "F-5", "F-6",
            # Champignons
            "G-1", "G-2", "G-3", "G-4", "G-5"
        ],
        "Repiquage_Necessaire": [
            # Gram positif
            "Oui", "Oui", "Oui", "Oui", "Non", "Non",
            "Oui", "Oui", "Non", "Oui", "Oui", "Oui", "Oui", "Oui",
            # Gram négatif
            "Oui", "Oui",
            "Oui", "Oui", "Oui", "Oui", "Non", "Non", "Non", "Oui",
            "Oui", "Oui", "Oui", "Non", "Oui",
            # Levures
            "Non", "Oui", "Oui", "Oui", "Non", "Non",
            # Champignons
            "Oui", "Non", "Non", "Oui", "Non"
        ]
    }
    return pd.DataFrame(bacteria_data)

# Charger les données
df = load_data()

# Section des filtres dans la barre latérale
st.sidebar.header("🔍 Filtres de recherche")

# Filtre par type de bactérie
type_selection = st.sidebar.multiselect(
    "**Sélectionner le type de micro-organisme:**",
    options=df['Type'].unique().tolist(),
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
    
    col_a, col_b, col_c, col_d = st.columns(4)
    
    with col_a:
        st.metric("GRAM+", len(df[df['Type'] == 'GRAM+']))
    with col_b:
        st.metric("GRAM-", len(df[df['Type'] == 'GRAM-']))
    with col_c:
        st.metric("Levures", len(df[df['Type'] == 'Levure']))
    with col_d:
        st.metric("Champignons", len(df[df['Type'] == 'Champignon']))
    
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
    Application de gestion du souchier de bactéries - Version 1.0<br>
    💡 Astuce: Utilisez plusieurs filtres simultanément pour affiner votre recherche
</div>
""", unsafe_allow_html=True)
