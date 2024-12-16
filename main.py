from utilitaire import utils
from classes import (
    Personne,
    Temoin,
    Suspect,
    Employe,
    Criminel,
    Evenement,
    Preuve,
    Enquete,
)


def creer_enquete(nom, date_de_debut, date_de_fin):
    """Crée une nouvelle enquête et la sauvegarde dans enquetes.json."""
    try:
        utils.convertir_date(date_de_debut)
        utils.convertir_date(date_de_fin)
    except ValueError:
        raise ValueError("Les dates doivent être au format YYYY-MM-DD.")

    nouvelle_enquete = Enquete(nom, date_de_debut, date_de_fin)
    return nouvelle_enquete


if __name__ == "__main__":

    Vol = creer_enquete("Vol", "2023-01-01", "2023-06-30")
    Fraude = creer_enquete("Fraude", "2023-07-01", "2023-12-31")
    Meurtre = Enquete("Meurtre", "2003-08-04", "2005-02-26", [], [])
    Cambriolage = Enquete("Cambriolage", "2010-06-15", "2011-08-01", [], [])

    Alexis = Personne("Demarcq", "Alexis", "2003-08-04", "Homme")
    Nathan = Employe("Lemaire", "Nathan", "2003-01-01", "Homme")
    Quentin = Suspect("Henrard", "Quentin", "2003-08-04", "Homme")
    Tristan = Criminel("Valcke", "Tristan", "2003-08-04", "Homme")

    Meurtre.ajouter_personne(Alexis)
    Meurtre.ajouter_personne(Quentin)
    Cambriolage.ajouter_personne(Alexis)
    Cambriolage.ajouter_personne(Nathan)

    # Afficher les enquêtes liées
    Vol.ajouter_enquetes_liees(Fraude)
    Meurtre.afficher_enquetes_liees()
    Meurtre.ajouter_enquetes_liees(Cambriolage)
    Meurtre.ajouter_enquetes_liees(Vol)
    Meurtre.afficher_enquetes_liees()
    Vol.afficher_enquetes_liees()

    # Sauvegarder les enquêtes
    # Vol.sauvegarder_enquete()
    # Fraude.sauvegarder_enquete()
    # Meurtre.sauvegarder_enquete()
    # Cambriolage.sauvegarder_enquete()

    # Afficher les preuves
    # Meurtre.ajouter_preuves("Arme")
    # Meurtre.ajouter_preuves("Indice")
    # Cambriolage.ajouter_preuves("Arme")
    # Meurtre.afficher_preuves()
    # Cambriolage.afficher_preuves()

    # Afficher les enquêtes existantes
    # Enquete.afficher_enquetes()

    # Afficher les évènements
    # Meurtre.ajouter_evenement("Découverte du corps")
    # Meurtre.afficher_evenements()
    # Cambriolage.afficher_evenements()

    # Afficher les interrogatoires
    # Alexis.ajouter_interrogatoire("2004-01-01", Nathan, Meurtre.id)
    # Quentin.ajouter_interrogatoire("2005-11-22", Nathan, Cambriolage.id)
    # Alexis.ajouter_interrogatoire("2002-01-21", Nathan, Cambriolage.id)
    # Meurtre.afficher_interrogatoires(Meurtre.id)
    # Cambriolage.afficher_interrogatoires(Cambriolage.id)

    # Clôturer une enquête
    # Cambriolage.cloturer_enquete()

    # Générer un rapport
    # Enquete.generer_rapport(1)
    # Enquete.generer_rapport(2)
