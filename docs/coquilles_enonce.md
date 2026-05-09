# Coquilles repérées dans les énoncés officiels

> **Statut** : signalées à Mme Pourcelot par mail (cf. `msg_pourcelot.txt` à la racine).
> **Mise à jour** : ce fichier est la source de vérité pour l'équipe ; chaque coquille passera en *résolu* dès qu'on aura le retour.

---

## v0.1 — Structure de base

### C1.1 — `IndexedFile` au lieu de `IndexedPage` dans la sortie attendue
- **Localisation** : page 4 du PDF, exemple de sortie.
- **Texte fautif** : `IndexedFile [url=http://fr.example.org]`
- **Correction présumée** : `IndexedPage [url=http://fr.example.org]` (la classe s'appelle `IndexedPage`).
- **Statut** : ⏳ en attente de réponse Pourcelot.

### C1.2 — `int getNorm()` vs `+ getNorm(): double`
- **Localisation** : page 3 du PDF, description des méthodes (vs page 2 du diagramme UML).
- **Conflit** : le texte dit `int getNorm()`, le diagramme dit `+ getNorm(): double`.
- **Correction présumée** : suivre le diagramme → **`double`** (cohérent avec `Math.sqrt(...)` qui renvoie un `double`).
- **Statut** : ⏳ en attente de réponse Pourcelot.

### C1.3 — `getCount` privée mais utilisée par les tests
- **Localisation** : page 2 du PDF, diagramme UML.
- **Texte fautif** : `- getCount(String word): int` (visibilité privée).
- **Problème** : utilisée depuis `SearchEngineTests`, donc forcément publique en pratique.
- **Correction présumée** : `+ getCount(String word): int` (publique).
- **Statut** : ⏳ en attente de réponse Pourcelot.

### C1.4 — `IndexedPages[]` (avec "s") au lieu de `IndexedPage[]`
- **Localisation** : page 2 du PDF, diagramme UML, classe `SearchEngine`.
- **Texte fautif** : `- pages: IndexedPages[ ]`
- **Correction présumée** : `- pages: IndexedPage[ ]` (singulier, cohérent avec le nom de la classe).
- **Statut** : ⏳ en attente de réponse Pourcelot.
- **Impact code** : par défaut, l'équipe utilise `IndexedPage[]` (pas de classe `IndexedPages` distincte) jusqu'au retour.

### C1.5 (mineur) — `getPonderation(String Word)` avec un W majuscule
- **Localisation** : page 4 du PDF, description.
- **Texte fautif** : `double getPonderation(String Word)` (paramètre `Word`).
- **Correction présumée** : `double getPonderation(String word)` (camelCase cohérent).
- **Statut** : non signalé (cosmétique, sans ambiguïté pour l'implémentation).

---

## v0.2 — Entrées/Sorties

### C2.1 — `IndexPage` au lieu de `IndexedPage`
- **Localisation** : page 2 du PDF, instruction.
- **Texte fautif** : *« Vous devez implémenter le constructeur manquant de la classe **IndexPage** »*
- **Correction présumée** : `IndexedPage`.
- **Statut** : ⏳ en attente de réponse Pourcelot.

### C2.2 — `launch_request()` au lieu de `launchRequest()`
- **Localisation** : page 3 du PDF, description de la classe `SearchEngine`.
- **Texte fautif** : *« sa méthode **launch_request()** »* (snake_case).
- **Conflit** : le diagramme officiel v0.1 dit `launchRequest()` (camelCase).
- **Correction présumée** : suivre le diagramme → **`launchRequest()`**.
- **Statut** : ⏳ en attente de réponse Pourcelot.

### C2.3 — Variable `index` non définie dans le code exemple
- **Localisation** : page 4 du PDF, code exemple pour résoudre le chemin INDEX.
- **Texte fautif** :
  ```java
  Path indexFolder = binFolder.resolve("INDEX");
  // ...
  SearchEngine se = new SearchEngine(index);  // ← `index` n'est jamais défini
  ```
- **Correction présumée** : `new SearchEngine(indexFolder)`.
- **Statut** : ⏳ en attente de réponse Pourcelot.

### C2.4 (mineur) — Fautes d'orthographe
- *« vous verrez **ulétrieurement** en TD »* → ultérieurement
- *« il semble **dificile** d'arriver »* → difficile
- **Statut** : non signalé (sans ambiguïté).

---

## v0.3 — Lemmatisation

### C3.1 (mineur) — Phrase mal construite
- **Localisation** : page 2 du PDF.
- **Texte fautif** : *« Il ne faut donc pas que vous cherchiez à l'améliorer, puisque **vous ce n'est pas vous** qui générez l'indexation »*
- **Sens** : « puisque ce n'est pas vous qui générez l'indexation ».
- **Statut** : non signalé (sans ambiguïté).

---

## v0.4 — Passage à l'échelle

### C4.1 — Titre « Rendu de la version 1.0 »
- **Localisation** : page 2 du PDF, en-tête de la section de rendu.
- **Texte fautif** : *« **Rendu de la version 1.0** »*
- **Correction présumée** : *« Rendu de la version 0.4 »* (toute la section concerne la v0.4).
- **Statut** : ⏳ en attente de réponse Pourcelot.

### C4.2 (mineur) — Tournure inversée
- **Texte fautif** : *« des Hashmap sont **plus bien** adaptées que les tableaux »*
- **Correction présumée** : « bien plus adaptées ».
- **Statut** : non signalé (sans ambiguïté).

---

## v0.5 — Interface web

### C5.1 (mineur) — Répétition « est est »
- **Localisation** : page 2 du PDF.
- **Texte fautif** : *« **L'idée est est** que la commande herve web va lancer un serveur http »*
- **Statut** : non signalé (sans ambiguïté).

### Note importante — divergence CDC/TDL vs PDF officiel
Le PDF officiel v0.5 donne des specs **différentes** de ce qui était initialement dans le CDC :
- Échéance : 5 juin (et non 12 juin)
- Port : 2026 (et non 8080)
- Commande : `herve web --recherche "..."` (et non `./herve serve`)
- Route : `/?recherche=...` (et non `/search?q=...`)
- Rendu : HTML+CSS côté serveur (et non JSON+frontend JS)

Le CDC et la TDL ont été corrigés en conséquence (commit du 2026-05-09).

---

## Convention de mise à jour

Quand une coquille est tranchée par l'enseignante :
1. Remplacer `⏳ en attente de réponse Pourcelot` par `✅ Confirmé : <décision>` ou `❌ Erreur d'interprétation, voir <précision>`.
2. Si nécessaire, mettre à jour le code et/ou le `project-context.md`.
3. Lister la résolution dans la section *Historique* ci-dessous.

## Historique des résolutions

_(vide pour l'instant — à remplir au fur et à mesure des retours)_
