"""
CampusCafé : scénario v2 avec annulations et rappel du Wrap végétarien.
"""

from produit import Produit
from client import Client
from cafeteria import Cafeteria


def creer_cafeteria_v2():
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
        Client("Visiteur", "visiteur", 0.00),
    ]
    return Cafeteria(produits, clients)


def afficher_etat_client(cafeteria, nom_client):
    if nom_client in cafeteria.clients:
        client = cafeteria.clients[nom_client]
        print(f"      Après : {client} ; cumul d'achats : {client.cumul_achats:.2f} €")


def evenement_commande(cafeteria, numero, heure, nom_client, demandes):
    acceptee, motif, montant = cafeteria.traiter_commande(nom_client, heure, demandes)
    if acceptee:
        print(f"[{numero}] {heure} - Commande de {nom_client} : ACCEPTÉE, {montant:.2f} € payés")
        print(cafeteria.journal[-1])
    else:
        print(f"[{numero}] {heure} - Commande de {nom_client} : REFUSÉE ({motif})")
    afficher_etat_client(cafeteria, nom_client)


def evenement_recharge(cafeteria, numero, heure, nom_client, montant):
    ok, motif = cafeteria.recharger_badge(nom_client, montant)
    if ok:
        print(f"[{numero}] {heure} - Recharge de {nom_client} (+{montant:.2f} €) : ACCEPTÉE")
    else:
        print(f"[{numero}] {heure} - Recharge de {nom_client} (+{montant:.2f} €) : REFUSÉE ({motif})")
    afficher_etat_client(cafeteria, nom_client)


def evenement_reapprovisionnement(cafeteria, numero, heure, code, quantite):
    ok = cafeteria.reapprovisionner(code, quantite)
    if ok:
        print(f"[{numero}] {heure} - Réapprovisionnement de {code} (+{quantite}) : FAIT")
    else:
        print(f"[{numero}] {heure} - Réapprovisionnement de {code} (+{quantite}) : REFUSÉ")


def evenement_annulation(cafeteria, numero, heure, numero_commande):
    annulee, motif, montant = cafeteria.annuler_commande(numero_commande)
    if annulee:
        print(f"[{numero}] {heure} - Annulation de la commande n°{numero_commande} : ACCEPTÉE, {montant:.2f} € remboursés")
    else:
        print(f"[{numero}] {heure} - Annulation de la commande n°{numero_commande} : REFUSÉE ({motif})")


def evenement_rappel(cafeteria, numero, heure, code):
    resume = cafeteria.rappeler_produit(code)
    if resume["motif"] == "":
        print(
            f"[{numero}] {heure} - Rappel de {resume['produit'].nom} : "
            f"{len(resume['commandes_annulees'])} commande(s) annulée(s), "
            f"{resume['montant_total']:.2f} € remboursés"
        )
    else:
        print(f"[{numero}] {heure} - Rappel de {code} : REFUSÉ ({resume['motif']})")


def jouer_la_journee(cafeteria):
    print("[1] 07:30 - Ouverture de la cafétéria")
    evenement_commande(cafeteria, 2, "07:45", "Alice", [("B01", 1), ("V01", 1)])
    evenement_commande(cafeteria, 3, "08:10", "Farid", [("B01", 2)])
    evenement_commande(cafeteria, 4, "08:30", "Bruno", [("B03", 1), ("V01", 3)])
    evenement_recharge(cafeteria, 5, "08:35", "Bruno", 20.00)
    evenement_commande(cafeteria, 6, "08:40", "Bruno", [("B03", 1), ("V01", 3)])
    evenement_commande(cafeteria, 7, "09:15", "Visiteur", [("B02", 1), ("D01", 1)])
    evenement_commande(cafeteria, 8, "11:00", "Chloé", [("P03", 1)])
    evenement_commande(cafeteria, 9, "12:05", "Chloé", [("P03", 1), ("B04", 1), ("D01", 1)])
    evenement_recharge(cafeteria, 10, "12:10", "Alice", 150.00)

    evenement_commande(cafeteria, 11, "12:15", "Bruno", [("P02", 2)])
    evenement_commande(cafeteria, 12, "12:18", "Chloé", [("P02", 1)])

    numero_chloe = None
    for commande in cafeteria.journal:
        if commande.heure == "12:18" and commande.client.nom == "Chloé":
            numero_chloe = commande.numero

    evenement_commande(cafeteria, 13, "12:20", "Alice", [("P02", 1), ("B05", 1), ("D02", 1), ("B01", 1)])
    evenement_annulation(cafeteria, 14, "12:25", numero_chloe)
    evenement_annulation(cafeteria, 15, "12:26", numero_chloe)
    evenement_annulation(cafeteria, 16, "12:27", 999)
    evenement_rappel(cafeteria, 17, "12:30", "P02")
    evenement_commande(cafeteria, 18, "12:35", "Bruno", [("P02", 1)])
    evenement_reapprovisionnement(cafeteria, 19, "12:36", "P02", 10)
    evenement_rappel(cafeteria, 20, "12:40", "P02")

    evenement_commande(cafeteria, 21, "12:45", "Visiteur", [("P01", 16)])
    evenement_commande(cafeteria, 22, "13:00", "Bruno", [("P01", 1), ("B06", 1)])
    evenement_commande(cafeteria, 23, "15:30", "Alice", [("B01", 1), ("D01", 1)])
    evenement_reapprovisionnement(cafeteria, 24, "16:00", "P01", 10)
    evenement_commande(cafeteria, 25, "17:30", "Farid", [("B02", 2)])

    print("[26] 18:30 - Clôture")
    cafeteria.afficher_rapport()


if __name__ == "__main__":
    cafeteria = creer_cafeteria_v2()
    jouer_la_journee(cafeteria)
