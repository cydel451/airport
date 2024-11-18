from django.db import models
 
class Equipement(models.Model):
    id_equip = models.CharField(max_length=100, primary_key=True)
    disponibilite = models.CharField(max_length=20)
    # photo = models.CharField(max_length=200)
    def __str__(self):
        return self.id_equip
 
 
class Character(models.Model):
    id_character = models.CharField(max_length=100, primary_key=True)
    etat = models.CharField(max_length=20)
    ligne = models.CharField(max_length=50, null=True)
    compagnie = models.CharField(max_length=20, null=True)
    photo = models.CharField(max_length=500, null=True)
    logo_compagnie = models.CharField(max_length=500, null=True)
    lieu = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    proba_failure = models.IntegerField(null=True)
    failure = models.BooleanField(null=True)
    end_time_countdown = models.DateTimeField(null=True)
    crashed = models.BooleanField(null=True)
    def __str__(self):
        return self.id_character
    def print_lieu(self):
        d = {
            "stationné":f"est stationné sur le {self.lieu}.", 
            "à l'embarquement":f"est à l'embarquement au {self.lieu}.",
            "au débarquement":f"est au débarquement au {self.lieu}.",
            "décollage":f"décolle de la {self.lieu}.",
            "atterrissage":f"atterit sur la {self.lieu}.",
            "vol aller":f"vole vers l'aéroport de {self.ligne.split(' - ')[0]}.",
            "vol retour":f"vole vers l'aéroport de {self.ligne.split(' - ')[1]}.",
            "escale":f"est en escale à {self.ligne.split(' ')[0]}."
            }
        if self.failure:
            return "subit un problème, il doit atterrir au plus vite !"
        else:
            return d[self.etat]
    def print_place(self):
        return self.lieu if self.lieu.id_equip != "aeroport de destination" else self.ligne.split(' - ')[0]