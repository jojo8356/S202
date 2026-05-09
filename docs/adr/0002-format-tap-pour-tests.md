# 0002 — Format TAP pour la sortie des tests

- **Status** : Accepted
- **Date** : 2026-05-09
- **Décideur·s** : Johan (CP/D4)
- **Sprint concerné** : transverse, dès v0.1

## Contexte

L'énoncé v0.1 impose une classe `SearchEngineTests` avec un `main` qui exécute des tests. L'énoncé v0.3 textuel : *« tout ce que vous implémentez doit être correctement testé »*. La contrainte « zéro dépendance » exclut JUnit/Mockito.

Il faut donc un format de sortie de tests :
- **lisible humain** (revue manuelle pendant le dev),
- **parsable machine** (intégration CI/CD GitLab),
- **standard** (pour démontrer une démarche pro en soutenance).

## Options envisagées

### Option A — Format ad-hoc `OK <label>` / `FAIL <label>`
- ✅ Pour : ultra simple à écrire.
- ❌ Contre : non standard, non parsable par les outils CI/CD existants, pas de comptage automatique.

### Option B — TAP (Test Anything Protocol)
- Standard universel, language-agnostic, créé pour Perl en 1988, supporté par Jenkins, GitLab CI, Buildkite.
- Format minimal : `1..N` plan + lignes `ok N - <desc>` ou `not ok N - <desc>`.
- ✅ Pour : standard reconnu (Wikipedia, doc Linux Kernel pour KTAP), parsable, lisible humain.
- ❌ Contre : nécessite d'écrire un mini-runner soi-même (mais ~30 lignes).

### Option C — Format JUnit XML
- Format XML produit par JUnit, supporté par tous les CI.
- ✅ Pour : intégration GitLab native (rapport de tests dans la MR).
- ❌ Contre : lourd à produire à la main (XML avec namespaces), illisible humain pendant le dev.

## Décision

> **Option B — TAP (Test Anything Protocol)**

Rationale :
- Lisible humain : `ok 3 - getNorm sur page vide retourne 0` se lit comme une phrase.
- Parsable : grep `^not ok` suffit pour un job de CI minimal.
- Standard reconnu : démontre la démarche pro en soutenance.
- Implémentation triviale : une classe `Assert` de ~50 lignes qui imprime au format TAP.
- Compatible avec une migration future vers JUnit XML si on en a besoin (lib `tap2junit`).

## Conséquences

### Positives
- Sortie de tests homogène entre les 5 sprints.
- Pipeline GitLab CI minimal possible : `grep -q "^not ok" tests.tap && exit 1`.
- Documentation de référence facile : <https://testanything.org/tap-specification.html>.

### Négatives / risques acceptés
- Pas d'intégration JUnit XML native dans la MR GitLab (à voir si on convertit en post-traitement plus tard).
- Pas vu en cours R201 — courte courbe d'apprentissage (mais 5 minutes suffisent).

### Suivi
- ☐ Implémenter `search_engine_tests.Assert` dès v0.1 (cf. project-context §Tests).
- ☐ Pipeline CI bloque la MR si `not ok` détecté (cf. `.gitlab-ci.yml`).

## Références

- [TAP Specification](https://testanything.org/tap-specification.html)
- [TAP for Java — tap4j](http://testanything.org/testing-with-tap/java.html) (lib externe, non utilisée mais référence)
- [Linux Kernel KTAP](https://docs.kernel.org/dev-tools/ktap.html) (variante kernel)
