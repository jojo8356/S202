from librairie import (produit_scalaire, norme, normaliser,
                       lister_mots, generer_donnees, vecteur_requete)

docs, vecteurs, mots = generer_donnees('.')

# Vecteurs normalisés
vects = [normaliser(v) for v in vecteurs]

# La requete est également mise sous la forme d'un vecteur normalisé
requete = input('Effectuez une recherche:')
r = vecteur_requete(requete, mots)
r = normaliser(r)

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
 
