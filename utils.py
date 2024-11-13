from datetime import datetime


def convertir_date(date):
    date_formate = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    return date_formate


def ajouter_indentation(texte, indentation=4):
    espaces_indent = " " * indentation
    lignes_indentees = [espaces_indent + ligne for ligne in texte.splitlines()]
    return "\n".join(lignes_indentees)
