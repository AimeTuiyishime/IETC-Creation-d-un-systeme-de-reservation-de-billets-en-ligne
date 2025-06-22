class CategorieDeSiege:
    def __init__(self, idCategorie, nomCategorie, prix):
        self.idCategorie = idCategorie
        self.nomCategorie = nomCategorie
        self.prix = prix
    
    def __str__(self):
        return f"[{self.idCategorie}] {self.nomCategorie} - {self.prix} "