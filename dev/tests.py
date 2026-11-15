
"""
Tests Projet

Un test = 3 étapes : 1. CRÉER les objets ; 2. APPELER la méthode ; 3. écrire un assert avec le résultat calculé À LA MAIN.
"""

from produit import Produit
from client import Client
from commande import Commande
from cafeteria import Cafeteria

# PRODUIT : le stock et le créneau des plats

wrap = Produit("P02", "Wrap végétarien", "plat", 4.60, 10)

assert wrap.disponible(10, "12:00") == (True, "")                    # CAS LIMITE : stock exactement suffisant
assert wrap.disponible(11, "12:00") == (False, "rupture de stock")   # une unité de trop
assert wrap.disponible(1, "11:30") == (True, "")                     # CAS LIMITE : 11:30 est inclus
assert wrap.disponible(1, "14:00") == (False, "hors créneau")        # CAS LIMITE : 14:00 est exclu

# CLIENT : payer, se recharger, la fidélité

bruno = Client("Bruno", "alternant", 3.50)
assert bruno.peut_payer(3.50) is True      # CAS LIMITE : solde exactement suffisant
assert bruno.peut_payer(3.51) is False     # un centime de trop

farid = Client("Farid", "personnel", 0.00)
assert farid.peut_payer(10.00) is True     # CAS LIMITE : découvert de -10,00 € autorisé
assert farid.peut_payer(10.01) is False    # -10,01 € : refusé

chloe = Client("Chloé", "etudiant", 25.00)
assert chloe.recharger(100.00) == (True, "")     # CAS LIMITE : recharge de 100,00 € acceptée

riche = Client("Riche", "etudiant", 100.00)
assert riche.recharger(100.00) == (False, "plafond de solde dépassé")   # 100 + 100 dépasse 150

moins_de_40 = Client("A", "etudiant", 50.00)
moins_de_40.ajouter_achat(39.99)
assert moins_de_40.avantage_fidelite() == 0.0     # 39,99 € cumulés : pas de remise

pile_40 = Client("B", "etudiant", 50.00)
pile_40.ajouter_achat(40.00)
assert pile_40.avantage_fidelite() == 0.05        # 40,00 € cumulés : -5 %


# COMMANDE : événement 6 du sujet (Chocolat chaud + Croissant x 3)

commande = Commande(bruno, "08:40")
commande.ajouter_ligne(Produit("B03", "Chocolat chaud", "boisson chaude", 1.60, 40), 1)
commande.ajouter_ligne(Produit("V01", "Croissant", "viennoiserie", 1.20, 30), 3)
assert commande.calculer_total() == 5.20    # 1,60 + 3 x 1,20
assert len(commande) == 4                   # 1 + 3 articles


# CAFETERIA : une petite caisse (2 produits, 1 client).

caf = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 100),
     Produit("P01", "Sandwich jambon-beurre", "plat", 4.00, 15)],
    [Client("Alice", "etudiant", 12.00)])

# Une commande acceptée : 2 cafés = 2,40 €
assert caf.traiter_commande("Alice", "07:45", [("B01", 2)]) == (True, "", 2.40)
assert caf.clients["Alice"].solde == 9.60       # Alice a été débitée
assert caf.carte["B01"].stock == 98             # le stock a baissé de 2

# Un produit inconnu fait refuser TOUTE la commande
assert caf.traiter_commande("Alice", "08:00", [("B01", 1), ("Z99", 1)]) == (False, "produit inconnu", 0.0)
assert caf.carte["B01"].stock == 98             # le café valide n'a pas été vendu

# Solde insuffisant : 3 sandwichs = 12,00 € - 10 % = 10,80 € alors qu'Alice a 9,60 €
assert caf.traiter_commande("Alice", "12:00", [("P01", 3)]) == (False, "solde insuffisant", 0.0)
assert caf.clients["Alice"].solde == 9.60       # son solde n'a pas bougé

# Gros panier (variante A3) : 2 sandwichs = 8,00 € : le seuil est atteint, -10 % pour une étudiante
assert caf.traiter_commande("Alice", "12:00", [("P01", 2)]) == (True, "", 7.20)

# Client fidèle (variante B3) : on lui ajoute 40,00 € d'achats, donc -5 % : 1,20 x 0,95 = 1,14
caf.clients["Alice"].ajouter_achat(40.00)
assert caf.traiter_commande("Alice", "12:00", [("B01", 1)]) == (True, "", 1.14)

# Rapport : le chiffre d'affaires est la somme des 3 commandes acceptées
assert caf.construire_rapport()["chiffre_affaires"] == 10.74    # 2,40 + 7,20 + 1,14

print("Tous les tests passent.")