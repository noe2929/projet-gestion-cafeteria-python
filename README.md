# CampusCafé : la caisse de la cafétéria du campus

Projet de fin de module Python — Master 1 Data/IA 2026-2027  
Étudiant : Noé LABBÉ

## 1. Présentation

CampusCafé est une application Python qui simule la gestion d'une caisse de cafétéria :

- gestion des produits et des stocks ;
- gestion des clients et des soldes ;
- traitement des commandes ;
- application des remises ;
- génération d'un rapport de clôture.

## 2. Variante choisie

| Axe | Règle |
|---|---|
| **A3 : Gros panier** | Si le total atteint 8,00 €, remise de 10 % pour les étudiants et alternants, 5 % pour les autres profils. |
| **B3 : Client fidèle** | Dès que le client a cumulé 40,00 € d'achats, il obtient une remise de 5 % sur ses commandes suivantes. |

## 3. Lancement

Les commandes suivantes doivent être exécutées depuis la racine du projet.

### Exécuter le scénario de la journée

```bash
python dev/scenario.py
```

Cette commande rejoue les événements de la journée et affiche le rapport de clôture.

### Exécuter les tests

```bash
python dev/tests.py
```

### Enregistrer la sortie du scénario

```bash
python dev/scenario.py > sortie_scenario.txt
```

## 4. Choix de conception

- La remise A3 est calculée avant la remise B3.
- Le seuil de 8,00 € pour A3 est inclus.
- Le cumul de fidélité correspond aux montants effectivement payés.
- Une commande refusée ne consomme pas de numéro de commande.
- Les doublons d'un même produit dans une demande sont regroupés avant les vérifications.
- En cas d'égalité pour le top 3 des ventes, le premier produit dans l'ordre de la carte est retenu.
- Un client inconnu entraîne un refus avec le motif `client inconnu`, sans modification de la caisse.

## 5. Structure du projet

```text
.
├── conception/
│   ├── CampusCafe_Enonce_Projet.pdf
│   ├── Diagramme de classe projet caféteria.jpg
│   ├── Exercice calcul à la main évènements projet caféteria.jpg
│   ├── cas_de_tests.ipynb
│   └── pseudo_code_traitement_commande.ipynb
├── dev/
│   ├── cafeteria.py      # Gestion de la caisse et traitement des commandes
│   ├── client.py         # Gestion des clients, soldes et fidélité
│   ├── commande.py       # Gestion des commandes
│   ├── produit.py        # Gestion des produits et des stocks
│   ├── scenario.py       # Scénario de la journée
│   └── tests.py          # Tests du projet
├── JOURNAL.md
├── README.md
└── sortie_scenario.txt  # Résultat enregistré du scénario
```
