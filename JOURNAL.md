# Journal de bord

## 07/11
- Ce qui a bloqué : j'ai hésité sur la classe qui doit calculer le total d'une commande
  (la Commande ou la Cafeteria ?).
  
- Comment je m'en suis sorti : j'ai relu le tableau de la section 5.1 du sujet, qui donne
  « calculer son total » à la classe Commande. la Commande connaît ses lignes (produit × quantité). J'ai donc mis calculer_total dans Commande.
  La Cafeteria l'appelle ensuite, puis applique (si les conditions sont remplies) la remise A3 et l'avantage B3 sur ce total.


## 09/11
- Ce qui a bloqué : 
j'avais un doute sur l'architecture de mon projet.

- Comment je m'en suis sorti : 
en relisant mon code, je me suis rendu compte qu'il serait plus lisible d'avoir une classe dans un fichier que d'avoir un fichier unique qui regroupe le contenu de chaque classe. Chaque classe est désormais dans son propre fichier.


# 10/11
- Ce qui a bloqué : 
Je me suis demandé si on pouvait se passer de `round` dans les calculs de montant.

- Comment je m'en suis sorti : 
j'ai fait un test dans Python. Il montre que 1.60 + 3 * 1.20 donne 5.199999999999999 au lieu de 5.20, et qu'un solde de 0.30 est refusé pour un paiement de 0.1 + 0.2 (0.1 + 0.2 = 0.30000000000000004). Python fait de très petites erreurs sur les nombres décimaux. J'ai donc gardé `round(x, 2)`, qui arrondit au centime, après chaque calcul d'argent.