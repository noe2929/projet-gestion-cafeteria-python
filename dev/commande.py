"""
CampusCafé : classe Commande (une commande passée par un client).
Variante : A3 (gros panier) + B3 (client fidèle).
"""

class Commande:
    """Une commande : un numéro, un client, une heure et des lignes.

    Une ligne est un couple (produit, quantite), par exemple (cafe, 2).
    Les lignes sont rangées dans une liste : self.lignes.
    """

    # Attribut de CLASSE : le compteur partagé par toutes les commandes, sert à donner un numéro différent à chaque nouvelle commande.
    compteur = 0

    def __init__(self, client, heure):
        # On écrit sur la CLASSE (Commande.compteur), pas sur self :
        # avec self.compteur += 1, on créerait un compteur propre à l'objet.
        Commande.compteur += 1
        self.numero = Commande.compteur   # numéro attribué automatiquement

        # Attributs d'INSTANCE : propres à chaque commande
        self.client = client              # l'objet Client qui commande
        self.heure = heure                # ex. "07:45"
        self.lignes = []                  # une NOUVELLE liste vide pour chaque commande
        self.montant_paye = 0.0           # rempli par la Cafeteria une fois la commande payée

    def ajouter_ligne(self, produit, quantite):
        """Ajoute la ligne (produit, quantite). Renvoie True si la ligne a été ajoutée."""
        if quantite <= 0:
            return False                  # on ne modifie rien
        self.lignes.append((produit, quantite))
        return True

    def calculer_total(self):
        """Renvoie le total de la commande (avant remises), en euros."""
        total = 0.0
        for produit, quantite in self.lignes:
            total += produit.prix * quantite
        # round évite les erreurs de calcul des nombres décimaux
        # (par exemple 1.60 + 3 x 1.20 donne 5.199999999999999 sans round)
        return round(total, 2)

    def __len__(self):
        """len(commande) : le nombre d'articles (la somme des quantités)."""
        nombre = 0
        for produit, quantite in self.lignes:
            nombre += quantite
        return nombre

    def __contains__(self, produit):
        """produit in commande : True si ce produit est dans une des lignes."""
        for produit_de_la_ligne, quantite in self.lignes:
            if produit_de_la_ligne == produit:     # utilise Produit.__eq__ (même code)
                return True
        return False

    def __iter__(self):
        """for ligne in commande : parcourt les lignes (produit, quantite)."""
        return iter(self.lignes)

    def __str__(self):
        """Affichage pour l'utilisateur : la commande sous forme de ticket."""
        ticket = f"--- Commande n°{self.numero} ({self.heure}) - {self.client.nom} ---\n"
        for produit, quantite in self.lignes:
            ticket += f"{quantite} x {produit.nom} : {produit.prix * quantite:.2f} €\n"
        ticket += f"Total : {self.calculer_total():.2f} €\n"
        ticket += f"Montant payé : {self.montant_paye:.2f} €"
        return ticket

    def __repr__(self):
        """Affichage pour le programmeur."""
        return (f"Commande(numero={self.numero}, client={self.client.nom!r}, "
                f"heure={self.heure!r}, lignes={self.lignes})")