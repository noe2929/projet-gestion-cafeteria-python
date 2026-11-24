"""
CampusCafé : classe Cafeteria (la caisse). Variante : A3 (gros panier) + B3 (client fidèle).

Elle respecte l’ordre des opérations (Vérifier, Calculer, Encaisser, Enregistrer) et utilise les classes Produit, Client et 
Commande pour traiter chaque commande
"""

from commande import Commande


class Cafeteria:
    """La caisse de la cafétéria.

    Attributs d'instance :
        carte   : dict  code -> Produit     ex. {"B01": <Café expresso>}
        clients : dict  nom -> Client       ex. {"Alice": <Alice>}
        journal : list  de Commande         les commandes ACCEPTÉES seulement
        refus   : dict  motif -> nombre     ex. {"rupture de stock": 1}
    """

    # Attributs de CLASSE : les règles de la variante A3 et du rapport
    SEUIL_GROS_PANIER = 8.00         # A3 : total à atteindre pour avoir une remise
    TAUX_GROS_PANIER_BADGE = 0.10    # A3 : -10 % pour étudiants et alternants
    TAUX_GROS_PANIER_AUTRES = 0.05   # A3 : -5 % pour personnel et visiteurs
    SEUIL_SOLDE_FAIBLE = 3.00        # rapport : badges sous ce solde
    NB_PRODUITS_TOP = 3              # rapport : nombre de produits les plus vendus
    TAUX_BOURSIER = 0.10
    MOTIFS_REFUS = (
        "produit inconnu", "quantité invalide", "rupture de stock",
        "hors créneau", "solde insuffisant", "produit rappelé", "déjà rappelé"
    )

    def __init__(self, produits, clients):
        """produits : list de Produit ; clients : list de Client."""
        # On parcourt les listes reçues pour remplir nos dictionnaires, sans les garder
        self.carte = {}
        for produit in produits:
            self.carte[produit.code] = produit

        self.clients = {}
        for client in clients:
            self.clients[client.nom] = client

        self.journal = []
        self.rappels = {}
        self.refus = {}                  # tous les motifs commencent à 0
        for motif in self.MOTIFS_REFUS:
            self.refus[motif] = 0

    # TRAITER UNE COMMANDE :

    def traiter_commande(self, nom_client, heure, demandes):
        """Traite une commande en 4 étapes. Renvoie un triplet (acceptee, motif, montant).

        nom_client : str   un nom de self.clients      ex. "Alice"
        heure      : str   "HH:MM"                      ex. "07:45"
        demandes   : list  de couples (code, quantite)  ex. [("B01", 1), ("V01", 2)]

        Acceptée : (True, "", montant_paye). Refusée : (False, motif, 0.0), sans RIEN modifier.
        """
        # Cas client inconnu (on ne modifie rien)
        if nom_client not in self.clients:
            return (False, "client inconnu", 0.0)
        client = self.clients[nom_client]

        # ÉTAPE 1 : VÉRIFIER (rien n'est modifié)
        ok, motif = self.verifier_demandes(demandes, heure)
        if not ok:
            return self.refuser(motif)

        # ÉTAPE 2 : CALCULER
        commande = self.creer_commande(client, heure, demandes)
        montant = self.calculer_montant(client, commande)

        # ÉTAPE 3 : ENCAISSER
        if not client.peut_payer(montant):
            Commande.compteur -= 1        # commande refusée : on rend son numéro
            return self.refuser("solde insuffisant")

        # ÉTAPE 4 : ENREGISTRER
        self.enregistrer_commande(client, commande, montant)
        return (True, "", montant)

    def refuser(self, motif):
        """Compte un refus pour 'motif' (str) et renvoie le triplet (False, motif, 0.0)."""
        self.refus[motif] += 1
        return (False, motif, 0.0)

    def regrouper_quantites(self, demandes):
        """Additionne les quantités d'un même produit. Renvoie un dict code -> quantité totale.

        demandes : list de couples (code, quantite). ex. [("B01", 1), ("B01", 2)] -> {"B01": 3}
        """
        totaux = {}
        for code, quantite in demandes:
            if code in totaux:
                totaux[code] += quantite
            else:
                totaux[code] = quantite
        return totaux

    def verifier_demandes(self, demandes, heure):
        """ÉTAPE 1 : vérifie la commande SANS RIEN MODIFIER. Renvoie (ok, motif)."""
        for code, quantite in demandes:               # contrôle 1 : les codes existent
            if code not in self.carte:
                return (False, "produit inconnu")
        for code, quantite in demandes:               # contrôle 2 : les produits rappelés sont refusés
            if self.carte[code].rappele:
                return (False, "produit rappelé")
        for code, quantite in demandes:               # contrôle 3 : les quantités sont > 0
            if quantite <= 0:
                return (False, "quantité invalide")
        totaux = self.regrouper_quantites(demandes)
        for code in totaux:                           # contrôle 3 : stock, puis créneau des plats
            ok, motif = self.carte[code].disponible(totaux[code], heure)
            if not ok:
                return (False, motif)
        return (True, "")

    def creer_commande(self, client, heure, demandes):
        """ÉTAPE 2 (a) : crée la Commande (elle reçoit son numéro) et ses lignes."""
        commande = Commande(client, heure)
        totaux = self.regrouper_quantites(demandes)
        for code in totaux:
            commande.ajouter_ligne(self.carte[code], totaux[code])
        return commande

    def calculer_taux_gros_panier(self, client, total):
        """Remise A3 : renvoie 0.0, 0.05 ou 0.10 selon le Client et le total (float) avant remises."""
        if total < self.SEUIL_GROS_PANIER:      # 8,00 € est inclus : seuil atteint
            return 0.0
        if client.profil == "etudiant" or client.profil == "alternant":
            return self.TAUX_GROS_PANIER_BADGE
        if client.profil == "boursier":
            return self.TAUX_BOURSIER
        return self.TAUX_GROS_PANIER_AUTRES

    def calculer_montant(self, client, commande):
        """ÉTAPE 2 (b) : renvoie le montant à payer. A3 d'abord, puis B3, un seul arrondi."""
        total = commande.calculer_total()                         # avant remises
        taux_a = self.calculer_taux_gros_panier(client, total)    # remise A3
        taux_b = client.avantage_fidelite()                       # avantage B3
        return round(total * (1 - taux_a) * (1 - taux_b), 2)

    def enregistrer_commande(self, client, commande, montant):
        """ÉTAPE 4 : tout est bon, on modifie enfin le solde, la fidélité, le stock et le journal."""
        avantage_avant = client.avantage_fidelite()
        client.debiter(montant)           # un visiteur paie comptant : son solde ne change pas
        client.ajouter_achat(montant)     # cumul pour la fidélité B3
        for produit, quantite in commande:            # utilise Commande.__iter__
            produit.vendre(quantite)
        total_initial = commande.calculer_total()
        commande.montant_paye = montant
        commande.remise = round(total_initial - montant, 2)
        commande.avantage_fidelite = avantage_avant
        commande.statut = "acceptee"
        self.journal.append(commande)

    def annuler_commande(self, numero):
        """Annule une commande acceptée et rembourse son montant réellement payé."""
        commande = None
        for commande_du_journal in self.journal:
            if commande_du_journal.numero == numero:
                commande = commande_du_journal

        if commande is None:
            return (False, "commande inconnue", 0.0)

        if commande.statut == "annulee":
            return (False, "commande déjà annulée", 0.0)

        client = commande.client

        for produit, quantite in commande:
            produit.stock += quantite

        if client.profil != "visiteur":
            client.solde = round(client.solde + commande.montant_paye, 2)

        commande.statut = "annulee"
        self.recalculer_fidelite(client)

        return (True, "", round(commande.montant_paye, 2))

    def recalculer_fidelite(self, client):
        """Rejoue les commandes actives du client dans l'ordre du journal."""
        if client.profil == "visiteur":
            return

        client.cumul_achats = 0.0
        client.fidelite_active = False

        for commande in self.journal:
            if commande.client == client and commande.statut == "acceptee":
                client.ajouter_achat(commande.montant_paye)

    # RECHARGE ET RÉAPPROVISIONNEMENT

    def recharger_badge(self, nom_client, montant):
        """nom_client : str ; montant : float. Renvoie (ok, motif), laissé à Client.recharger."""
        if nom_client not in self.clients:
            return (False, "client inconnu")
        return self.clients[nom_client].recharger(montant)

    def reapprovisionner(self, code, quantite):
        """code : str ; quantite : int. Renvoie True si le stock a augmenté, sinon False."""
        if code not in self.carte:
            return False
        if self.carte[code].rappele:
            self.refus["produit rappelé"] += 1
            return False
        return self.carte[code].reapprovisionner(quantite)

    def rappeler_produit(self, code):
        """Rappelle un produit et annule toutes les commandes actives qui le contiennent."""
        if code not in self.carte:
            self.refus["produit inconnu"] += 1
            return {
                "produit": None,
                "commandes_annulees": [],
                "clients_rembourses": {},
                "montant_total": 0.0,
                "motif": "produit inconnu"
            }

        produit = self.carte[code]

        if produit.rappele:
            self.refus["déjà rappelé"] += 1
            return {
                "produit": produit,
                "commandes_annulees": [],
                "clients_rembourses": {},
                "montant_total": 0.0,
                "motif": "déjà rappelé"
            }

        produit.rappeler()

        commandes_a_annuler = []
        for commande in self.journal:
            if commande.statut == "acceptee":
                contient_produit = False
                for produit_commande, quantite in commande:
                    if produit_commande.code == code:
                        contient_produit = True
                if contient_produit:
                    commandes_a_annuler.append(commande)

        commandes_a_annuler.sort(key=lambda commande: commande.numero)

        commandes_annulees = []
        clients_rembourses = {}
        montant_total = 0.0

        for commande in commandes_a_annuler:
            annulee, motif, montant = self.annuler_commande(commande.numero)
            if annulee:
                commandes_annulees.append(commande.numero)
                nom_client = commande.client.nom
                if nom_client not in clients_rembourses:
                    clients_rembourses[nom_client] = 0.0
                clients_rembourses[nom_client] = round(
                    clients_rembourses[nom_client] + montant, 2
                )
                montant_total = round(montant_total + montant, 2)

        produit.stock = 0

        resume = {
            "produit": produit,
            "commandes_annulees": commandes_annulees,
            "clients_rembourses": clients_rembourses,
            "montant_total": montant_total,
            "motif": ""
        }
        self.rappels[code] = resume
        return resume

    # RAPPORT DE CLÔTURE : 

    def construire_rapport(self):
        """Assemble le rapport de clôture et le RENVOIE. Clés du dictionnaire :

        "nb_acceptees"     : int     commandes acceptées
        "refus"            : dict    motif -> nombre de refus
        "chiffre_affaires" : float   somme des montants payés
        "total_remises"    : float   somme des remises et avantages accordés
        "top_ventes"       : list    de couples (Produit, quantité), du plus vendu au moins vendu
        "carte_triee"      : list    de Produit, du moins cher au plus cher
        "soldes_faibles"   : list    de Client dont le solde est sous SEUIL_SOLDE_FAIBLE
        """
        rapport = {}
        rapport["nb_acceptees"] = len([
            commande for commande in self.journal
            if commande.statut == "acceptee"
        ])
        rapport["refus"] = self.refus
        rapport["chiffre_affaires"] = self.calculer_chiffre_affaires()
        rapport["montant_rembourse"] = self.calculer_montant_rembourse()
        rapport["nb_annulees"] = len([
            commande for commande in self.journal
            if commande.statut == "annulee"
        ])
        rapport["total_remises"] = self.calculer_total_remises()
        rapport["rappels"] = self.rappels
        rapport["top_ventes"] = self.calculer_top_ventes()
        rapport["carte_triee"] = sorted(self.carte.values())    # sorted utilise Produit.__lt__
        rapport["soldes_faibles"] = self.trouver_soldes_faibles()
        return rapport

    def calculer_chiffre_affaires(self):
        """Renvoie la somme des montants payés par toutes les commandes acceptées."""
        chiffre = 0.0
        # Ajoute le montant payé de chaque commande acceptée et non annulée.
        for commande in self.journal:
            if commande.statut == "acceptee":
                chiffre += commande.montant_paye
        return round(chiffre, 2)

    def calculer_montant_rembourse(self):
        """Renvoie la somme réellement remboursée pour les commandes annulées."""
        montant = 0.0
        for commande in self.journal:
            if commande.statut == "annulee":
                montant += commande.montant_paye
        return round(montant, 2)

    def calculer_total_remises(self):
        """Renvoie la somme des remises et avantages : (total avant remises - montant payé)."""
        remises = 0.0
        for commande in self.journal:
            if commande.statut == "acceptee":
                remises += commande.remise
        return round(remises, 2)

    def compter_ventes(self):
        """Renvoie un dict code -> quantité vendue (0 pour un produit jamais vendu)."""
        ventes = {}
        # Initialise tous les produits, même ceux qui n'ont jamais été vendus.
        for code in self.carte:
            ventes[code] = 0
        # Additionne les quantités présentes dans les commandes acceptées et non annulées.
        for commande in self.journal:
            if commande.statut == "acceptee":
                for produit, quantite in commande:
                    ventes[produit.code] += quantite
        return ventes

    def trouver_meilleur_code(self, ventes):
        """Renvoie le code le plus vendu dans 'ventes' (dict code -> quantité), ou None si tout est à 0.

        En cas d'égalité, le premier produit de la carte gagne.
        """
        meilleur_code = None
        meilleure_quantite = 0
        # En cas d'égalité, la carte conserve son ordre initial.
        for code in ventes:
            if ventes[code] > meilleure_quantite:
                meilleur_code = code
                meilleure_quantite = ventes[code]
        return meilleur_code

    def calculer_top_ventes(self):
        """Renvoie les NB_PRODUITS_TOP produits les plus vendus : liste de couples (Produit, quantité)."""
        ventes = self.compter_ventes()
        top = []
        for rang in range(self.NB_PRODUITS_TOP):
            # Sélectionne le meilleur produit puis l'exclut du prochain classement.
            code = self.trouver_meilleur_code(ventes)
            if code is not None:              # None s'il reste moins de 3 produits vendus
                top.append((self.carte[code], ventes[code]))
                ventes[code] = 0              # on le retire pour trouver le suivant
        return top

    def trouver_soldes_faibles(self):
        """Renvoie la liste des Client dont le solde est sous SEUIL_SOLDE_FAIBLE (sans les visiteurs)."""
        soldes_faibles = []
        # Les visiteurs sont exclus puisqu'ils ne possèdent pas de badge.
        for client in self.clients.values():
            if client.profil != "visiteur" and client.solde < self.SEUIL_SOLDE_FAIBLE:
                soldes_faibles.append(client)
        return soldes_faibles

    # AFFICHAGE : 

    def afficher_rapport(self):
        """Affiche le rapport de clôture. Elle ne calcule rien : elle affiche construire_rapport."""
        # Cette méthode se charge uniquement de présenter les résultats.
        rapport = self.construire_rapport()
        print("===== RAPPORT DE CLÔTURE =====")
        print(f"Commandes acceptées : {rapport['nb_acceptees']}")
        self.afficher_refus(rapport["refus"])
        print(f"Chiffre d'affaires : {rapport['chiffre_affaires']:.2f} €")
        print(f"Commandes annulées : {rapport['nb_annulees']}")
        print(f"Montant remboursé : {rapport['montant_rembourse']:.2f} €")
        print(f"Total des remises et avantages : {rapport['total_remises']:.2f} €")
        self.afficher_rappels(rapport["rappels"])
        self.afficher_top_ventes(rapport["top_ventes"])
        self.afficher_carte(rapport["carte_triee"])
        self.afficher_soldes_faibles(rapport["soldes_faibles"])

    def afficher_refus(self, refus):
        """refus : dict motif -> nombre."""
        print("Refus par motif :")
        # Afficher aussi les motifs à zéro rend le bilan complet.
        for motif in refus:
            print(f"  {motif} : {refus[motif]}")

    def afficher_rappels(self, rappels):
        """Affiche chaque rappel avec les clients triés par montant décroissant."""
        print("Rappels de produits :")
        if len(rappels) == 0:
            print("  Aucun rappel")
            return

        for code in rappels:
            rappel = rappels[code]
            produit = rappel["produit"]
            print(f"  {produit.nom} ({code}) : {rappel['montant_total']:.2f} € remboursés")

            clients = []
            for nom_client in rappel["clients_rembourses"]:
                montant = rappel["clients_rembourses"][nom_client]
                clients.append((nom_client, montant))

            clients.sort(key=lambda element: (-element[1], element[0]))
            for nom_client, montant in clients:
                print(f"    {nom_client} : {montant:.2f} €")

    def afficher_top_ventes(self, top):
        """top : list de couples (Produit, quantité)."""
        print(f"Les {self.NB_PRODUITS_TOP} produits les plus vendus :")
        # Chaque ligne contient le nom, le code et la quantité vendue.
        for produit, quantite in top:
            print(f"  {produit.nom} ({produit.code}) : {quantite} vendus")

    def afficher_carte(self, carte_triee):
        """carte_triee : list de Produit. On signale les produits épuisés."""
        print("Carte triée par prix croissant :")
        # Le stock restant est affiché avec chaque produit.
        for produit in carte_triee:
            if produit.rappele:
                print(f"  {produit} - RAPPELÉ")
            elif produit.stock == 0:
                print(f"  {produit} - ÉPUISÉ")
            else:
                print(f"  {produit}")

    def afficher_soldes_faibles(self, soldes_faibles):
        """soldes_faibles : list de Client."""
        print(f"Badges dont le solde est inférieur à {self.SEUIL_SOLDE_FAIBLE:.2f} € :")
        # Seuls les clients sous le seuil sont listés.
        for client in soldes_faibles:
            print(f"  {client}")

    def __repr__(self):
        """Affichage pour le programmeur."""
        return (f"Cafeteria({len(self.carte)} produits, {len(self.clients)} clients, "
                f"{len(self.journal)} commandes acceptées)")