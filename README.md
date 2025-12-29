# Analyse des déterminants de la réussite olympique

## Table des matières : 

1. Objectifs
2. Définitions
3. Sources de données
4. Présentation du dépôt

## 1. Objectifs 

L’objectif de ce projet est d’analyser empiriquement les déterminants de la réussite des pays aux Jeux Olympiques d’été.

La performance olympique est mesurée à l’aide d’un score agrégé fondé sur les médailles remportées, permettant des comparaisons entre pays et dans le temps.
L’analyse vise à évaluer le rôle de facteurs économiques et structurels — niveau de richesse, développement humain, dépenses sportives et dynamique passée de performance — dans l’explication des résultats olympiques.

L’approche repose sur une analyse descriptive, suivie d’estimations économétriques simples (OLS, tests de robustesse, validation hors échantillon et estimation par variables instrumentales).

## 2. Définitions

Score olympique
Indicateur synthétique de performance construit à partir des médailles obtenues par chaque pays lors des Jeux Olympiques d’été, avec une pondération différenciée selon le type de médaille.

Indice de développement humain (IDH)
Indice composite compris entre 0 et 1, mesurant le niveau de développement humain d’un pays à partir de trois dimensions : santé, éducation et niveau de vie.

Dépenses sportives (% du PIB)
Part des dépenses publiques consacrées au sport rapportée au PIB, utilisée comme indicateur d’effort public relatif.

Dépenses sportives en volume
Mesure des dépenses sportives exprimée en valeur absolue, obtenue en combinant les dépenses relatives et le PIB.

## 3. Source des données 

Les données utilisées dans ce projet proviennent de sources institutionnelles et de bases publiques reconnues. Les résultats olympiques et les informations sur les médailles sont issus de jeux de données disponibles sur Kaggle, complétés pour les éditions récentes de Tokyo 2021 et Paris 2024 par des données provenant de Wikipedia.

Les indicateurs macroéconomiques, notamment le PIB et le PIB par habitant, proviennent des bases de données de la Banque mondiale et de la Federal Reserve Bank of St. Louis (FRED) pour les États-Unis.

Les données relatives aux dépenses publiques consacrées au sport sont issues des statistiques de l’OCDE et de data.gouv.fr, permettant une mesure harmonisée des dépenses sportives.

Enfin, les indicateurs de développement humain sont fournis par le Programme des Nations unies pour le développement (PNUD) à travers l’indice de développement humain (IDH).

## 4. Présentation du dépôt

data/ :
Données brutes et intermédiaires utilisées dans le projet.

Notebook_Résultats.ipynb :
Notebook principal contenant l’ensemble du code exécuté, les visualisations et les résultats économétriques. Il constitue le rapport final du projet.

Notebook_Sans_Résultats.ipynb :
Version du notebook sans sorties, destinée à la lecture du code et des commentaires.

Scriptsfinal/ :
Ensemble de scripts Python regroupant les fonctions de nettoyage des données, de construction des variables, de visualisation et d’estimation économétrique.