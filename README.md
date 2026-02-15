# Dataset Analytics Dashboard

Application web interactive d'analyse de données supportant **2 types de datasets** :
- 🛒 **Shopping Trends** : Analyse des tendances de consommation
- 🏠 **Airbnb Open Data** : Analyse des locations Airbnb

Développé avec **Streamlit**, **DuckDB**, **Pandas** et **Plotly**.

## ✨ Fonctionnalités

### 🔍 Détection Automatique de Dataset

L'application détecte automatiquement si vous uploadez :
- 🛒 Un dataset **Shopping Trends**
- 🏠 Un dataset **Airbnb**

Et adapte automatiquement :
- Les colonnes utilisées (date, région, produit, montant, note)
- Les KPIs affichés
- Les filtres disponibles

### 📊 4 Visualisations Principales

#### 📈 1. Évolution Mensuelle (Onglet "Évolution")
- **Graphique linéaire** avec marqueurs
- **Shopping** : Somme des montants par mois
- **Airbnb** : Prix moyen par mois
- Labels automatiques sur les points min, max et dernier

#### 🌍 2. Top Régions (Onglet "Régions")
- **Graphique en barres** des 10 meilleures régions
- Tri par montant total (ou par nombre de lignes si pas de montant)

#### 🧾 3. Top Produits (Onglet "Produits")
- **Graphique en barres** des 10 meilleurs produits
- Tri par montant total (ou par nombre de lignes si pas de produit)

#### ⭐ 4. Distribution des Notes (Onglet "Notes")
- **Histogramme** de la répartition des ratings

### 📌 KPIs de Synthèse

4 métriques clés affichées en haut du dashboard :
- **Lignes** : Nombre d'enregistrements (après filtres)
- **Total** : Somme des montants
- **Moyenne** : Montant moyen
- **Note moyenne** : Rating moyen

### 🔎 Filtres Dynamiques

Les filtres s'adaptent selon le dataset :

**Filtres disponibles :**
- 📅 **Plage de dates** (si colonne date disponible)
- 🌍 **Régions** (multi-sélection, 5 par défaut)
- 🧾 **Produits** (multi-sélection, 5 par défaut)
- 🔄 **Bouton Reset** pour réinitialiser tous les filtres

**Les graphiques se mettent à jour en temps réel** selon les filtres appliqués.

## 🚀 Installation et Exécution

### Prérequis
- Python 3.10+
- pip

### Installation Rapide
```bash
# 1. Télécharger le projet
# Cliquer sur le bouton vert "Code" → "Download ZIP"
# Extraire le fichier ZIP dans un dossier de votre choix

# 2. Ouvrir un terminal dans le dossier extrait
cd dataset-analytics-main

# 3. Créer un environnement virtuel
python -m venv venv

# 4. Activer l'environnement
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 5. Installer les dépendances
pip install -r requirements.txt

# 6. Lancer l'application
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à `http://localhost:8501`

### Utilisation

1. **Télécharger un dataset** depuis Kaggle :
   - [Shopping Trends](https://www.kaggle.com/datasets/zeesolver/consumer-behavior-and-shopping-habits-dataset)
   - [Airbnb Open Data](https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata)

2. **Dans l'application** :
   - Cliquer sur "Téléverser un CSV" dans la sidebar
   - Sélectionner le fichier téléchargé
   - Explorer les 4 onglets de visualisation
   - Utiliser les filtres pour affiner l'analyse

3. **Arrêter l'application** : `Ctrl+C` dans le terminal

