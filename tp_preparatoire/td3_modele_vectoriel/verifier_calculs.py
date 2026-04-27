"""Vérification arithmétique exacte des calculs de l'exercice 13 du TD1.

Le but est de s'assurer que les valeurs reportées dans `reponses.pdf`
sont correctes au-delà de toute imprécision flottante :
- Les normes au carré sont entières (Fraction)
- Les similarités cosinus sont des fractions exactes
- Les racines carrées sont calculées avec Decimal à 50 chiffres
"""

from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 50  # 50 chiffres significatifs


def sqrt_decimal(n):
    """Racine carrée exacte (Newton) sur Decimal à la précision courante."""
    n = Decimal(n)
    if n == 0:
        return Decimal(0)
    x = n
    last = Decimal(0)
    while x != last:
        last = x
        x = (x + n / x) / 2
    return x


# Données du tableau de l'exercice 13
# Ordre des mots : (aubergine, courgette, poivron, tomate)
documents = {
    'd1': (0, 2, 2, 12),
    'd2': (3, 1, 3, 6),
    'd3': (4, 3, 2, 5),
    'd4': (7, 8, 0, 17),
    'd5': (3, 5, 1, 6),
}

requete = (0, 0, 1, 1)  # « tomate poivron »

print("=" * 70)
print("EXERCICE 13.1 — Calcul des normes et des cosinus (sac de mots)")
print("=" * 70)

# Norme au carré (entier exact)
norm2 = {nom: sum(c * c for c in v) for nom, v in documents.items()}
print("\nNormes au carré (exactes) :")
for nom, n2 in norm2.items():
    print(f"  ||{nom}||^2 = {n2:>4}    ||{nom}|| = {sqrt_decimal(n2)}")

norm_r2 = sum(c * c for c in requete)  # = 2
print(f"\n||r||^2 = {norm_r2}    ||r|| = {sqrt_decimal(norm_r2)}")

# Vecteurs normalisés u_i = d_i / ||d_i||
print("\nVecteurs normalisés u_i = d_i / ||d_i|| (4 décimales) :")
print(f"  {'doc':<4} {'u_i,1':>9} {'u_i,2':>9} {'u_i,3':>9} {'u_i,4':>9}")
norms_u = {}
for nom, v in documents.items():
    n = sqrt_decimal(norm2[nom])
    u = tuple(Decimal(c) / n for c in v)
    norms_u[nom] = u
    print(f"  {nom:<4} " + " ".join(f"{x:>9.4f}" for x in u))

# Produit scalaire requête·document (entier exact)
print("\nProduits scalaires r·d (exacts) :")
prods = {}
for nom, v in documents.items():
    p = sum(r * d for r, d in zip(requete, v))
    prods[nom] = p
    print(f"  r·{nom} = 0 + 0 + {requete[2]}*{v[2]} + {requete[3]}*{v[3]} = {p}")

# Cosinus = (r·d) / (||r|| * ||d||)
print("\nCosinus de similarité (haute précision) :")
print(f"  {'doc':<4} {'r·d':>4} {'||r||·||d||':>30} {'cos':>30}")
sims_brutes = {}
for nom, v in documents.items():
    p = prods[nom]
    denom = sqrt_decimal(norm_r2) * sqrt_decimal(norm2[nom])
    cos = Decimal(p) / denom
    sims_brutes[nom] = cos
    print(f"  {nom:<4} {p:>4} {str(denom)[:30]:>30} {str(cos)[:30]:>30}")

# Classement
ranked = sorted(sims_brutes.items(), key=lambda kv: kv[1], reverse=True)
print("\nClassement sac de mots brut :")
print("  " + " > ".join(nom for nom, _ in ranked))

print()
print("=" * 70)
print("EXERCICE 13.2 — Pondération TF-IDF")
print("=" * 70)

# Coefficients de pertinence c_i = ln(D / d_i)
# D = 5, d_i = nb de documents contenant le mot i
D = len(documents)
mots = ['aubergine', 'courgette', 'poivron', 'tomate']
d_freq = []
for i in range(4):
    nb = sum(1 for v in documents.values() if v[i] > 0)
    d_freq.append(nb)

print(f"\nD = {D} documents")
print(f"d_i (nb de documents contenant le mot) :")
for nom_mot, di in zip(mots, d_freq):
    print(f"  d({nom_mot}) = {di}")

print("\nCoefficients c_i = ln(D / d_i) :")
import math
coeffs = []
for nom_mot, di in zip(mots, d_freq):
    c = Decimal(str(math.log(D / di)))
    coeffs.append(c)
    print(f"  c({nom_mot:<10}) = ln({D}/{di}) = {c}")

# Vecteurs pondérés et leurs normes
print("\nVecteurs pondérés et normes :")
vects_pond = {}
norms_pond = {}
for nom, v in documents.items():
    vp = tuple(Decimal(c) * coeffs[i] for i, c in enumerate(v))
    vects_pond[nom] = vp
    n2 = sum(x * x for x in vp)
    norms_pond[nom] = n2.sqrt() if hasattr(n2, 'sqrt') else sqrt_decimal(n2)
    # Decimal.sqrt() existe : on l'utilise
    norms_pond[nom] = n2.sqrt()
    print(f"  {nom}_pond = ({', '.join(f'{x:.4f}' for x in vp)})")
    print(f"     ||  || = {norms_pond[nom]:.6f}")

# Vecteur requête pondéré
r_pond = tuple(Decimal(c) * coeffs[i] for i, c in enumerate(requete))
norm_r_pond = (sum(x * x for x in r_pond)).sqrt()
print(f"\n  r_pond = ({', '.join(f'{x:.4f}' for x in r_pond)})")
print(f"  ||r_pond|| = {norm_r_pond:.6f}")

# Cosinus pondérés
print("\nCosinus pondérés (TF-IDF) :")
sims_tfidf = {}
for nom, vp in vects_pond.items():
    p = sum(r * d for r, d in zip(r_pond, vp))
    if norms_pond[nom] == 0:
        cos = Decimal(0)
    else:
        cos = p / (norm_r_pond * norms_pond[nom])
    sims_tfidf[nom] = cos
    print(f"  cos(r, {nom}) = {cos:.10f}")

ranked_tfidf = sorted(sims_tfidf.items(), key=lambda kv: kv[1], reverse=True)
print("\nClassement TF-IDF :")
print("  " + " > ".join(nom for nom, _ in ranked_tfidf))

print()
print("=" * 70)
print("RÉCAPITULATIF DES VALEURS REPORTÉES DANS reponses.md")
print("=" * 70)

print("\nValeurs attendues (à 4 décimales) :")
attendues_brutes = {
    'd1': '0.8030', 'd2': '0.8581', 'd3': '0.6736',
    'd4': '0.5995', 'd5': '0.5874',
}
attendues_tfidf = {
    'd1': '1.0000', 'd2': '0.7071', 'd3': '0.4472',
    'd4': '0.0000', 'd5': '0.3162',
}

print("\n  Vecteurs normalisés u_i (4 décimales attendues) :")
attendues_u = {
    'd1': ('0.0000', '0.1622', '0.1622', '0.9733'),
    'd2': ('0.4045', '0.1348', '0.4045', '0.8090'),
    'd3': ('0.5443', '0.4082', '0.2722', '0.6804'),
    'd4': ('0.3491', '0.3990', '0.0000', '0.8479'),
    'd5': ('0.3560', '0.5934', '0.1187', '0.7121'),
}
ok = True
for nom in documents:
    calc = tuple(f"{x:.4f}" for x in norms_u[nom])
    exp = attendues_u[nom]
    badge = "OK " if calc == exp else "KO!"
    if calc != exp:
        ok = False
    print(f"    {badge}  {nom}: attendu {exp}  /  calculé {calc}")

print("\n  Cosinus sac de mots :")
for nom, exp in attendues_brutes.items():
    calc = f"{sims_brutes[nom]:.4f}"
    badge = "OK " if calc == exp else "KO!"
    if calc != exp:
        ok = False
    print(f"    {badge}  {nom}: attendu {exp}  /  calculé {calc}")

print("\n  TF-IDF :")
for nom, exp in attendues_tfidf.items():
    calc = f"{sims_tfidf[nom]:.4f}"
    badge = "OK " if calc == exp else "KO!"
    if calc != exp:
        ok = False
    print(f"    {badge}  {nom}: attendu {exp}  /  calculé {calc}")

print()
print("=" * 70)
if ok:
    print("✅ TOUS LES CALCULS SONT CONFIRMÉS")
else:
    print("⚠️  ÉCARTS DÉTECTÉS — relire reponses.md")
print("=" * 70)
