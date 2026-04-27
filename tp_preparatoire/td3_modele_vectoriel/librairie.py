import os
from math import sqrt

# Mots vides français : ne portent pas d'information thématique.
# Filtrer ces mots évite que des requêtes du type « pomme de terre »
# soient dominées par les occurrences de « de » présentes partout.
MOTS_VIDES = {
    'a', 'à', 'au', 'aux', 'avec', 'c', 'ce', 'ces', 'cet', 'cette',
    'd', 'dans', 'de', 'des', 'du', 'elle', 'elles', 'en', 'est', 'et',
    'il', 'ils', 'j', 'je', 'l', 'la', 'le', 'les', 'leur', 'leurs',
    'lui', 'm', 'ma', 'mais', 'me', 'mes', 'moi', 'mon', 'n', 'ne',
    'nos', 'notre', 'nous', 'on', 'ou', 'où', 'par', 'pas', 'pour',
    'qu', 'que', 'qui', 's', 'sa', 'sans', 'se', 'ses', 'si', 'son',
    'sur', 't', 'ta', 'te', 'tes', 'toi', 'ton', 'tu', 'un', 'une',
    'vos', 'votre', 'vous', 'y',
}


def produit_scalaire(u,v):
    if len(u) != len(v):
        raise ValueError("Les deux vecteurs n'ont pas les memes dimension.")
    return sum(ui*vi for ui, vi in zip(u, v))

def norme(u):
    return sqrt(produit_scalaire(u, u))

def normaliser(u):
    norme_u = norme(u)
    if norme_u == 0:
        return u
    v = []
    for ui in u:
        v.append(ui/norme_u)
    return v

def lister_mots(fichier):
    "Retourne la liste des mots contenus dans le fichier (mots vides exclus)."
    with open(fichier) as f:
        txt = f.read()
    # Liste des caractères (en minuscules).
    caracteres = list(txt.casefold())
    # On ne garde que les lettres et les espaces.
    txt = ''.join(c for c in caracteres if c.isalpha() or c.isspace())
    # On découpe suivant les espaces et on retire les mots vides.
    return [m for m in txt.split() if m not in MOTS_VIDES]


def generer_donnees(repertoire):
    """Renvoie les 3 listes suivantes:
       - la liste des documents .txt du répertoire,
       - la liste des vecteurs (non normés) correspondants,
       - la liste complète des mots présents."""
    print('Lecture des données...')
    os.chdir(repertoire)
    docs = [nom for nom in os.listdir('.') if nom.endswith('.txt')]
    # `mots` va contenir tous les mots contenus au moins un document.
    mots = set()
    listes_mots = []
    for fichier in docs:
        l_mots = sorted(lister_mots(fichier))
        mots.update(l_mots)
        listes_mots.append(l_mots)
    mots = sorted(mots)
    print(len(mots), 'mots trouvés.')
    # Maintenant qu'on a la liste complète des mots, on peut générer
    # les vecteurs correspondant au nombre d'occurences de chaque mot.
    print('Génération des vecteurs...')
    vecteurs = [[l.count(mot) for mot in mots] for l in listes_mots]
    return docs, vecteurs, mots

def vecteur_requete(requete, mots):
    "Renvoie le vecteur correspondant à la requete (mots vides exclus)."
    l_mots = [m for m in requete.casefold().split() if m not in MOTS_VIDES]
    return [l_mots.count(mot) for mot in mots]
