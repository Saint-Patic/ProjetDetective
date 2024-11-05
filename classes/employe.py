from person import Person


class Employe(Person):
    _matricule_counter = 1

    def __init__(
        self,
        nom,
        prenom,
        sexe="pas de sexe précisé",
        date_de_naissance="9999-12-31",
        grade="gardien de la paix",
        division="pas de division",
    ):
        super().__init__(nom, prenom, sexe, date_de_naissance)
        self.grade = grade
        self.division = division
        self.matricule = Employe._matricule_counter
        Employe._matricule_counter += 1

    def __str__(self):
        return (
            f"{self.nom} {self.prenom}, Matricule: {self.matricule}, Grade: {self.grade}, "
            f"Division: {self.division}, Date de naissance: {self.date_de_naissance}"
        )
