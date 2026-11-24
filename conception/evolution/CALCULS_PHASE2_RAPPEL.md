# Phase 2 - Calculs a la main : rappel produit

## Source officielle

Les valeurs suivantes sont celles obtenues avec le PDF officiel placé dans `conception/` et rejouées dans `dev/scenario_v2.py`.

## Variante utilisée

- A3 : 10 % pour les étudiants et alternants si le total atteint 8 €, sinon 5 % pour les autres profils.
- B3 : 5 % dès que le cumul payé atteint 40 €.
- Annulation : remboursement du montant réellement payé, restitution intégrale des lignes.
- Rappel : annulation des commandes actives contenant le produit, dans l’ordre chronologique.

## Événement 12:30 - rappel officiel des Wraps P02

### Situation avant rappel

La commande de Chloé 12:18 a déjà été annulée. Deux autres commandes actives contiennent encore P02 :

| Commande | Heure | Client | Contenu | Montant payé |
|---|---|---|---|---:|
| 6 | 12:15 | Bruno | 2 Wraps P02 | 8.28 € |
| 8 | 12:20 | Alice | 1 Wrap P02 + autres produits | 7.60 € |

Avant le rappel :

```text
Stock P02 = 6 unités
Solde Bruno = 10.02 €
Cumul Bruno = 13.48 €
Solde Alice = 2.00 €
Cumul Alice = 10.00 €
```

### Ordre du rappel

1. P02 est marqué rappelé.
2. Son stock passe immédiatement à 0.
3. La commande 6 de Bruno est annulée.
4. La commande 8 d'Alice est annulée.

### Annulation de la commande 6

```text
Montant remboursé à Bruno = 8.28 €
```

Après remboursement :

```text
Solde Bruno = 10.02 + 8.28 = 18.30 €
Cumul Bruno = 13.48 - 8.28 = 5.20 €
Fidélité Bruno = inactive
```

### Annulation de la commande 8

La commande Alice contient P02, Eau, Fruit de saison et Café.

```text
Montant remboursé à Alice = 7.60 €
```

Après remboursement :

```text
Solde Alice = 2.00 + 7.60 = 9.60 €
Cumul Alice = 10.00 - 7.60 = 2.40 €
Fidélité Alice = inactive
```

Toutes les lignes de la commande sont remises en stock. P02 est ensuite maintenu à 0 et devient rappelé.

### Montant total remboursé

```text
Bruno : 8.28 €
Alice : 7.60 €
Total : 8.28 + 7.60 = 15.88 €
```

Le montant total remboursé à 12:30 est donc 15.88 €.

### Résumé officiel

```python
{
    "produit": produit_P02,
    "commandes_annulees": [6, 8],
    "clients_rembourses": {
        "Bruno": 8.28,
        "Alice": 7.60
    },
    "montant_total": 15.88,
    "motif": ""
}
```

## État des clients concernés

### Bruno

```text
Solde avant rappel = 10.02 €
Remboursement = 8.28 €
Solde après rappel = 18.30 €
Cumul avant = 13.48 €
Cumul après rejeu = 5.20 €
Fidélité B3 = inactive
```

### Alice

```text
Solde avant rappel = 2.00 €
Remboursement = 7.60 €
Solde après rappel = 9.60 €
Cumul avant = 10.00 €
Cumul après rejeu = 2.40 €
Fidélité B3 = inactive
```

Les commandes 6 et 8 restent dans le journal avec le statut `annulee`.

## Produit sans aucune commande

Exemple : rappeler P02 sans aucune vente active.

```text
Commandes annulées : 0
Montant remboursé : 0.00 €
Clients remboursés : aucun
Stock final P02 : 0
```

## Produit rappelé utilisé dans une nouvelle commande

Avant rappel :

```text
Commande (B01, 1) = acceptée
```

Après rappel :

```text
Résultat = (False, "produit rappelé", 0.0)
Stock = inchangé à 0
Solde = inchangé
Journal = inchangé
```

## Réapprovisionnement d'un produit rappelé

```text
Résultat = False
Stock = 0
Aucun stock ajouté
Motif compté = "produit rappelé"
```

## Second rappel

Premier rappel :

```text
Produit.rappeler() = True
Stock = 0
```

Second rappel :

```text
Motif = "déjà rappelé"
Aucune commande annulée
Aucun remboursement
Aucune modification supplémentaire
Compteur rapport = déjà rappelé + 1
```

## Code produit inconnu

```text
Résultat = motif "produit inconnu"
Aucune commande annulée
Aucun stock modifié
Aucun solde modifié
Aucun cumul modifié
```

## Tests manuels minimaux

### Plusieurs commandes

```text
Commande Alice : 1 × B01 = 1.20 €
Commande Bruno : 1 × B01 + 1 × D01 = 2.60 €
Total remboursé = 3.80 €
Commandes annulées = 2
```

### Aucun retour en stock du produit rappelé

```text
B01 avait 10 unités
Une commande vend 1 unité
Le rappel annule la commande
B01 doit finir à 0, pas à 10
```

Les autres produits sont remis normalement en stock.
