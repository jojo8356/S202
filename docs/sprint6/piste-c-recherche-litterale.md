# Sprint 6 — Piste C : Recherche littérale entre guillemets

> **Difficulté** : ⭐. Charge estimée : ~6 h.
> **Énoncé** : *« En tant qu'utilisateur, je tape `"pommes de terre"` entre guillemets pour forcer l'expression exacte. »* (US-06).

## Objectif

Quand l'utilisateur met une partie de sa requête entre guillemets, ne retourner que les pages qui contiennent **littéralement** cette expression (et pas juste les mots, dispersés dans la page).

Exemple : `"pommes de terre" gâteau` →
1. Pages classées par cosinus sur `{pomme, terre, gâteau}` (lemmatisé, stopwords retirés).
2. Filtrage : ne garder que celles qui contiennent la chaîne `pommes de terre` dans le **texte brut**.

## Données fournies

- `contenus_textuels_bruts.7z` (17 Mo) : texte brut de chaque page, **même nom de fichier que l'index** → jointure triviale.

## Approche en 2 phases (cf. CDC §4.8)

### Phase 1 — Recherche vectorielle classique
- Sur l'union des mots dans la requête (lemmatisée, sans stopwords).
- Trier par cosinus, garder les **top 50** (au lieu du top 15 final).

### Phase 2 — Filtrage exact
- Pour chaque page du top 50 :
  - Charger le fichier de contenu brut associé (`bin/CONTENT/<même nom>.txt`).
  - Vérifier `texteBrut.toLowerCase(Locale.FRANCE).contains(fragmentLitteral.toLowerCase(Locale.FRANCE))`.
- Re-classement : seules les pages passant le filtre sont conservées, dans l'ordre de leur cosinus phase 1.
- Afficher le top 15 final.

## Sous-tâches

### S6.C.1 — Décompression de l'archive
- Décompresser `contenus_textuels_bruts.7z` dans `bin/CONTENT/`.
- Vérifier la jointure : `bin/INDEX/Tarte.txt` ↔ `bin/CONTENT/Tarte.txt`.

### S6.C.2 — Parser de requête
- Tokenizer simple : repérer les fragments `"..."` et les mots libres.
- Exemple : `"pommes de terre" gâteau` → `[fragmentLittéral="pommes de terre", motsLibres=["gâteau"]]`.
- Gérer les guillemets non fermés (erreur explicite ou tolérance).
- Gérer les guillemets typographiques `« »` ?

### S6.C.3 — Phase 1 (vectorielle élargie)
- Mots de la requête = mots libres ∪ mots décomposés du fragment littéral (lemmatisés).
- Récupérer top 50 (au lieu de top 15) → laisser de la marge pour le filtrage.

### S6.C.4 — Phase 2 (filtrage exact)
- Charger le contenu brut UNIQUEMENT pour les top 50 (pas pour les 38k pages).
- Recherche `String.contains` insensible à la casse (`Locale.FRANCE`).
- ⚠️ Le contenu brut ≠ le texte lemmatisé : la recherche se fait sur la **forme de surface** (avec accents, conjugaisons).

### S6.C.5 — Tests
- `"pommes de terre"` retourne uniquement les pages contenant la chaîne exacte.
- `"pommes de terre" gâteau` : combinaison fragment littéral + mot libre.
- `pomme terre` (sans guillemets) : comportement v0.5 inchangé.
- Cas limite : guillemet vide `""` → ignoré.

## KPI à mesurer

| Métrique | Cible |
| --- | --- |
| Pertinence sur 20 requêtes étalon | ≥ 90 % |
| Latence ajoutée par requête avec guillemets | ≤ 150 ms |
| Cas où la phase 2 vide tout le top 50 | < 10 % (sinon le seuil top 50 est trop bas) |

## Risques principaux

| Risque | Probabilité | Mitigation |
| --- | :---: | --- |
| Le top 50 vide après filtrage | M | augmenter à top 100, ou retomber sur la phase 1 sans filtrage |
| Lenteur du chargement des contenus bruts | M | charger uniquement pour le top 50, cacher les contenus déjà chargés |
| Sensibilité aux ponctuations (`pommes, de terre`) | M | normaliser ponctuation avant `contains` |

## Références

- [Manning — Phrase queries in IR](https://nlp.stanford.edu/IR-book/html/htmledition/positional-postings-and-phrase-queries-1.html)
- CDC §4.8 — Recherche littérale (rendu final)
