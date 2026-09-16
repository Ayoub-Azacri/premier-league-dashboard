# Document de cadrage : Dashboard Premier League

Projet note : Dashboard interactif et visualisation decisionnelle
Filiere : Bachelor Data et IA (MD4)
Equipe : Ayoub AZACRI, Youssef EL HAJJI, Omar HAKIK, Youssef DEKHAIL

## 1. Message cle (Pyramide de Minto)

L'efficacite offensive au cadrage et la conversion clinique des tirs determinent le succes sportif d'un club bien plus que l'accumulation de tirs steriles ou la seule possession territoriale.

Ce message central structure l'ensemble des ecrans du tableau de bord : nous demontrons avec 5 saisons de donnees (1 900 matchs) que multiplier les tirs hors cadre reduit l'esperance de gain, tandis que maximiser le ratio tirs cadres / tirs totaux separe les clubs europeens des equipes en difficulte.

## 2. Audience cible

Direction sportive, cellule de recrutement et staff technique d'un club professionnel de Premier League.

Besoin metier : evaluer objectivement la rentabilite offensive reelle de leur effectif et de leurs adversaires, identifier les profils sous-performants dans le dernier geste, et adapter le plan de jeu selon le contexte du match (domicile, deplacement, huis clos).

## 3. Selection et justification des KPIs

Pour eviter la surcharge cognitive et respecter la regle de 2 a 3 indicateurs majeurs, nous avons ecarte les metriques d'apparence (vanity metrics) pour privilegier des indicateurs directement exploitables par le staff :

* Taux de cadrage net (Tirs cadres / Tirs totaux) : indicateur actionnable. Il mesure la qualite du choix de tir et la discipline tactique des attaquants. A l'inverse, le total brut de tirs tentes est une vanity metric trompeuse car un fort volume de tirs lointains hors cadre n'augmente pas la probabilite de marquer.
* Taux de conversion clinique (Buts / Tirs cadres) : indicateur actionnable. Il quantifie le sang-froid et le realisme devant le gardien adverse. Il permet a la cellule de recrutement de reperer les equipes ultra-efficaces malgre un faible nombre d'occasions creees.
* Indice d'efficacite territoriale (Ratio points par tir cadre) : indicateur de contexte actionnable. Il evalue la rentabilite comptable de chaque action dangereuse generee, en isolant les performances a domicile et a l'exterieur.

## 4. Structure de l'application et parcours utilisateur

L'application adopte une architecture multi-pages pour hierarchiser l'information en 3 niveaux :

* Vue de synthese executive (`app.py`) : bandeau de cadrage, zone des 3 KPIs cles contextualises avec comparaison a la moyenne de la ligue, et classement interactif de l'efficacite globale des 20 clubs.
* Volet Efficacite Offensive (`pages/1_Efficacite_Offensive.py`) : quadrant strategique croisant precision (cadrage) et conversion (buts/tirs cadres). Ce quadrant classe les clubs en 4 profils : Chirurgicaux, Dominateurs, Steriles et En difficulte.
* Volet Le 12eme Homme (`pages/2_Le_12eme_Homme.py`) : analyse de l'avantage a domicile et demonstration de son effondrement historique lors de la saison COVID a huis clos (chute de 46 % a 37,9 % de victoires a domicile).
* Volet Simulateur Tactique (`pages/3_Simulateur_Tactique.py`) : outil prospectif permettant au coach de simuler l'issue d'une confrontation entre deux equipes selon leurs profils d'efficacite et le lieu du match.

## 5. Filtres interactifs globaux (Sidebar)

* Filtre de saison : selection de 2019-20 a 2023-24, permettant d'isoler la saison COVID ou d'analyser les cycles pluriannuels.
* Filtre des clubs : selection multi-equipes pour des benchmarks cibles (ex : Big 6, course au maintien).
* Filtre du lieu du match : Domicile, Exterieur ou Ensemble des matchs.

Toutes les requetes de donnees exploitent `@st.cache_data` pour garantir un temps de reponse inferieur a 100 ms.
