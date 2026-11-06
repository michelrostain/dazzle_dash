# **Dazzle Dash - Analyse et dashboarding d'une base de données**     

Nous allons ici analyser une base de données raltives à l'espérance de vie dans le monde, à travers des facteurs sanitaires, socio-économiques et démographique.     
Pour ce faire nous utilisons une base de données en libre accès : Life Expectancy Data (WHO).     

Dans le cadre de cette analyse de données, nous allons mettre en place une première phase constituée des 3 axes suivants :    
- Analyse descriptives de la base de donnée : type de données, nombre de cases vides, nombre de case à  zéro, etc. Le tout mis en forme dans une fichier Jupyter.     
- Veille technologiques sur les outils à utiliser pour le dashboard : Dash, Python. Résumé du projet. le tout mis en forme dans ce readme.md     
- Construction de l'architecture technique : composants UI, Interactivité (callback), exécution sur un serveur local ou distant.     

## **Phase 1**     

### **<u>1) Analyse descriptive de la base de donnée</u>**     

**1.1) Description de la base de données**     
Notre base de donnée possède 22 colonnes et 2938 lignes.     
Les données concernent les catégories suivantes :       
- Socio économiques (Status, GDP (PIB), percentage expenditure, total expenditure, income expedition of ressources).     
- Santé : le taux de vaccination, consommation d'aclcool, mortalité.     
- Population      

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
* under-five deaths : Le nombre de décès d'enfants de moins de 5 ans en milliers.    
* Polio : Taux de couverture vaccinale contre la polio chez les enfants de 1 an (exprimé en %).    
* Total expenditure : Dépenses générales de santé publique en pourcentage des dépenses totales du gouvernement.    
* Diphtheria : Taux de couverture vaccinale contre la diphtérie, le tétanos et la coqueluche (DTP3) chez les enfants de 1 an (exprimé en %).    
* HIV/AIDS : Nombre de décès dus au VIH/SIDA pour 1 000 naissances vivantes d'enfants (de 0 à 4 ans).    
* GDP : Produit Intérieur Brut (PIB) par habitant (exprimé en USD).
* Population : Population totale du pays.    
* thinness 1-19 years : Prévalence de la minceur/maigreur chez les enfants et adolescents de 10 à 19 ans (exprimé en %).    
* thinness 5-9 years : Prévalence de la minceur/maigreur spécifiquement chez les enfants de 5 à 9 ans (exprimé en %).    
* Income composition of resources : L'Indice de Développement Humain (IDH ou HDI) basé sur la composition des revenus (échelle allant de 0 à 1).    
* Schooling : Le nombre moyen d'années de scolarisation de la population.    

**2) Suppression des données non pertinentes**     
Dans la mesure ou toutes les colonnes ont moins de 22% de données manquantes, nous allons considérer chaque colonnes afin de voir si les données sont pertinentes. Nous gèrerons aussi les case vides et les données aberrantes.     
Dans un premier temps nous calculons le ratio par pays : (valeur de la ligne) / (Médiane des valeurs de ce pays).     
Ensuite nous répartissons les ratios de chaque pays dans un histogramme et un rapport écris (en terminal) et faisons notre choix du ratio idéal et l'apploquons dans le code du fichier graph.py.

Là où le ratio ne marche pas : 
Valeurs trop petites ou arrondies : under-five deaths, pour 111 pays.
Variations naturelles énormes : Measles, où une épidémie multiplie le nombre de cas par 100.
Médiane non représentative : séries en tendance ou corrompues, comme India pour Hepatitis B ou Montenegro pour Alcohol. Cela arrive aussi sur des taux.     
Il n’y a pas de règle « nombres de cas : on ne touche à rien ». La règle du document est la même pour tous les types de colonnes : on ne corrige que s’il existe un schéma d’erreur qu’on peut prouver (chiffre perdu, valeur par défaut, zéro qui code un manquant). Pour Measles et under-five deaths, on n’en trouve aucun, donc on laisse les données telles quelles.     

Médiane : un seuil unique par colonne, valable tant que la médiane du pays est représentative ; les pays où elle ne l’est pas sont documentés comme limites connues

<u>2.1) Colonne Adult Mortality</u>   


### **<u>2) Veille technologique</u>**     
2.1) <u>Dash by plotly</u>     
Dash est un framework Python spécialisé dans la création d'applications web et de dashboards.

