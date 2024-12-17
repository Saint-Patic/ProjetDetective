from datetime import datetime
from utilitaire.commandes_terminale import *


def convertir_date(date) -> str:
    if isinstance(date, str):
        if "/" in date:
            # Format avec des "/"
            return datetime.strptime(date, "%d/%m/%Y").strftime("%d/%m/%Y")
        else:
            # Format avec des "-"
            return datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    elif isinstance(date, datetime):
        # La date est un objet datetime
        return date.strftime("%d/%m/%Y")
    else:
        raise TypeError("La date doit être une chaîne ou un objet datetime.")


def ajouter_indentation(texte, indentation=4):
    espaces_indent = " " * indentation
    lignes_indentees = [espaces_indent + ligne for ligne in texte.splitlines()]
    return "\n".join(lignes_indentees)
