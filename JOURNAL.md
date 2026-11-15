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


## 10/11
- Ce qui a bloqué : 
Je me suis demandé si on pouvait se passer de `round` dans les calculs de montant.

- Comment je m'en suis sorti : 
j'ai fait un test dans Python. Il montre que 1.60 + 3 * 1.20 donne 5.199999999999999 au lieu de 5.20, et qu'un solde de 0.30 est refusé pour un paiement de 0.1 + 0.2 (0.1 + 0.2 = 0.30000000000000004). Python fait de très petites erreurs sur les nombres décimaux. J'ai donc gardé `round(x, 2)`, qui arrondit au centime, après chaque calcul d'argent.

## 12/11
- Ce qui a bloqué : je ne savais pas comment donner automatiquement un numéro différent à chaque commande. En écrivant `self.compteur += 1`, je me suis demandé si chaque commande n'allait pas avoir son propre compteur.

- Comment je m'en suis sorti : j'ai relu la section 5.2 du sujet, qui dit que « le numéro de commande vient d'un compteur de classe ». Un attribut de classe est partagé par toutes les commandes. Je l'écris donc avec `Commande.compteur += 1` et non `self.compteur += 1`. Chaque nouvelle commande reçoit ainsi le numéro suivant.


## 15/11
- Ce qui a bloqué : je ne savais pas comment organiser le traitement d'une commande dans
  `Cafeteria`, notamment pour éviter de modifier le stock ou le solde avant d'être sûr que
  la commande pouvait être acceptée.

- Comment je m'en suis sorti : j'ai suivi l'ordre indiqué dans le sujet : vérifier,
  calculer, encaisser puis enregistrer. J'ai séparé ces étapes dans plusieurs méthodes.
  Les vérifications sont donc faites avant les modifications du stock, du solde et du
  journal.


- Ce qui a bloqué : je ne savais pas où appliquer les remises A3 et B3, ni dans quel ordre
  les calculer.

- Comment je m'en suis sorti : j'ai laissé `Commande` calculer le total de ses lignes,
  puis j'ai fait appliquer les remises dans `Cafeteria`. La remise A3 est calculée en
  premier, puis l'avantage B3. J'ai aussi testé les limites de 8,00 € pour A3 et de
  40,00 € d'achats pour B3.


- Ce qui a bloqué : je voulais être sûr qu'une commande refusée ne débite pas le client,
  ne retire pas les produits du stock et ne soit pas ajoutée au journal.

- Comment je m'en suis sorti : j'ai ajouté des tests avec un produit inconnu et avec un
  solde insuffisant. Après chaque refus, je vérifie que le solde et le stock n'ont pas
  changé.


## Vérification des calculs à la main
- J'ai comparé les calculs réalisés sur papier pour les événements 2, 6 et 11 avec les résultats présents dans `sortie_scenario.txt`.

- Les résultats sont identiques :
  - événement 2 : Alice paie 2,40 €, son solde passe à 9,60 € et son cumul de fidélité
    est de 2,40 € ;
  - événement 6 : Bruno paie 5,20 €, son solde passe à 18,30 € et son cumul de fidélité
    est de 5,20 € ;
  - événement 11 : Alice paie 7,60 €, son solde passe à 2,00 € et son cumul de fidélité
    est de 10,00 €.

- Il n'y a donc pas d'écart entre les calculs manuels et le programme. Dans ces trois
  événements, aucun client n'a encore atteint le seuil de fidélité de 40,00 €.