# Guide du pitch oral : Dashboard Premier League (5 minutes)

Format : 5 minutes de presentation + 5 minutes de questions / reponses
Equipe : Ayoub AZACRI, Youssef EL HAJJI, Omar HAKIK, Youssef DEKHAIL

## Structure du temps (1 min 15 par membre)

| Membre | Partie prise en charge | Duree |
| :--- | :--- | :--- |
| Youssef EL HAJJI | 1. Introduction, audience cible et message cle Minto | 1 min 15 |
| Ayoub AZACRI | 2. Architecture des donnees, cache et selection des KPIs | 1 min 15 |
| Omar HAKIK | 3. Demonstration de la matrice d'efficacite offensive | 1 min 15 |
| Youssef DEKHAIL | 4. Le 12e Homme, simulateur tactique et synthese | 1 min 15 |

## 1. Youssef EL HAJJI : Cadrage et pyramide de Minto (00:00 - 01:15)

"Bonjour a tous. Aujourd'hui, nous nous placons dans la posture d'un cabinet de conseil sportif mandate par la direction technique d'un club de Premier League.

Notre mandat n'etait pas de produire un catalogue de chiffres, mais d'apporter une reponse a une question strategique : comment optimiser le rendement offensif sans tomber dans le piege des vanity metrics ?

Notre message cle Minto tient en une phrase :
L'efficacite au cadrage et la conversion clinique des tirs determinent le succes sportif bien plus que l'accumulation de frappes steriles.

Pour servir cette audience exigeante, nous avons concu un tableau de bord decisionnel multi-pages sous Streamlit, structure pour livrer l'essentiel en moins de 5 secondes."

## 2. Ayoub AZACRI : Qualite des donnees et KPIs actionnables (01:15 - 02:30)

"Pour asseoir cette analyse, nous nous appuyons sur 1 900 rencontres de Premier League sur 5 saisons completes, de 2019 a 2024.

Au niveau technique, nous appliquons le decorateur `@st.cache_data` pour garantir une fluidite totale sous les 100 millisecondes lors des filtrages multi-saisons.

Sur la page d'accueil, nous avons deliberement banni la vanity metric universelle du football : le total brut de tirs. Multiplier les tirs lointains hors cadre rassure le public mais penalise l'equipe en alimentant les contre-attaques adverses.

Nous avons retenu trois indicateurs purement actionnables :
Le taux de cadrage net, qui mesure la qualite du choix de tir ;
Le taux de conversion clinique, qui isole le sang-froid face au but ;
Et les points engranges par tir cadre, qui mesurent la rentabilite comptable directe."

## 3. Omar HAKIK : Demonstration du quadrant d'efficacite (02:30 - 03:45)

"Sur notre premier volet detaille, nous croisons ces deux dimensions dans une matrice tactique en quatre quadrants.

Ce graphique repond au principe des canaux pre-attentifs : les seuils medians separent instantanement l'elite des equipes en difficulte.

En haut a droite, la zone chirurgicale regroupe Manchester City, Arsenal et Liverpool, qui allient plus de 35 % de cadrage et 33 % de conversion.
A l'oppose, nous identifions le profil des equipes volumineuses : beaucoup de frappes tentees, mais une finition sterile qui les maintient en milieu de tableau.

Pour la cellule de recrutement, ce quadrant est un outil de decision direct pour cibler des attaquants rentables plutot que de simples accumulateurs de tirs."

## 4. Youssef DEKHAIL : Le 12e Homme et simulateur tactique (03:45 - 05:00)

"Notre second volet explore l'experience naturelle du huis clos lors de la saison COVID 2020-21.
Les donnees prouvent la realite statistique du 12e Homme : sans supporters, le taux de victoires a domicile s'est effondre de 8,3 points, passant sous la barre des victoires a l'exterieur pour la premiere fois de l'histoire moderne.

Enfin, notre simulateur tactique permet au coach d'anticiper une confrontation donnee en pondérant les forces d'attaque, la resistance defensive et l'effet terrain.

En conclusion, ce dashboard transforme 5 ans de donnees brutes en un levier d'action concret pour les decideurs du football professionnel. Nous sommes a votre disposition pour vos questions."

## Reponses aux questions probables du jury

* Pourquoi ne pas avoir inclus les Expected Goals (xG) ?
Reponse : Le dataset officiel football-data.co.uk fournit les tirs et tirs cadres fiables sur 1 900 matchs. Notre ratio Buts / Tir cadre et notre indice de cadrage constituent une modelisation fidele et verifiable sans boite noire proprietaire.

* Comment garantissez-vous l'honnetete des graphiques ?
Reponse : Echelles commencant a zero pour les histogrammes, axes des quadrants normalises sur les medians de la ligue, et aucune troncation artificielle qui viendrait biaiser la perception visuelle.

* Quelle est la plus-value de l'architecture multi-pages ?
Reponse : Elle respecte la pyramide de Minto et reduit la charge cognitive : l'utilisateur dispose d'une vue de synthese en 3 KPIs, puis plonge volontairement dans les ecrans specialises sans defilement vertical infini.
