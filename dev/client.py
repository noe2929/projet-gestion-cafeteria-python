"""
Variante : A3 (gros panier) + B3 (client fidèle).
"""

class Client:
    """Un client de la cafétéria, avec son badge (sauf visiteur).
 
    Les quatre profils différents sont :
    "etudiant", "alternant", "personnel", "visiteur".
    """
 
    # Attributs de CLASSE : les règles de la cafétéria
    RECHARGE_MIN = 5.00            # recharge minimale
    RECHARGE_MAX = 100.00          # recharge maximale
    SOLDE_MAX = 150.00             # le solde après recharge ne doit pas dépasser 150€
    DECOUVERT_PERSONNEL = -10.00   # le solde du personnel peut aller jusqu'à -10 €
    SEUIL_FIDELITE = 40.00         # cumul d'achats à partir duquel on a la remise B3
    TAUX_FIDELITE = 0.05           # remise B3 : -5 %
 
    def __init__(self, nom, profil, solde):
        # Attributs d'INSTANCE : propres à chaque client
        self.nom = nom
        self.profil = profil
        self.solde = solde         # solde du badge en €
        self.cumul_achats = 0.0    # total payé jusqu'ici (sert à la fidélité B3)
 
    def recharger(self, montant):
        """Recharge le badge. Renvoie un couple (ok, motif), comme Produit.disponible."""
        # Un visiteur n'a pas de badge
        if self.profil == "visiteur":
            return (False, "pas de badge")
 
        # La recharge doit être comprise entre 5 € et 100 €
        if montant < self.RECHARGE_MIN or montant > self.RECHARGE_MAX:
            return (False, "montant de recharge invalide")
 
        # Le solde après recharge ne doit pas dépasser 150 €.
        # round(..., 2) évite les petites erreurs de calcul des nombres décimaux.
        nouveau_solde = round(self.solde + montant, 2)
        if nouveau_solde > self.SOLDE_MAX:
            return (False, "plafond de solde dépassé")
 
        # Tout est bon : on modifie le solde
        self.solde = nouveau_solde
        return (True, "")
 
    def peut_payer(self, montant):
        """Dit si le client peut payer 'montant' (sans rien modifier). Renvoie True ou False."""
        # Un visiteur paie comptant : il peut toujours payer
        if self.profil == "visiteur":
            return True
 
        # Solde minimum autorisé après paiement : -10 € pour le personnel, 0 € sinon
        if self.profil == "personnel":
            limite = self.DECOUVERT_PERSONNEL
        else:
            limite = 0.0
 
        solde_apres = round(self.solde - montant, 2)
        return solde_apres >= limite
 
    def debiter(self, montant):
        """Débite le badge de 'montant'. Renvoie True si le paiement a eu lieu."""
        # Clause de garde : si le client ne peut pas payer, on ne touche à rien
        if not self.peut_payer(montant):
            return False
 
        # Un visiteur paie comptant : son badge n'existe pas, donc rien à débiter
        if self.profil != "visiteur":
            self.solde = round(self.solde - montant, 2)
        return True
 
    def ajouter_achat(self, montant):
        """Ajoute 'montant' au cumul des achats (fidélité B3). Pas de fidélité pour un visiteur."""
        if self.profil == "visiteur":
            return
        self.cumul_achats = round(self.cumul_achats + montant, 2)
 
    def avantage_fidelite(self):
        """Renvoie la remise B3 du client : 0.05 (5 %) s'il a cumulé 40 € ou plus, sinon 0.0."""
        if self.profil == "visiteur":
            return 0.0
        if self.cumul_achats >= self.SEUIL_FIDELITE:
            return self.TAUX_FIDELITE
        return 0.0
 
    def __str__(self):
        """Affichage pour l'utilisateur : print(client)."""
        return f"{self.nom} ({self.profil}) : solde {self.solde:.2f} €"
 
    def __repr__(self):
        """Affichage pour le programmeur."""
        return f"Client({self.nom!r}, {self.profil!r}, {self.solde})"