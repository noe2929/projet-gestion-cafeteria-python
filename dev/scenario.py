"""
CampusCafé : le scénario de la journée décrit par le sujet

Il crée la caisse, rejoue les 17 événements un par un, puis affiche le rapport de clôture.
"""

from produit import Produit
from client import Client
from cafeteria import Cafeteria


# 1. La préparation : la carte, les clients et la caisse (sections 2.1 et 2.2)

def creer_cafeteria():
    """Crée la caisse avec la carte et les clients du début de journée."""
    produits = [
        Produit("B01", "Café expresso", "boisson chaude", 1.20, 100),
        Produit("B02", "Thé", "boisson chaude", 1.30, 60),
        Produit("B03", "Chocolat chaud", "boisson chaude", 1.60, 40),
        Produit("B04", "Jus d'orange", "boisson froide", 2.00, 24),
        Produit("B05", "Eau 50 cl", "boisson froide", 1.00, 40),
        Produit("V01", "Croissant", "viennoiserie", 1.20, 30),
        Produit("P01", "Sandwich jambon-beurre", "plat", 4.00, 15),
        Produit("P02", "Wrap végétarien", "plat", 4.60, 10),
        Produit("P03", "Plat du jour", "plat", 7.20, 20),
        Produit("D01", "Cookie", "dessert", 1.40, 25),
        Produit("D02", "Fruit de saison", "dessert", 0.80, 30),
    ]
    clients = [
        Client("Alice", "etudiant", 12.00),
        Client("Bruno", "alternant", 3.50),
        Client("Chloé", "etudiant", 25.00),
        Client("Farid", "personnel", 0.00),
        Client("Visiteur", "visiteur", 0.00),    # le visiteur paie comptant : pas de badge
    ]
    return Cafeteria(produits, clients)


# 2. Les trois types d'événements : chacun joue l'action puis affiche le résultat

def afficher_etat_client(cafeteria, nom_client):
    """Affiche le solde et le cumul d'achats d'un client (pour comparer avec les calculs à la main)."""
    if nom_client in cafeteria.clients:
        client = cafeteria.clients[nom_client]
        print(f"      Après : {client} ; cumul d'achats : {client.cumul_achats:.2f} €")


def evenement_commande(cafeteria, numero, heure, nom_client, demandes):
    """Événement « Commande » : on la traite, puis on affiche le résultat (et le ticket si acceptée)."""
    acceptee, motif, montant = cafeteria.traiter_commande(nom_client, heure, demandes)
    if acceptee:
        print(f"[{numero}] {heure} - Commande de {nom_client} : ACCEPTÉE, {montant:.2f} € payés")
        print(cafeteria.journal[-1])              # le ticket (la dernière commande du journal)
    else:
        print(f"[{numero}] {heure} - Commande de {nom_client} : REFUSÉE ({motif})")
    afficher_etat_client(cafeteria, nom_client)


def evenement_recharge(cafeteria, numero, heure, nom_client, montant):
    """Événement « Recharge » : on recharge le badge, puis on affiche le résultat."""
    ok, motif = cafeteria.recharger_badge(nom_client, montant)
    if ok:
        print(f"[{numero}] {heure} - Recharge de {nom_client} (+{montant:.2f} €) : ACCEPTÉE")
    else:
        print(f"[{numero}] {heure} - Recharge de {nom_client} (+{montant:.2f} €) : REFUSÉE ({motif})")
    afficher_etat_client(cafeteria, nom_client)


def evenement_reapprovisionnement(cafeteria, numero, heure, code, quantite):
    """Événement « Réapprovisionnement » : on ajoute au stock, puis on affiche le résultat."""
    ok = cafeteria.reapprovisionner(code, quantite)
    if ok:
        print(f"[{numero}] {heure} - Réapprovisionnement de {code} (+{quantite}) : FAIT")
    else:
        print(f"[{numero}] {heure} - Réapprovisionnement de {code} (+{quantite}) : REFUSÉ")


# 3. La journée : les 17 événements du sujet, dans l'ordre. Une commande est une liste de couples (code du produit, quantité).

def jouer_la_journee(cafeteria):
    """Rejoue les 17 événements de la section 6 du sujet."""
    print("[1] 07:30 - Ouverture de la cafétéria")
    evenement_commande(cafeteria, 2, "07:45", "Alice", [("B01", 1), ("V01", 1)])       # Café expresso, Croissant
    evenement_commande(cafeteria, 3, "08:10", "Farid", [("B01", 2)])                   # Café expresso x 2
    evenement_commande(cafeteria, 4, "08:30", "Bruno", [("B03", 1), ("V01", 3)])       # Chocolat chaud, Croissant x 3
    evenement_recharge(cafeteria, 5, "08:35", "Bruno", 20.00)
    evenement_commande(cafeteria, 6, "08:40", "Bruno", [("B03", 1), ("V01", 3)])       # la même commande
    evenement_commande(cafeteria, 7, "09:15", "Visiteur", [("B02", 1), ("D01", 1)])    # Thé, Cookie
    evenement_commande(cafeteria, 8, "11:00", "Chloé", [("P03", 1)])                   # Plat du jour
    evenement_commande(cafeteria, 9, "12:05", "Chloé", [("P03", 1), ("B04", 1), ("D01", 1)])   # Plat du jour, Jus d'orange, Cookie
    evenement_recharge(cafeteria, 10, "12:10", "Alice", 150.00)
    evenement_commande(cafeteria, 11, "12:20", "Alice",
                       [("P02", 1), ("B05", 1), ("D02", 1), ("B01", 1)])   # Wrap, Eau 50 cl, Fruit de saison, Café
    evenement_commande(cafeteria, 12, "12:45", "Visiteur", [("P01", 16)])              # Sandwich x 16
    # Le « Smoothie mangue » n'est pas à la carte : on lui donne un code qui n'existe pas (B06)
    evenement_commande(cafeteria, 13, "13:00", "Bruno", [("P01", 1), ("B06", 1)])
    evenement_commande(cafeteria, 14, "15:30", "Alice", [("B01", 1), ("D01", 1)])      # Café expresso, Cookie
    evenement_reapprovisionnement(cafeteria, 15, "16:00", "P01", 10)                   # Sandwich + 10
    evenement_commande(cafeteria, 16, "17:30", "Farid", [("B02", 2)])                  # Thé x 2
    print("[17] 18:30 - Clôture")
    cafeteria.afficher_rapport()


# 4. Le lancement : on crée la caisse puis on joue la journée
cafeteria = creer_cafeteria()
jouer_la_journee(cafeteria)