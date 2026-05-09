# Git hooks de l'équipe HeRVé

Hooks Git **versionnés** dans le repo (au lieu du `.git/hooks/` local de chacun) pour qu'on partage tous les mêmes contrôles automatiques.

## Activation (à faire UNE FOIS par contributeur)

```bash
git config core.hooksPath .githooks
```

Cette commande dit à Git d'utiliser le dossier `.githooks/` du repo plutôt que `.git/hooks/`. Effet local seulement (pas pushé), mais c'est volontaire — chaque contributeur l'active explicitement.

## Hooks installés

| Hook | Quand | Rôle |
| --- | --- | --- |
| `pre-commit` | avant chaque `git commit` | vérifie que les fichiers `.java` staged respectent le **Google Java Style** (cf. [ADR-0001](../docs/adr/0001-google-java-style.md)) |

## Pré-requis

Avoir [`google-java-format`](https://github.com/google/google-java-format) installé localement. Voir [`CONTRIBUTING.md` §6.5](../CONTRIBUTING.md) pour la procédure d'installation par OS.

## Bypass (en cas d'urgence uniquement)

```bash
git commit --no-verify
```

À éviter — le job CI `lint` rattrape de toute façon les fichiers mal formatés et bloque la MR.

## Désactivation

```bash
git config --unset core.hooksPath
```

Revient au comportement par défaut (`.git/hooks/`).
