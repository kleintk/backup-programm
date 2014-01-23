'''
Created on 23.01.2014

@author: Phate aka kleintk

TO DO:
- Vernueftiges Bedienkonzept einfuegen
- CLI oder GUI
'''

'''
Bedienungsanleitung:
- in:
quelle_root_verzeichnis = "c:/Users/Phate/workspace/backup-programm/src/test-umgebung/quelle"
ziel_root_verzeichnis = "c:/Users/Phate/workspace/backup-programm/src/test-umgebung/ziel/zielOrt"
-- seine Quell- und Ziel-Ordner des Abgleichs einfuegen
-- Script ausfuehren
-- Abgleich beendet

'''


import os
import os.path
import glob
import shutil

    
#-------------------------------------------------------------------------------------------------------------------------------

#vergleicht und kopiert datei wenn notwendig
def vergleichenUndKopieren(pfad_alt_komplett):
    #print(pfad_alt_komplett)
    pfad_relativ = os.path.relpath(pfad_alt_komplett, quelle_root_verzeichnis)
    pfad_neu_komplett = ziel_root_verzeichnis + "\\" + pfad_relativ
    #print(pfad_neu_komplett)
    #erstelle neuen ordner falls notwendig
    try:
        os.makedirs(os.path.dirname(pfad_neu_komplett))
    except FileExistsError:
        #print("Gibts schon.")
        pass
        
    props_alt = os.stat(pfad_alt_komplett)
    try:
        props_neu = os.stat(pfad_neu_komplett)
    except:
        #datei ist neu, wird also erstellt
        print(pfad_relativ + " - wurde erstellt")   #pfad_relativ    #os.path.basename(pfad_neu_komplett)
        shutil.copy2(pfad_alt_komplett, pfad_neu_komplett)
    #kopiert die datei, wenn diese schon existiert
    try:
        #pruefen ob die alte datei geaendert wurde, nur bei aenderung wird kopiert
        if (props_alt[8] > props_neu[8]):
            shutil.copy2(pfad_alt_komplett, pfad_neu_komplett)
            print(pfad_relativ + " - Aenderung gefunden - wurde kopiert")   #pfad_relativ    #os.path.basename(pfad_neu_komplett)
        else:
            #print(pfad_relativ + " - keine Aenderung -> keine kopie")   #pfad_relativ    #os.path.basename(pfad_neu_komplett)
            pass
    except:
        #neue datei existiert noch nicht
        pass
    


#erstellt einen Ordner falls noch nicht vorhanden (betrifft nur leere ordner) ordner mit inhalt
#werden in vergleichenUndKopieren() mit erstellt
def nurLeererOrdnerErstellen(pfad_alt):
    pfad_relativ = os.path.relpath(pfad_alt, quelle_root_verzeichnis)
    pfad_neu_komplett = ziel_root_verzeichnis + "\\" + pfad_relativ
    try:
        #print(pfad_neu_komplett)
        os.makedirs(pfad_neu_komplett)
    except FileExistsError:
        #print("Gibts schon.")
        pass

# kopiert daten von quelle -> Ziel
def rekursiverDurchlaufQuelleNachZiel(pfad):
    objects = os.listdir(pfad)
    objects.sort()
    
    #anzahlObjekte = len(objects)
    #print(anzahlObjekte)
    
    for objectname in objects:
        
        #falls Ordner, ruf die selber wieder auf
        if os.path.isdir(pfad + "\\" + objectname) == True:
            #print(objectname + " - ist ein Ordner")
            nurLeererOrdnerErstellen(pfad + "\\" + objectname)
            rekursiverDurchlaufQuelleNachZiel(pfad + "\\" + objectname)
        
        #falls Datei, fuehre vergleichs und kopieroperation aus
        if os.path.isfile(pfad + "\\" + objectname) == True:
            #print(objectname + " - ist ein File")
            vergleichenUndKopieren(pfad + "\\" + objectname)
        
        #falls Verknuepfung, fuehre vergleichs und kopieroperation aus 
        if os.path.islink(pfad + "\\" + objectname) == True:
            #print(objectname + " - ist eine Verknuepfung")        
            vergleichenUndKopieren(pfad + "\\" + objectname)


#-----------------------------------------------------------------------------------------------------------------------------------------


#pruefe ob ordner noch existiert, wenn nein loesche, wenn ja
def existenzPruefenUndggfOrdnerLoeschen(pfad_ziel):
    pfad_relativ = os.path.relpath(pfad_ziel, ziel_root_verzeichnis)
    pfad_quelle_komplett = quelle_root_verzeichnis + "\\" + pfad_relativ

    if os.path.exists(pfad_quelle_komplett) == True:
        #print(pfad_quelle_komplett, " - Ordner existiert.")
        pass
    else:
        print(pfad_quelle_komplett, " - Ordner existiert nicht mehr.")
        #shutil.rmtree(pfad_ziel) <--- geht noch nicht, da dieser ordner ja unten in der for schleife nochmals durchsucht wird
        #muss also in eine loesch-liste eingetragen werden
        loeschlisteOrdner.append(pfad_ziel)


#pruefe ob ordner noch existiert, wenn nein loesche, wenn ja
def existenzPruefenUndggfDateiLoeschen(pfad_ziel):
    pfad_relativ = os.path.relpath(pfad_ziel, ziel_root_verzeichnis)
    pfad_quelle_komplett = quelle_root_verzeichnis + "\\" + pfad_relativ

    if os.path.exists(pfad_quelle_komplett) == True:
        #print(pfad_quelle_komplett, " - Datei existiert.")
        pass
    else:
        print(pfad_quelle_komplett, " - Datei existiert nicht mehr. Wird geloescht.")
        os.remove(pfad_ziel)




# loescht daten die in quelle nichtmehr existieren, wird mit pfad des ziels initialisiert
def rekursiverDurchlaufLoescheUeberzaehligeDatenInZiel(pfad):
    objects = os.listdir(pfad)
    objects.sort()
    
    #anzahlObjekte = len(objects)
    #print(anzahlObjekte)
    
    for objectname in objects:
        
        #falls Ordner, ruf die selber wieder auf
        if os.path.isdir(pfad + "\\" + objectname) == True:
            #print(objectname + " - ist ein Ordner")
            #pruefe ob ordner noch existiert, wenn nein loesche, wenn ja rufe dich selber wieder auf
            existenzPruefenUndggfOrdnerLoeschen(pfad + "\\" + objectname)
            rekursiverDurchlaufLoescheUeberzaehligeDatenInZiel(pfad + "\\" + objectname)
            '''
            nurLeererOrdnerErstellen(pfad + "\\" + objectname)
            rekursiverDurchlaufLoescheUeberzaehligeDatenInZiel(pfad + "\\" + objectname)
            '''
        
        #falls Datei, fuehre vergleichs und kopieroperation aus
        if os.path.isfile(pfad + "\\" + objectname) == True:
            #print(objectname + " - ist ein File")
            #pruefe ob datei noch existiert, wenn ja, tu nix, wenn nein, loesche datei
            existenzPruefenUndggfDateiLoeschen(pfad + "\\" + objectname)
            '''
            vergleichenUndKopieren(pfad + "\\" + objectname)
            '''
            pass
        
        #falls Verknuepfung, fuehre vergleichs und kopieroperation aus 
        if os.path.islink(pfad + "\\" + objectname) == True:
            #print(objectname + " - ist eine Verknuepfung")
            #pruefe ob link noch existiert, wenn ja, tu nix, wenn nein, loesche link
            existenzPruefenUndggfDateiLoeschen(pfad + "\\" + objectname)
            '''       
            vergleichenUndKopieren(pfad + "\\" + objectname)
            '''
            pass






def abgleichAusfuehren():
    
    rekursiverDurchlaufQuelleNachZiel(quelle_root_verzeichnis)

    
    rekursiverDurchlaufLoescheUeberzaehligeDatenInZiel(ziel_root_verzeichnis)
    
    for ordnerPfad in loeschlisteOrdner:
        
        try:
            shutil.rmtree(ordnerPfad)
        except:
            #weil auch unterordner in der liste stehen kann das loeschen schief gehen
            pass

        
    print("----------------------------\nAbgleich erfolgreich durchgefuehrt.")











#--------------------------------------------------------------------------------------------------------------------------------------------

quelle_root_verzeichnis = "c:/Users/Phate/workspace/backup-programm/src/test-umgebung/quelle"
ziel_root_verzeichnis = "c:/Users/Phate/workspace/backup-programm/src/test-umgebung/ziel/zielOrt"
quelle_root_verzeichnis = os.path.normcase(quelle_root_verzeichnis) #macht aus /   --->  \   von hand muesste man \\ schreiben
ziel_root_verzeichnis = os.path.normcase(ziel_root_verzeichnis)

loeschlisteOrdner = []

abgleichAusfuehren()




