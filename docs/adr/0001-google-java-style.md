# 0001 — Adoption du Google Java Style Guide

- **Status** : Accepted
- **Date** : 2026-05-09
- **Décideur·s** : Johan (CP)
- **Sprint concerné** : transverse

## Contexte

Le projet S2.02 attend un rendu **professionnel** (cf. énoncé v0.3 : *« il vous faudra être capables d'expliquer vos choix et de les défendre »*). Sans convention de style explicite, l'équipe (5 personnes) risque des incohérences de formatage qui rendent les revues de MR pénibles et masquent les vrais problèmes.

Le programme R201 enseigne :
- CamelCase pour les identificateurs (1ère lettre majuscule pour classes, minuscule pour méthodes/variables, MAJUSCULES pour constantes)
- Indentation à 4 espaces
- Une classe publique par fichier

…mais ne fixe pas la longueur de ligne, l'ordre des membres, ni les règles Javadoc.

## Options envisagées

### Option A — Oracle Java Code Conventions (1997)
- Standard historique d'Oracle (réf. R201).
- ✅ Pour : aligné avec le cours, gratuit, exhaustif.
- ❌ Contre : daté (1997), ligne max 80 caractères trop strict pour Java moderne, non maintenu depuis 25 ans.

### Option B — Google Java Style Guide
- Convention publique de Google : <https://google.github.io/styleguide/javaguide.html>.
- ✅ Pour : moderne (révisé régulièrement), 100 caractères de ligne, profil Eclipse fourni, adopté par Spring/Guava et la majorité des projets open source modernes.
- ❌ Contre : un peu plus permissif que le cours sur certains points (longueur ligne notamment).

### Option C — Style ad-hoc équipe
- Inventer nos propres règles.
- ✅ Pour : taillées au projet.
- ❌ Contre : énergie perdue, biais, pas de profil Eclipse pré-fait, non transférable hors projet.

## Décision

> **Option B — Google Java Style Guide**

Rationale :
- Standard pro le plus répandu en industrie (Spring le suit aussi).
- Profil Eclipse importable directement (pas de configuration manuelle) : <https://github.com/google/styleguide/blob/gh-pages/eclipse-java-google-style.xml>.
- Aligné avec les conventions R201 sur les fondamentaux (CamelCase, indentation, naming) ; étend simplement les règles de longueur et d'ordonnancement.
- Démontre une démarche professionnelle en soutenance.

## Conséquences

### Positives
- Cohérence visuelle entre les 5 contributeurs.
- Revues de MR centrées sur le fond, pas sur le formatage.
- Sortie pro pour le marché du travail.

### Négatives / risques acceptés
- Une légère acclimatation pour les équipiers habitués à un autre style (≤ 1 jour).
- Ligne 100 caractères au lieu de 80 du cours : assumé.

### Suivi
- ☐ Chaque équipier importe le profil Google Java Style dans son Eclipse (cf. `CONTRIBUTING.md` §6).
- ☐ Revue de MR : checklist style à appliquer (cf. `CONTRIBUTING.md` §4.3).

## Références

- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [Spring Framework Code Style](https://github.com/spring-projects/spring-framework/wiki/Code-Style) (suit Google)
- [Profil Eclipse Google Java Style (XML)](https://github.com/google/styleguide/blob/gh-pages/eclipse-java-google-style.xml)
