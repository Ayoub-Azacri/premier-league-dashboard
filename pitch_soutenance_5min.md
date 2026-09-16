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

## 3. Omar HAKIK : Matrice d'efficacite et radar tactique 360° (02:30 - 03:45)

"Dès la page d'accueil, notre entonnoir de conversion offensive montre que 65 % des tirs sont perdus hors cadre avant même d'inquiéter le gardien.

Sur notre premier volet détaillé, nous croisons ces dimensions dans une matrice tactique en quatre quadrants où chaque bulle est indexée sur les points réels engrangés au classement.

Ce graphique répond au principe des canaux pré-attentifs : les seuils médians séparent instantanément l'élite des équipes en difficulté. En haut à droite, la zone chirurgicale regroupe Manchester City, Arsenal et Liverpool, qui allient plus de 35 % de cadrage et 33 % de conversion.

Pour la cellule de recrutement, nous avons ajouté un radar tactique à 360° inspiré des standards Opta. Il compare en un clin d'œil n'importe quel club aux moyennes de la Premier League sur la précision, la conversion, le volume et la rentabilité par tir cadré."

## 4. Youssef DEKHAIL : Le 12e Homme et simulateur tactique (03:45 - 05:00)

"Notre second volet explore l'expérience naturelle du huis clos lors de la saison COVID 2020-21.

Notre courbe temporelle sur 5 saisons démontre l'effondrement historique de l'avantage à domicile : le taux de victoires à domicile est tombé à 37,9 %, passant sous la barre des victoires à l'extérieur (40,3 %) pour la seule fois de l'histoire moderne.

Notre graphique Cleveland Dumbbell isole la sensibilité de chaque club : sans le Kop d'Anfield, le taux de victoire de Liverpool à domicile s'est effondré de 24 points. Newcastle et Arsenal ont perdu plus de 20 points, alors que Manchester City est resté quasiment insensible avec seulement 2,6 points d'écart.

Enfin, notre simulateur tactique combine un modèle d'espérance de buts et une loi de Poisson bivariée pour estimer les probabilités d'issue et les scores exacts les plus probables avec ou sans public."

## Reponses aux questions probables du jury

* Comment avez-vous modélisé l'espérance de buts (xG) et les scores dans le simulateur ?
Réponse : Nous combinons la force offensive relative de chaque club, la résistance défensive adverse et la prime de terrain observée sur 1 900 matchs, puis appliquons une distribution de Poisson bivariée pour extraire les probabilités de victoires et les trois scores exacts les plus fréquents.

* Comment garantissez-vous l'honnêteté des graphiques ?
Réponse : Échelles commençant à zéro pour les histogrammes, axes des quadrants normalisés sur les médianes réelles de la ligue, et aucune troncature artificielle qui viendrait biaiser la perception visuelle.

* Quelle est la plus-value de l'architecture multi-pages ?
Reponse : Elle respecte la pyramide de Minto et reduit la charge cognitive : l'utilisateur dispose d'une vue de synthese en 3 KPIs, puis plonge volontairement dans les ecrans specialises sans defilement vertical infini.
