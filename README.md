# Dataset Analytics Dashboard

Application web interactive d'analyse de données supportant **2 types de datasets** :
- 🛒 **Shopping Trends** : Analyse des tendances de consommation
- 🏠 **Airbnb Open Data** : Analyse des locations Airbnb

Développé avec **Streamlit**, **DuckDB**, **Pandas** et **Plotly**.

# Fonctionnalités

### Détection Automatique de Dataset

L'application détecte automatiquement si vous uploadez :
- 🛒 Un dataset **Shopping Trends**
- 🏠 Un dataset **Airbnb**

Et adapte automatiquement :
- Les colonnes utilisées (date, région, produit, montant, note)
- Les KPIs affichés
- Les filtres disponibles

---

### 4 Visualisations Principales

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

---

### 📌 KPIs de Synthèse

4 métriques clés affichées en haut du dashboard :
- **Lignes** : Nombre d'enregistrements (après filtres)
- **Total** : Somme des montants
- **Moyenne** : Montant moyen
- **Note moyenne** : Rating moyen

---

### 🔎 Filtres Dynamiques

Les filtres s'adaptent selon le dataset :

**Filtres disponibles :**
- 📅 **Plage de dates** (si colonne date disponible)
- 🌍 **Régions** (multi-sélection, 5 par défaut)
- 🧾 **Produits** (multi-sélection, 5 par défaut)
- 🔄 **Bouton Reset** pour réinitialiser tous les filtres

**Les graphiques se mettent à jour en temps réel** selon les filtres appliqués.

---

