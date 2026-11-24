
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

# PHASE 1 : ANNULATION DE COMMANDE

# 1. Annuler la dernière commande remet le stock, le solde et la fidélité dans leur état avant la commande
annulation_caf = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)],
    [Client("Test", "etudiant", 10.00)])
solde_avant = annulation_caf.clients["Test"].solde
stock_avant = annulation_caf.carte["B01"].stock
cumul_avant = annulation_caf.clients["Test"].cumul_achats
assert annulation_caf.traiter_commande("Test", "07:45", [("B01", 1)]) == (True, "", 1.20)
commande_annulee = annulation_caf.journal[-1]
assert annulation_caf.annuler_commande(commande_annulee.numero) == (True, "", 1.20)
assert annulation_caf.clients["Test"].solde == solde_avant
assert annulation_caf.carte["B01"].stock == stock_avant
assert annulation_caf.clients["Test"].cumul_achats == cumul_avant

# 2. Annulation d'une commande inconnue
annulation_caf2 = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)],
    [Client("Test", "etudiant", 10.00)])
assert annulation_caf2.annuler_commande(999) == (False, "commande inconnue", 0.0)

# 3. Annulation d'une commande déjà annulée
annulation_caf3 = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)],
    [Client("Test", "etudiant", 10.00)])
annulation_caf3.traiter_commande("Test", "07:45", [("B01", 1)])
numero_caf3 = annulation_caf3.journal[-1].numero
assert annulation_caf3.annuler_commande(numero_caf3) == (True, "", 1.20)
assert annulation_caf3.annuler_commande(numero_caf3) == (False, "commande déjà annulée", 0.0)

# 4. Annulation refusée : aucune modification
annulation_caf4 = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)],
    [Client("Test", "etudiant", 10.00)])
stock_avant_refus = annulation_caf4.carte["B01"].stock
solde_avant_refus = annulation_caf4.clients["Test"].solde
assert annulation_caf4.annuler_commande(999) == (False, "commande inconnue", 0.0)
assert annulation_caf4.carte["B01"].stock == stock_avant_refus
assert annulation_caf4.clients["Test"].solde == solde_avant_refus

# 5. Remboursement d'un visiteur
visiteur_caf = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)],
    [Client("Visiteur", "visiteur", 0.00)])
assert visiteur_caf.traiter_commande("Visiteur", "07:45", [("B01", 1)]) == (True, "", 1.20)
numero_visiteur = visiteur_caf.journal[-1].numero
assert visiteur_caf.annuler_commande(numero_visiteur) == (True, "", 1.20)
assert visiteur_caf.clients["Visiteur"].solde == 0.00

# 6. Remboursement qui fait dépasser 150,00 €
plafond_caf = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)],
    [Client("Riche", "etudiant", 145.80)])
assert plafond_caf.traiter_commande("Riche", "07:45", [("B01", 1)]) == (True, "", 1.20)
numero_riche = plafond_caf.journal[-1].numero
assert plafond_caf.recharger_badge("Riche", 5.00) == (True, "")
assert plafond_caf.annuler_commande(numero_riche) == (True, "", 1.20)
assert plafond_caf.clients["Riche"].solde == 150.80

# 7. Annulation d'une commande ayant utilisé un avantage de fidélité
fidelite_caf = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 100),
     Produit("P01", "Sandwich", "plat", 4.00, 20)],
    [Client("Fidele", "etudiant", 100.00)])
fidelite_client = fidelite_caf.clients["Fidele"]
assert fidelite_caf.traiter_commande("Fidele", "12:00", [("P01", 12)]) == (True, "", 43.20)
assert fidelite_client.avantage_fidelite() == 0.05
assert fidelite_caf.traiter_commande("Fidele", "07:45", [("B01", 1)]) == (True, "", 1.14)
fidelite_commande = fidelite_caf.journal[-1]
assert fidelite_commande.avantage_fidelite == 0.05
assert fidelite_caf.annuler_commande(fidelite_commande.numero) == (True, "", 1.14)
assert fidelite_client.cumul_achats == 43.20
assert fidelite_client.avantage_fidelite() == 0.05

# 8. Ticket d'une commande annulée
assert "ANNULÉE" in fidelite_commande.__str__()

# Rapport : montant remboursé et nombre de commandes annulées
rapport_fidelite = fidelite_caf.construire_rapport()
assert rapport_fidelite["montant_rembourse"] == 1.14
assert rapport_fidelite["nb_annulees"] == 1

# PHASE 2 : RAPPEL DE PRODUIT

# 1. Rappel d'un produit présent dans plusieurs commandes
rappel_caf = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10),
     Produit("D01", "Cookie", "dessert", 1.40, 10)],
    [Client("Alice", "etudiant", 20.00),
     Client("Bruno", "alternant", 20.00)])

assert rappel_caf.traiter_commande("Alice", "07:45", [("B01", 1)]) == (True, "", 1.20)
numero_alice_rappel = rappel_caf.journal[-1].numero
assert rappel_caf.traiter_commande("Bruno", "08:00", [("B01", 1), ("D01", 1)]) == (True, "", 2.60)
numero_bruno_rappel = rappel_caf.journal[-1].numero
stock_cookie_avant = rappel_caf.carte["D01"].stock
resume = rappel_caf.rappeler_produit("B01")
assert resume["motif"] == ""
assert resume["commandes_annulees"] == [numero_alice_rappel, numero_bruno_rappel]
assert resume["montant_total"] == 3.80
assert resume["clients_rembourses"] == {"Alice": 1.20, "Bruno": 2.60}
assert rappel_caf.carte["B01"].stock == 0
assert rappel_caf.carte["B01"].rappele is True
assert rappel_caf.carte["D01"].stock == stock_cookie_avant + 1
assert rappel_caf.clients["Alice"].solde == 20.00
assert rappel_caf.clients["Bruno"].solde == 20.00

# 2. Rappel d'un produit sans aucune commande
rappel_vide = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)],
    [Client("Alice", "etudiant", 20.00)])
resume_vide = rappel_vide.rappeler_produit("B01")
assert resume_vide["commandes_annulees"] == []
assert resume_vide["clients_rembourses"] == {}
assert resume_vide["montant_total"] == 0.0
assert rappel_vide.carte["B01"].stock == 0

# 3. Commande contenant un produit rappelé : refusée, sans modification
rappel_caf3 = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)],
    [Client("Alice", "etudiant", 20.00)])
rappel_caf3.rappeler_produit("B01")
solde_avant_refus = rappel_caf3.clients["Alice"].solde
stock_avant_refus = rappel_caf3.carte["B01"].stock
assert rappel_caf3.traiter_commande("Alice", "07:45", [("B01", 1)]) == (False, "produit rappelé", 0.0)
assert rappel_caf3.clients["Alice"].solde == solde_avant_refus
assert rappel_caf3.carte["B01"].stock == stock_avant_refus

# 4. Réapprovisionnement d'un produit rappelé : refusé
rappel_caf4 = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)],
    [Client("Alice", "etudiant", 20.00)])
rappel_caf4.rappeler_produit("B01")
assert rappel_caf4.reapprovisionner("B01", 5) is False
assert rappel_caf4.carte["B01"].stock == 0

# 5. Second rappel du même produit
rappel_caf5 = Cafeteria(
    [Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)],
    [Client("Alice", "etudiant", 20.00)])
rappel_caf5.rappeler_produit("B01")
resume_second = rappel_caf5.rappeler_produit("B01")
assert resume_second["motif"] == "déjà rappelé"
assert resume_second["commandes_annulees"] == []
assert rappel_caf5.construire_rapport()["refus"]["déjà rappelé"] == 1

# PHASE 3 : RUBRIQUES DU RAPPORT DE CRISE

rapport_rappel = rappel_caf.construire_rapport()
assert rapport_rappel["nb_acceptees"] == 0
assert rapport_rappel["nb_annulees"] == 2
assert rapport_rappel["chiffre_affaires"] == 0.0
assert rapport_rappel["montant_rembourse"] == 3.80
assert rapport_rappel["top_ventes"] == []

rappel_client = rapport_rappel["rappels"]["B01"]
assert rappel_client["montant_total"] == 3.80
assert rappel_client["clients_rembourses"] == {"Alice": 1.20, "Bruno": 2.60}

produit_carte = rapport_rappel["carte_triee"][0]
for produit in rapport_rappel["carte_triee"]:
    if produit.code == "B01":
        produit_carte = produit
assert produit_carte.rappele is True
assert produit_carte.stock == 0

print("Tous les tests passent.")