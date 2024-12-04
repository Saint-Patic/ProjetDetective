import unittest
from datetime import datetime
import json
from unittest.mock import patch, mock_open
from classes.person import Personne


class TestPersonne(unittest.TestCase):
    def setUp(self):
        self.personne = Personne("Doe", "John", "1980-01-01", sexe="Homme")
        self.enqueteur = Personne("Smith", "Jane", "1975-05-15", sexe="Femme")

    def test_initialisation(self):
        self.assertEqual(self.personne.nom, "Doe")
        self.assertEqual(self.personne.prenom, "John")
        self.assertEqual(self.personne.date_de_naissance, "1980-01-01")
        self.assertEqual(self.personne.date_de_deces, "9999-12-31")
        self.assertEqual(self.personne.sexe, "Homme")
        self.assertEqual(self.personne.metier, "'Pas de métier actuellement'")

    def test_date_de_naissance_setter_valide(self):
        self.personne.date_de_naissance = "1990-06-15"
        self.assertEqual(self.personne.date_de_naissance, "1990-06-15")

    def test_date_de_naissance_setter_invalide(self):
        with self.assertRaises(ValueError):
            self.personne.date_de_naissance = "3000-01-01"

    def test_date_de_deces_setter_valide(self):
        self.personne.date_de_deces = "2023-01-01"
        self.assertEqual(self.personne.date_de_deces, "2023-01-01")

    def test_date_de_deces_setter_invalide_futur(self):
        with self.assertRaises(ValueError):
            self.personne.date_de_deces = "3000-01-01"

    def test_date_de_deces_setter_invalide_avant_naissance(self):
        with self.assertRaises(ValueError):
            self.personne.date_de_deces = "1970-01-01"

    def test_ajouter_interrogatoire_valide(self):
        with patch("builtins.open", mock_open(read_data="[]")) as mock_file:
            self.personne.ajouter_interrogatoire("2022-01-01", self.enqueteur, 123)
            mock_file.assert_called_with(
                "fichiers/interrogatoires.json", "r", encoding="utf-8"
            )
            self.assertIn("2022-01-01", self.personne.interrogatoires)

    def test_ajouter_interrogatoire_enqueteur_non_ne(self):
        enqueteur = Personne("Young", "Tom", "2025-01-01")
        with self.assertRaises(ValueError):
            self.personne.ajouter_interrogatoire("2023-01-01", enqueteur, 123)

    def test_ajouter_interrogatoire_personne_morte(self):
        self.personne.date_de_deces = "2020-01-01"
        with self.assertRaises(ValueError):
            self.personne.ajouter_interrogatoire("2022-01-01", self.enqueteur, 123)

    def test_ajouter_interrogatoire_doublon(self):
        with patch("builtins.open", mock_open(read_data="[]")) as mock_file:
            self.personne.ajouter_interrogatoire("2022-01-01", self.enqueteur, 123)
            self.personne.ajouter_interrogatoire("2022-01-01", self.enqueteur, 123)
            data_written = json.loads(mock_file().write.call_args[0][0])
            self.assertEqual(len(data_written), 1)

    def test_obtenir_interrogatoires_existant(self):
        self.personne.interrogatoires = {
            "2022-01-01": [{"id": "123", "enqueteur": "Jane", "num_enquete": 456}]
        }
        result = self.personne.obtenir_interrogatoires("2022-01-01")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "123")

    def test_obtenir_interrogatoires_inexistant(self):
        with self.assertRaises(KeyError):
            self.personne.obtenir_interrogatoires("2023-01-01")

    def test_to_dict(self):
        self.personne.metier = "Développeur"
        expected_dict = {
            "nom": "Doe",
            "prenom": "John",
            "date_de_naissance": "1980-01-01",
            "date_de_deces": "9999-12-31",
            "sexe": "Homme",
            "metier": "Développeur",
            "interrogatoires": {},
            "mail": "",
        }
        self.assertDictEqual(self.personne.to_dict(), expected_dict)

    def test_str(self):
        self.personne.metier = "Développeur"
        self.assertEqual(
            str(self.personne),
            "Doe John, né le 1980-01-01, travaille comme Développeur",
        )

    def test_interrogatoire_fichier_inexistant(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            self.personne.ajouter_interrogatoire("2022-01-01", self.enqueteur, 123)
            self.assertIn("2022-01-01", self.personne.interrogatoires)

    def test_interrogatoire_fichier_corrompu(self):
        with patch("builtins.open", mock_open(read_data="{invalid json}")):
            self.personne.ajouter_interrogatoire("2022-01-01", self.enqueteur, 123)
            self.assertIn("2022-01-01", self.personne.interrogatoires)


if __name__ == "__main__":
    unittest.main()
