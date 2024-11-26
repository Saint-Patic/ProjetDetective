from datetime import datetime
from main import Enquete


def convertir_date(date: str | datetime) -> str:
    if isinstance(date, str):
        # La date est une chaîne, il faut la convertir
        return datetime.strptime(date, "%Y-%m-%d")
    elif isinstance(date, datetime):
        # La date est déjà un objet datetime, on la formate
        return date.strftime("%d/%m/%Y")
    else:
        raise TypeError("La date doit être une chaîne ou un objet datetime.")


def ajouter_indentation(texte, indentation=4):
    espaces_indent = " " * indentation
    lignes_indentees = [espaces_indent + ligne for ligne in texte.splitlines()]
    return "\n".join(lignes_indentees)


def creer_enquete(nom, date_de_debut, date_de_fin):
    """Crée une nouvelle enquête et la sauvegarde dans enquetes.json."""
    try:
        convertir_date(date_de_debut)
        convertir_date(date_de_fin)
    except ValueError:
        raise ValueError("Les dates doivent être au format YYYY-MM-DD.")

    nouvelle_enquete = Enquete(nom, date_de_debut, date_de_fin)
    return nouvelle_enquete
