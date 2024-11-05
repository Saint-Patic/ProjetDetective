from datetime import datetime

def convertir_date(date):
    date_formate = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    return date_formate