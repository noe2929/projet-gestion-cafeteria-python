"""
Variante : A3 (gros panier) + B3 (client fidèle).
"""

class Produit:
    """Un produit de la carte : code, nom, catégorie, prix TTC et stock."""

    # Attributs de CLASSE : les mêmes pour tous les produits
    HEURE_DEBUT_PLATS = "11:30"   # début du créneau des plats (inclus)
    HEURE_FIN_PLATS = "14:00"     # fin du créneau des plats (exclue)

    def __init__(self, code, nom, categorie, prix, stock):
        # Attributs d'INSTANCE : propres à chaque produit
        self.code = code            # ex. "B01"
        self.nom = nom              # ex. "Café expresso"
        self.categorie = categorie  # "boisson chaude", "plat", "dessert"...
        self.prix = prix            # prix en €
        self.stock = stock          # nombre produits en stock

    def disponible(self, quantite, heure):
        """Dit si on peut servir 'quantite' unités à 'heure'.

        Renvoie un couple (ok, motif) :
          (True, "")                   si le produit est disponible
          (False, "rupture de stock")  si le stock est insuffisant
          (False, "hors créneau")      si c'est un plat hors de 11:30-14:00
        Cette méthode ne modifie rien : elle répond seulement.
        """
        # Contrôle 1 : le stock
        if quantite > self.stock:
            return (False, "rupture de stock")

        # Contrôle 2 : le créneau, seulement pour les plats. Les heures sont des chaînes "HH:MM", qui se comparent directement.
        if self.categorie == "plat":
            dans_le_creneau = self.HEURE_DEBUT_PLATS <= heure < self.HEURE_FIN_PLATS
            if not dans_le_creneau:
                return (False, "hors créneau")

        # Aucun contrôle n'a échoué
        return (True, "")

    def vendre(self, quantite):
        """Retire 'quantite' unités du stock. Renvoie True si la vente a eu lieu."""
        if quantite <= 0 or quantite > self.stock:
            return False            # on ne modifie rien
        self.stock -= quantite
        return True

    def reapprovisionner(self, quantite):
        """Ajoute 'quantite' unités au stock. Renvoie True si l'ajout a eu lieu."""
        if quantite <= 0:
            return False            # on ne modifie rien
        self.stock += quantite
        return True

    def __eq__(self, autre):
        """Deux produits sont égaux s'ils ont le même code (pour == et pour in)."""
        return self.code == autre.code      # même code = même produit
    
    def __lt__(self, autre):
        """Un produit est « plus petit » s'il est moins cher (pour <, sorted, max)."""
        return self.prix < autre.prix       # moins cher = « plus petit »
    
    def __str__(self):
        """Affichage pour l'utilisateur : print(produit)."""
        return f"{self.nom} ({self.code}) : {self.prix:.2f} € - stock : {self.stock}"

    def __repr__(self):
        """Affichage pour le programmeur ; {!r} ajoute les guillemets."""
        return (f"Produit({self.code!r}, {self.nom!r}, {self.categorie!r}, "
                f"{self.prix}, {self.stock})")
