# Journal de bord

## 07/11
- Ce qui a bloqué : j'ai hésité sur la classe qui doit calculer le total d'une commande
  (la Commande ou la Cafeteria ?).
- Comment je m'en suis sorti : j'ai relu le tableau de la section 5.1 du sujet, qui donne
  « calculer son total » à la classe Commande. la Commande connaît ses lignes (produit × quantité). J'ai donc mis calculer_total dans Commande.
  La Cafeteria l'appelle ensuite, puis applique (si les conditions sont remplies) la remise A3 et l'avantage B3 sur ce total.