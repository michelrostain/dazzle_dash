# **Dazzle Dash - Analyse et dashboarding d'une base de données**     

Nous allons ici analyser une base de données raltives à l'espérance de vie dans le monde, à travers des facteurs sanitaires, socio-économiques et démographique.     
Pour ce faire nous utilisons une base de données en libre accès : Life Expectancy Data (WHO).     

Dans le cadre de cette analyse de données, nous allons mettre en place une première phase constituée des 3 axes suivants :    
- Analyse descriptives de la base de donnée : type de données, nombre de cases vides, nombre de case à  zéro, etc. Le tout mis en forme dans une fichier Jupyter.     
- Veille technologiques sur les outils à utiliser pour le dashboard : Dash, Python. Résumé du projet. le tout mis en forme dans ce readme.md     
- Construction de l'architecture technique : composants UI, Interactivité (callback), exécution sur un serveur local ou distant.     

## **Phase 1**     

### **<u>1) Analyse descriptive de la base de donnée</u>**     
Notre base de donnée possède 22 colonnes et 2938 lignes.     
Les données concernent les catégories suivantes :       
- Socio économiques (Status, GDP (PIB), percentage expenditure, total expenditure, income expedition of ressources).     
- Santé : le taux de vaccination, consommation d'aclcool, mortalité.     
- Population      

En terme de données manquantes, la plupart des colonnes se trouvent à moins de 6% de données manquantes. En revanche, les colonnes avec 15, 18 et 22% ((GDP, Hepatis B, Population) de données manquantes ne seront pas prises en compte dans nos maniplations du DATASET pour des tendances mondiales.    

les deux pays qui ont le plus de données manquantes sont le Soudan et le Soudan du Sud.     

<b>Signification des titres de colonnes :</b>    
* Country : Le pays concerné par l'observation (193 pays au total).    
* Year : L'année de collecte de la donnée (de 2000 à 2015).    
* Status : Statut de développement du pays ("Developed" pour développé, "Developing" pour en développement).    
* Life expectancy : L'espérance de vie à la naissance (exprimée en années).    
* Adult Mortality : Le taux de mortalité des adultes. Probabilité de mourir entre 15 et 60 ans pour 1 000 personnes.    
* infant deaths : Le nombre de décès d'enfants de moins d'un an pour 1 000 naissances.    
* Alcohol : Consommation d'alcool par habitant mesurée en litres d'alcool pur (pour les plus de 15 ans).    
* percentage expenditure : Dépenses de santé en pourcentage du Produit Intérieur Brut (PIB) par habitant (Attention: contient des anomalies de calcul et des valeurs en dollars).    
* Hepatitis B : Taux de couverture vaccinale contre l'Hépatite B chez les enfants de 1 an (exprimé en %).    
* Measles : Nombre de cas de rougeole signalés pour 1 000 habitants.    
* BMI : Indice de Masse Corporelle (IMC) moyen de l'ensemble de la population du pays.    
* under-five deaths : Le nombre de décès d'enfants de moins de 5 ans pour 1 000 naissances.    
* Polio : Taux de couverture vaccinale contre la polio chez les enfants de 1 an (exprimé en %).    
* Total expenditure : Dépenses générales de santé publique en pourcentage des dépenses totales du gouvernement.    
* Diphtheria : Taux de couverture vaccinale contre la diphtérie, le tétanos et la coqueluche (DTP3) chez les enfants de 1 an (exprimé en %).    
* HIV/AIDS : Nombre de décès dus au VIH/SIDA pour 1 000 naissances vivantes d'enfants (de 0 à 4 ans).    
* GDP : Produit Intérieur Brut (PIB) par habitant (exprimé en USD).
* Population : Population totale du pays.    
* thinness 1-19 years : Prévalence de la minceur/maigreur chez les enfants et adolescents de 1 à 19 ans (exprimé en %).    
* thinness 5-9 years : Prévalence de la minceur/maigreur spécifiquement chez les enfants de 5 à 9 ans (exprimé en %).    
* Income composition of resources : L'Indice de Développement Humain (IDH ou HDI) basé sur la composition des revenus (échelle allant de 0 à 1).    
* Schooling : Le nombre moyen d'années de scolarisation de la population.    


### **<u>2) Veille technologique</u>**     
2.1) <u>Dash by plotly</u>     
Dash est un framework Python spécialisé dans la création d'applications web et de dashboards.

