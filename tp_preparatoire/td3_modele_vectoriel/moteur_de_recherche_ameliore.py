from librairie import (produit_scalaire, norme, normaliser,
                       lister_mots, generer_donnees, vecteur_requete)
from math import log


def coefficienter(vecteur, coeffs):
    u = []
    for i in range(len(coeffs)):
        u.append(vecteur[i]*coeffs[i])
    return u
# ou:
# def coefficienter_vecteur2(v, coeffs):
#     return [vi*c for vi, c in zip(v, coeffs)]

docs, vecteurs, mots = generer_donnees('.')

# On génère les coefficients de pertinence
# Nombre de documents :
D = len(docs)
# Nombre de documents contenant chaque mot :
d = []
for i in range(len(mots)):
    total = 0
    for v in vecteurs:
        if v[i] != 0:
            total += 1
    d.append(total)

coeffs = [log(D/di) for di in d]


# Vecteurs normalisés
vects = [normaliser(coefficienter(v, coeffs)) for v in vecteurs]



# La requete est également mise sous la forme d'un vecteur normalisé
requete = input('Effectuez une recherche:')
r = vecteur_requete(requete, mots)
r = normaliser(coefficienter(r, coeffs))

similitudes = [produit_scalaire(r, v) for v in vects]

# Affichage des résultats par ordre décroissant de similitude avec la requete :
# - On associe à chaque degré de similitude le nom du document:
sims_noms = zip(similitudes, docs)
# - On trie selon le degré de similitude décroissant
sims_noms = sorted(sims_noms, reverse=True)
# - On affiche les noms de documents

print('\nRésultats de la recherche:')
for sim, nom in sims_noms:
    if sim > 0:
        print('-', nom, '-> pertinence :', sim)
 
