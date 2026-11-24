# Phase 1 - Calculs a la main : annulation

## Variante utilisee

- A3 : gros panier a partir de 8 €, avec 10 % pour les etudiants et alternants, 5 % pour les autres profils.
- B3 : 5 % de remise apres 40 € d'achats effectivement payes.
- Remboursement : badge credite sans plafond de 150 €.
- Le cumul est rejoue a partir des commandes acceptees et non annulees.

## Source officielle

Les données suivantes viennent du PDF officiel placé dans `conception/`.

## Événement 12:15 - base officielle

Bruno commande deux Wraps végétariens :

```text
2 × 4,60 € = 9,20 €
Remise A3 = 9,20 × 10 % = 0,92 €
Montant payé = 9,20 - 0,92 = 8,28 €
Solde avant = 18,30 €
Solde après = 18,30 - 8,28 = 10,02 €
Cumul après = 5,20 + 8,28 = 13,48 €
```

## Événement 12:18 - commande officielle de Chloé

```text
Total = 4,60 €
Remise A3 = 0,00 € car 4,60 < 8,00 €
Remise B3 = 0,00 € car le cumul est 9,54 €
Montant payé = 4,60 €

Solde avant = 15,46 €
Solde après = 15,46 - 4,60 = 10,86 €
Cumul avant = 9,54 €
Cumul après = 9,54 + 4,60 = 14,14 €
Fidélité B3 = inactive
```

## Événement 12:25 - annulation de la commande de Chloé

La commande créée à 12:18 porte le numéro 7.

```text
Montant réellement payé = 4,60 €
Remboursement = 4,60 €
Solde avant annulation = 10,86 €
Solde après remboursement = 10,86 + 4,60 = 15,46 €
```

Rejeu de la fidélité :

```text
Cumul avant annulation = 14,14 €
Montant retiré = 4,60 €
Cumul après rejeu = 14,14 - 4,60 = 9,54 €
Fidélité B3 = inactive
```

Le Wrap est remis en stock, puis la commande reste au journal avec le statut `annulee`.

## Événements 12:26 et 12:27

- 12:26 : `(False, "commande déjà annulée", 0.0)`.
- 12:27 : `(False, "commande inconnue", 0.0)`.

## Cas de fidélité avec seuil franchi

### Achat initial

```text
Commande 1 : 12 cafés à 4 € = 48 €
A3 étudiant : -10 %
Montant payé = 48 × 0,90 = 43,20 €
Cumul après = 43,20 €
```

Une commande suivante gagne donc B3.

### Commande suivante de 1 café

```text
Total = 1,20 €
A3 sans gros panier = 0 %
B3 = -5 %
Montant payé = 1,20 × 0,95 = 1,14 €
```

Si cette commande est annulée :

```text
Cumul rejoué = 43,20 €
Avantage B3 = actif
Montant remboursé = 1,14 €
```

Annuler une commande ayant utilisé B3 ne supprime pas automatiquement B3 si le cumul rejoué reste au moins égal à 40 €.

## Tests de remboursement calculés

### Annulation normale

```text
Solde avant achat = 10,00 €
Café payé = 1,20 €
Solde après achat = 8,80 €
Remboursement = 1,20 €
Solde restauré = 10,00 €
Stock restauré = stock avant achat
Cumul restauré = 0,00 €
```

### Visiteur

```text
Montant payé = 1,20 €
Remboursement = 1,20 €
Solde du visiteur = 0,00 € avant et après
Montant compté dans le chiffre d'affaires actif avant annulation
```

### Remboursement dépassant 150 €

Montage vérifié par les tests :

```text
Solde initial = 145,80 €
Café payé = 1,20 €
Solde apres achat = 144,60 €
Recharge valide = 5,00 €
Recharge plafonnée = 149,60 €
Remboursement = 1,20 €
Solde final = 150,80 €
```

Résultat : 150,80 € est autorisé par le remboursement. La limite de 150 € ne s'applique pas.

### Quantité excessive

```text
Limite acceptée = 10
Première quantité refusée = 11
Motif = quantité excessive
```

### Double annulation

Première annulation :

```text
Résultat = (True, "", montant_remboursé)
Statut = "annulee"
```

Deuxième annulation :

```text
Résultat = (False, "commande déjà annulée", 0.0)
```

### Commande inconnue

```text
Résultat = (False, "commande inconnue", 0.0)
```

Aucun stock, solde ou cumul ne doit être modifié.

## Ticket annulée

Le ticket doit contenir obligatoirement :

```text
Statut : ANNULEE
Montant réellement payé
Remise enregistrée
Avantage fidélité enregistré
```
