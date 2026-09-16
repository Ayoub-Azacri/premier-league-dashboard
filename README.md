# Premier League Analytics Dashboard

Tableau de bord decisionnel et recit statistique sur l'efficacite offensive et la performance des clubs de Premier League (2019-2024).

Developpe avec Streamlit, Plotly, Pandas et NumPy.

## Equipe du projet

* Ayoub AZACRI
* Youssef EL HAJJI
* Omar HAKIK
* Youssef DEKHAIL

Promotion HETIC MD4 : Bachelor Data et IA.

## Message cle (Minto)

L'efficacite au cadrage et la conversion clinique des tirs determinent le succes sportif d'un club bien plus que l'accumulation de frappes steriles ou la simple possession territoriale.

## Structure de l'application (Architecture multi-pages)

L'application est organisee en 4 ecrans complementaires :

* Synthese executive (`app.py`) : bandeau de cadrage Minto, 3 KPIs majeurs contextualises et classement interactif de l'efficacite des clubs.
* Efficacite Offensive (`pages/1_🎯_Efficacite_Offensive.py`) : matrice strategique en 4 quadrants croisant precision au cadrage et conversion en buts.
* Le 12e Homme (`pages/2_🏟️_Le_12eme_Homme.py`) : evaluation de l'avantage a domicile et demonstration de son effondrement lors de la saison COVID a huis clos.
* Simulateur Tactique (`pages/3_🔮_Simulateur_Tactique.py`) : simulateur interactif d'issue de match et d'esperance de buts selon les profils d'equipes.

## Architecture des fichiers

* `cadrage.md` : document officiel de cadrage (1 page) destine a l'evaluation academique.
* `pitch_soutenance_5min.md` : conducteur du pitch oral de 5 minutes avec repartition du temps et reponses aux questions du jury.
* `app.py` : point d'entree Streamlit et vue de synthese.
* `pages/` : sous-pages specialisees de l'application.
* `engine/` : moteur statistique modulaire (chargement avec cache, calculs des KPIs, matrice tactique, generateur Plotly).
* `data/premier_league_5seasons.csv` : jeu de donnees propre couvrant 1 900 matchs sur 5 saisons completes.
* `tests/` : suite de 8 tests unitaires automatisant la validation des indicateurs et du chargement des donnees.
* `requirements.txt` : dependances logicielles.

## Installation et lancement

### 1. Cloner le depot

```bash
git clone https://github.com/Ayoub-Azacri/premier-league-dashboard.git
cd premier-league-dashboard
```

### 2. Creer et activer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dependances

```bash
pip install -r requirements.txt
```

### 4. Executer les tests de validation

```bash
pytest -v
```

Tous les tests doivent etre valides au vert.

### 5. Lancer l'application Streamlit

```bash
streamlit run app.py
```

L'application est accessible localement sur `http://localhost:8501`.
