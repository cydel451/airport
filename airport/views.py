from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from datetime import timedelta
from .models import Character, Equipement
from .forms import MoveForm
from random import random

def crash(request):
    pk = Character.objects.filter(failure=True, crashed=False).order_by('end_time_countdown')[0].id_character
    plane = get_object_or_404(Character, pk=pk)
    plane.crashed = True
    plane.save()
    # print(pk, '----------------- test')
    return render(request, 'airport/crash.html', {'plane':plane})

def plane_list(request):
    planes  = Character.objects.filter(crashed=False)
    failures = Character.objects.filter(failure=True, crashed=False).order_by('end_time_countdown')
    return render(request, 'airport/plane_list.html',
                  {'failures':[(plane_.id_character, int((plane_.end_time_countdown - now()).total_seconds())) for plane_ in failures], 'planes':planes})

def flight_detail(request, pk):
    if pk != 'INIT':
        planes  = Character.objects.filter(crashed=False)
        plane = get_object_or_404(Character, pk=pk)
        if request.method == "POST":
            form = MoveForm(request.POST, instance=plane)
        else:
            form = MoveForm()
        
        ancien_lieu = get_object_or_404(Equipement, id_equip=plane.lieu.id_equip)
        ancien_etat = plane.etat

        if form.is_valid():
            liste_etats = ["stationné- libre", "à l'embarquement", "décollage", "vol aller- libre", "escale- libre", "vol retour- libre", "atterrissage", "au débarquement"]
            liste_lieux = ["tarmac", "terminal 1", "piste 1 - piste 2", "espace aérien", "aeroport de destination", "espace aérien", "piste 1 - piste 2", "terminal 1"]

            form.save(commit=False)

            nouveau_lieu = get_object_or_404(Equipement, id_equip=plane.lieu.id_equip)

            i_nouvel_etat = ([ancien_etat in e for e in liste_etats].index(True) + 1)%len(liste_etats)

            if nouveau_lieu.disponibilite == "libre" and i_nouvel_etat in [i for i,x in enumerate([nouveau_lieu.id_equip in e for e in liste_lieux]) if x] and not plane.failure:

                form.save()

                plane.etat = liste_etats[i_nouvel_etat].split('-')[0]

                if plane.lieu.id_equip == "tarmac":
                    plane.proba_failure += 2
                if plane.lieu.id_equip == "espace aérien" and plane.proba_failure/100 > random():
                    plane.failure = True
                    plane.end_time_countdown = now() + timedelta(seconds=10)
                
                plane.save()

                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()

                if not 'libre' in liste_etats[i_nouvel_etat]:
                    nouveau_lieu.disponibilite = "occupe"
                nouveau_lieu.save()
            
            elif plane.failure and nouveau_lieu.id_equip in liste_lieux[6] and nouveau_lieu.disponibilite == "libre":
                form.save()
                plane.etat = "atterrissage"
                plane.proba_failure = 5
                plane.failure = False
                if not 'libre' in liste_etats[i_nouvel_etat]:
                    nouveau_lieu.disponibilite = "occupe"
                nouveau_lieu.save()
                plane.save()

            failures = Character.objects.filter(failure=True, crashed=False).order_by('end_time_countdown')
            return render(request, 'airport/plane_list.html',
                    {'failures':[(plane_.id_character, int((plane_.end_time_countdown - now()).total_seconds())) for plane_ in failures], 'planes':planes})
        else:
            form = MoveForm()
            failures = Character.objects.filter(failure=True, crashed=False).order_by('end_time_countdown')
            return render(request, 'airport/flight_detail.html', 
                        {'plane':plane, 'lieu':plane.lieu, 'form':form, 
                        'failures':[(plane_.id_character, int((plane_.end_time_countdown - now()).total_seconds())) for plane_ in failures], 'planes':planes})
    else:
        init()
        planes  = Character.objects.filter(crashed=False)
        failures = Character.objects.filter(failure=True, crashed=False).order_by('end_time_countdown')
        return render(request, 'airport/plane_list.html',
                  {'failures':[(plane_.id_character, int((plane_.end_time_countdown - now()).total_seconds())) for plane_ in failures], 'planes':planes})


def init():
    planes = Character.objects.all()
    for plane in planes:
        plane.etat = 'escale'
        plane.lieu = get_object_or_404(Equipement, pk='aeroport de destination')
        plane.proba_failure = 5
        plane.failure = False
        plane.crashed = False
        plane.save()
    places = Equipement.objects.all()
    for place in places:
        place.disponibilite = 'libre'
        place.save()