# Architecture Decision Records (ADR)

Ce dossier contient les **décisions techniques structurantes** prises pendant le projet HeRVé, au format **MADR** (Markdown Architectural Decision Records).

## Pourquoi des ADR ?

L'énoncé v0.3 dit textuellement :

> *« Il vous faudra être capables d'expliquer vos choix et de les défendre lors de la soutenance : quelles étaient les autres possibilités ? pourquoi avoir retenu celle-ci ? »*

Les ADR sont **le format pro standard** pour répondre à cette demande. Chaque décision est :
- **Datée** (numérotation strictement croissante).
- **Justifiée** (alternatives + critères + rationale).
- **Versionnée** dans Git.
- **Lisible** par n'importe quel relecteur (équipier, enseignant).

## Convention de nommage

```
0001-titre-court-en-kebab-case.md
0002-decision-suivante.md
...
```

La numérotation est **immuable** : un ADR n'est jamais renuméroté, même s'il devient `Deprecated`.

## Template

Voir [`template.md`](./template.md). Copier-coller pour créer un nouvel ADR.

## États possibles

| Status | Sens |
| --- | --- |
| `Proposed` | en discussion |
| `Accepted` | décision actée, en vigueur |
| `Deprecated` | décision encore valable mais découragée |
| `Superseded by ADR-XXXX` | remplacée par un ADR plus récent (référencer le numéro) |

## ADR du projet

| # | Titre | Status |
| --- | --- | --- |
| [0001](./0001-google-java-style.md) | Adoption du Google Java Style Guide | Accepted |
| [0002](./0002-format-tap-pour-tests.md) | Format TAP pour la sortie des tests | Accepted |
| [0003](./0003-merge-classique-conventional-commits.md) | Merge classique + Conventional Commits | Accepted |
| [0004](./0004-helper-html-escape.md) | Classe utilitaire HtmlEscape (zéro dépendance) | Accepted |

## Workflow

1. Quelqu'un identifie un choix non-trivial à figer (regex de split, structure de données, lib alternative…).
2. Il copie `template.md` en `XXXX-titre.md` avec le numéro suivant.
3. Il rédige et ouvre une **MR dédiée** sur le dossier `docs/adr/`.
4. Discussion en review. Une fois mergé, status passe à `Accepted`.
5. Si une décision ultérieure annule celle-ci : nouvel ADR avec `Supersedes ADR-XXXX` et l'ancien passe à `Superseded by ADR-YYYY`.

## Référence

- [Michael Nygard — Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [MADR — Markdown Architectural Decision Records](https://adr.github.io/madr/)
- [AWS — Master ADRs Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
