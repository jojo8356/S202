# Coquilles repérées dans les énoncés officiels

> **Statut** : signalées à M. Pourcelot par mail (cf. `msg_pourcelot.txt` à la racine).
> **Mise à jour** : retours reçus le 2026-05-10 23:27 — toutes les coquilles v0.1 et v0.2 sont **confirmées**. Les énoncés locaux (`v0.1_structure_de_base/enonce.txt`, `v0.2_entrees_sorties/enonce.txt`) ont été corrigés en conséquence. M. Pourcelot mettra à jour les pages HTML officielles de son côté.

---

## v0.1 — Structure de base

### C1.1 — `IndexedFile` au lieu de `IndexedPage` dans la sortie attendue
- **Localisation** : page 4 du PDF, exemple de sortie.
- **Texte fautif** : `IndexedFile [url=http://fr.example.org]`
- **Correction** : `IndexedPage [url=http://fr.example.org]` (la classe s'appelle `IndexedPage`).
- **Statut** : ✅ Confirmé par M. Pourcelot (mail 2026-05-10).

### C1.2 — `int getNorm()` vs `+ getNorm(): double`
- **Localisation** : page 3 du PDF, description des méthodes (vs page 2 du diagramme UML).
- **Conflit** : le texte dit `int getNorm()`, le diagramme dit `+ getNorm(): double`.
- **Correction** : suivre le diagramme → **`double`** (cohérent avec `Math.sqrt(...)`).
- **Statut** : ✅ Confirmé par M. Pourcelot (mail 2026-05-10).

### C1.3 — `getCount` privée mais utilisée par les tests
- **Localisation** : page 2 du PDF, diagramme UML.
- **Texte fautif** : `- getCount(String word): int` (visibilité privée).
- **Problème** : utilisée depuis `SearchEngineTests`, donc forcément publique en pratique.
- **Correction** : `+ getCount(String word): int` (publique).
- **Statut** : ✅ Confirmé par M. Pourcelot (mail 2026-05-10).

### C1.4 — `IndexedPages[]` (avec "s") au lieu de `IndexedPage[]`
- **Localisation** : page 2 du PDF, diagramme UML, classe `SearchEngine`.
- **Texte fautif** : `- pages: IndexedPages[ ]`
- **Correction** : `- pages: IndexedPage[ ]` (singulier, cohérent avec le nom de la classe).
- **Statut** : ✅ Confirmé par M. Pourcelot (mail 2026-05-10).

### C1.5 — `indexation_directory` (snake_case) au lieu de `indexationDirectory`
- **Localisation** : page 2 du PDF, diagramme UML, classe `SearchEngine` (attribut + paramètre du constructeur). Apparaît aussi dans le texte de la v0.2.
- **Texte fautif** : `- indexation_directory: Path` et `+ SearchEngine(Path indexation_directory)`.
- **Correction** : `indexationDirectory` (camelCase, conforme aux conventions Java — réflexe Python à oublier ici).
- **Statut** : ✅ Confirmé par M. Pourcelot (mail 2026-05-10) — ajouté à la liste sur sa propre relecture.

### C1.6 (mineur) — `getPonderation(String Word)` avec un W majuscule
- **Localisation** : page 4 du PDF, description.
- **Texte fautif** : `double getPonderation(String Word)` (paramètre `Word`).
- **Correction** : `double getPonderation(String word)` (camelCase cohérent).
- **Statut** : ✅ Corrigé localement (cosmétique, non signalé dans le mail).

---

## v0.2 — Entrées/Sorties

### C2.1 — `IndexPage` au lieu de `IndexedPage`
- **Localisation** : page 2 du PDF, instruction.
- **Texte fautif** : *« Vous devez implémenter le constructeur manquant de la classe **IndexPage** »*
- **Correction** : `IndexedPage`.
- **Statut** : ✅ Corrigé localement (cosmétique, non explicitement listé dans le mail mais sans ambiguïté).

### C2.2 — `launch_request()` au lieu de `launchRequest()`
- **Localisation** : page 3 du PDF, description de la classe `SearchEngine`.
- **Texte fautif** : *« sa méthode **launch_request()** »* (snake_case).
- **Conflit** : le diagramme officiel v0.1 dit `launchRequest()` (camelCase).
- **Correction** : suivre le diagramme → **`launchRequest()`** (camelCase en Java, snake_case en Python — réflexe à oublier ici).
- **Statut** : ✅ Confirmé par M. Pourcelot (mail 2026-05-10).

### C2.3 — Variable `index` non définie dans le code exemple
- **Localisation** : page 4 du PDF, code exemple pour résoudre le chemin INDEX.
- **Texte fautif** :
  ```java
  Path indexFolder = binFolder.resolve("INDEX");
  // ...
  SearchEngine se = new SearchEngine(index);  // ← `index` n'est jamais défini
  ```
- **Correction** : `new SearchEngine(indexFolder)`.
- **Statut** : ✅ Confirmé par M. Pourcelot (mail 2026-05-10).

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
- **Statut** : ⏳ non signalé pour l'instant (à traiter dans un mail séparé si besoin).

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

### 2026-05-10 — Retour de M. Pourcelot (mail à Johan, 23:27)
Toutes les coquilles signalées dans le mail du 2026-05-09 sont confirmées :
- C1.1 (`IndexedFile` → `IndexedPage` dans `toString()`).
- C1.2 (`int getNorm()` → `double getNorm()`, suivre le diagramme).
- C1.3 (`getCount` doit être publique).
- C1.4 (`IndexedPages[]` → `IndexedPage[]`, retirer le « s »).
- C2.2 (`launch_request()` → `launchRequest()`, camelCase en Java).
- C2.3 (`new SearchEngine(index)` → `new SearchEngine(indexFolder)`).

M. Pourcelot a ajouté de lui-même une coquille supplémentaire :
- **C1.5** (`indexation_directory` → `indexationDirectory`), même logique de camelCase que `launchRequest`.

Actions appliquées :
1. Énoncés locaux (`v0.1_structure_de_base/enonce.txt`, `v0.2_entrees_sorties/enonce.txt`) corrigés.
2. `docs/project-context.md`, `docs/cahier_des_charges.md`, `TDL.md` mis à jour pour utiliser `indexationDirectory` et retirer les notes « ignorer la coquille ».
3. Les pages HTML officielles seront mises à jour par M. Pourcelot de son côté.
