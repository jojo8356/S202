# Sprint 6 — Piste B : Autocorrection

> **Difficulté** : ⭐⭐. Charge estimée : ~8 h.
> **Énoncé** : *« En tant qu'utilisateur, je tape une faute et le moteur la corrige. »* (US-07).

## Objectif

Lorsqu'un mot de la requête n'apparaît pas dans le vocabulaire indexé (présumé faute de frappe), le remplacer par le mot **le plus proche** au sens d'une distance d'édition.

Bandeau d'avertissement en sortie : *« recherche suggérée : pomme »* quand l'utilisateur tape *« pome »*.

## Approche en 2 passes (cf. CDC §4.7)

### Phase 1 — Pré-sélection rapide par n-grammes (Jaccard)
- Construire un **index n-gram** (n = 2 ou 3) du vocabulaire à l'indexation : pour chaque bigramme, la liste des mots qui le contiennent.
- Pour un mot inconnu, calculer ses bigrammes, récupérer les 50 mots du vocabulaire qui en partagent le plus.
- Distance de Jaccard : `J(A, B) = |A ∩ B| / |A ∪ B|`.
- Coût : O(|n-grammes(mot)|), très rapide.

### Phase 2 — Affinage par Levenshtein
- Sur les ~50 candidats retenus, calculer la **distance de Levenshtein** classique (DP O(|a|·|b|)).
- Garder le candidat avec la plus petite distance, **si distance ≤ 2** (sinon laisser le mot tel quel).

## Sous-tâches

### S6.B.1 — Index n-gram du vocabulaire
- À l'indexation (au démarrage du `SearchEngine`), parcourir tous les mots distincts.
- Pour chaque mot de longueur ≥ n, extraire les bigrammes.
- `HashMap<String, HashSet<String>>` : bigramme → mots qui le contiennent.

### S6.B.2 — Distance de Jaccard
- Pour le mot tapé, extraire ses bigrammes.
- Pour chaque bigramme du mot, agréger les mots candidats (HashSet).
- Calculer `J(bigrammes_mot, bigrammes_candidat)` → trier décroissant, garder top 50.

### S6.B.3 — Distance de Levenshtein DP
- Implémenter en O(|a|·|b|) avec deux lignes de tableau (mémoire O(min(|a|, |b|))).
- Tester sur des paires connues (`cerise` ↔ `cerice` → 1, `pomme` ↔ `pome` → 1).

### S6.B.4 — Intégration dans la pipeline de requête
- Si après lemmatisation un mot n'est pas dans le vocabulaire, lancer la phase 1 + 2.
- Si distance ≤ 2 → remplacer + afficher le bandeau.
- Si distance > 2 → laisser tel quel (probable nom propre, néologisme, etc.).

### S6.B.5 — Tests unitaires
- `pomes` → `pomme` (distance 1)
- `cerice` → `cerise` (distance 1)
- `xyzqwerty` → reste tel quel (pas de candidat à distance ≤ 2)
- Test perf : autocorrection en < 50 ms sur le vocabulaire 38k pages.

## KPI à mesurer

| Métrique | Cible |
| --- | --- |
| Précision suggestion sur 30 fautes étalon | ≥ 80 % |
| Latence ajoutée par requête avec faute | ≤ 100 ms |
| Faux positifs (correction non souhaitée) | ≤ 5 % |

## Risques principaux

| Risque | Probabilité | Mitigation |
| --- | :---: | --- |
| Sur-correction (noms propres, anglais) | M | seuil distance ≤ 2 strict |
| Coût mémoire de l'index n-gram | M | `String.intern()` sur les bigrammes |
| Lenteur Levenshtein sur top-50 | F | mesurer, augmenter à top-20 si besoin |

## Références

- [Algo Jaccard sur n-grammes (Manning, IR)](https://nlp.stanford.edu/IR-book/html/htmledition/k-gram-indexes-for-spelling-correction-1.html)
- [Levenshtein DP standard (Wikipedia)](https://en.wikipedia.org/wiki/Levenshtein_distance)
- [Norvig — How to write a spelling corrector](https://norvig.com/spell-correct.html) (lecture inspirante)
