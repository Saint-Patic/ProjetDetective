from utilitaire.commandes_terminale import *
from datetime import datetime


def convertir_date(date) -> str:
    if isinstance(date, str):
        if "/" in date:
            # La date utilise déjà le format avec des /
            try:
                return datetime.strptime(date, "%d/%m/%Y").strftime("%d/%m/%Y")
            except ValueError:
                raise ValueError("La date n'est pas au format valide DD/MM/YYYY.")
        else:
            # La date est au format avec des -
            try:
                return datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                raise ValueError("La date n'est pas au format valide YYYY-MM-DD.")
    elif isinstance(date, datetime):
        # La date est déjà un objet datetime, on la formate
        return date.strftime("%d/%m/%Y")
    else:
        raise TypeError("La date doit être une chaîne ou un objet datetime.")


def ajouter_indentation(texte, indentation=4):
    espaces_indent = " " * indentation
    lignes_indentees = [espaces_indent + ligne for ligne in texte.splitlines()]
    return "\n".join(lignes_indentees)


def organiser_par_section(donnees, chemin_preuves=None):
    """Organise les personnes et preuves par sections."""
    sections = {
        "Employes": [],
        "Criminels": [],
        "Suspects": [],
        "Témoins": [],
        "Preuves": [],
    }
    for personne in donnees:
        classe = personne.get("classe", "Inconnu")
        if classe in ["Employe", "Suspect", "Criminel"]:
            sections[classe + "s"].append(personne)

    if chemin_preuves:
        sections["Preuves"].extend(charger_donnees(chemin_preuves))

    return sections
