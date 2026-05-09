# 0003 — Merge classique + Conventional Commits

- **Status** : Accepted
- **Date** : 2026-05-09
- **Décideur·s** : Johan (CP)
- **Sprint concerné** : transverse

## Contexte

L'énoncé v0.1 impose le workflow GitLab : branches `v0.X`, tags `v0.X`, *« Attention à scrupuleusement respecter les noms de branche et de commit »*. L'historique Git sera relu en soutenance et **pour la répartition des points** entre équipiers.

Deux choix transverses à figer :
1. **Stratégie de merge** des MR (squash, classique, rebase).
2. **Format des messages de commit** (libre, Conventional Commits, autre).

## Options envisagées (1 — stratégie de merge)

### A1 — Squash merge
- Tous les commits d'une MR fusionnés en un seul lors du merge dans `v0.X`.
- ✅ Pour : historique linéaire propre.
- ❌ Contre : perd la granularité des commits intermédiaires (utile pour la traçabilité par équipier en soutenance).

### A2 — Merge classique (avec commit de merge)
- Préserve tous les commits de la MR + ajoute un commit de merge.
- ✅ Pour : historique complet, traçabilité fine.
- ❌ Contre : graphe Git en branches (lisible avec `git log --graph`).

### A3 — Rebase merge
- Replay des commits de la MR sur `v0.X` sans commit de merge.
- ✅ Pour : historique linéaire ET commits préservés.
- ❌ Contre : réécriture d'historique, conflits possibles si plusieurs équipiers parallèlement.

## Options envisagées (2 — format des commits)

### B1 — Format libre
- ✅ Pour : zéro contrainte.
- ❌ Contre : incohérence, messages illisibles type *« fix »*, *« WIP »*.

### B2 — Conventional Commits (`feat(scope): desc`)
- Standard reconnu (Angular, Vue, kernel Linux récemment).
- ✅ Pour : pro, lisible, génération de changelog automatique possible.
- ❌ Contre : courte courbe d'apprentissage.

### B3 — Format custom interne
- ✅ Pour : taillé au projet.
- ❌ Contre : non transférable, énergie perdue.

## Décision

> **Option A2 (merge classique) + Option B2 (Conventional Commits)**

Rationale :
- **Merge classique** : préserver la granularité fine des commits de feature pour la **soutenance et la répartition des points**. Chaque équipier doit pouvoir pointer ses contributions précises. La lisibilité du graphe est secondaire.
- **Conventional Commits** : format pro reconnu, démontre la démarche en soutenance, permet à un agent IA (revue automatique) de classifier les changements (`feat` vs `fix` vs `docs`).

## Conséquences

### Positives
- Traçabilité fine par équipier (utile S7.2 — répartition des points).
- Format de commit cohérent et professionnel.
- Possibilité de générer un changelog automatique avec `git-cliff` ou équivalent.

### Négatives / risques acceptés
- Graphe Git non linéaire — assumé, lisible avec `git log --graph --oneline`.
- Effort initial pour acclimater l'équipe au format Conventional Commits (cf. `CONTRIBUTING.md` §3).

### Suivi
- ☐ Configurer GitLab : *Merge method* = `Merge commit` (Settings > General > Merge requests).
- ☐ Documenter dans `CONTRIBUTING.md` §3.
- ☐ Reviewer pédagogue sur les premiers commits qui ne respectent pas le format.

## Références

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Angular commit message guidelines](https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md)
- [GitLab — Merge methods](https://docs.gitlab.com/ee/user/project/merge_requests/methods/)
