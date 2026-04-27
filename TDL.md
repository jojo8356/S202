# TDL — Plan d'exécution du projet HeRVé

> **Source :** `docs/cahier_des_charges.md` (v1.0).
> **Méthode :** Tree of Thoughts — 3 plans candidats → évaluation pondérée → plan retenu détaillé en *babysteps*.

---

## 0. Trois plans candidats

### Plan A — *« Waterfall strict, version par version »*

Une version livrée intégralement avant d'attaquer la suivante. Tag posé, push, on passe à la v0.X+1. Pas de travail parallèle entre versions.

- **Pour :** colle exactement à la grille de notation, traçabilité git parfaite, simple à suivre.
- **Contre :** une équipe de 5 ne peut pas tous coder la même classe en même temps → temps mort. Si v0.1 prend du retard, tout le calendrier glisse.

### Plan B — *« Slicing vertical par équipier »*

Dès le démarrage, chaque membre prend un domaine *transverse à toutes les versions* : un sur l'I/O et la persistance, un sur le NLP (lemmatisation/filtrage), un sur la perf, un sur l'UI web, un sur les tests.

- **Pour :** maximise le débit, chacun monte en compétence sur son axe.
- **Contre :** très risqué pour une équipe étudiante — il faut figer les interfaces dès J0, sinon merges infernaux. Le rendu *par version* est compliqué à découper.

### Plan C — *« Spiral / risk‑driven »*

On identifie les 3 risques techniques critiques (passage à 38 000 pages, cohérence lemmatisation index/requête, intégration web ↔ Java) et on bâtit un *vertical slice* minimal qui les couvre dès la semaine 1, *avant* de retravailler proprement v0.1 → v0.5.

- **Pour :** surface les vrais blocages au plus tôt.
- **Contre :** dévie du schéma de notation par version. Risque qu'à la fin il manque la propreté de chaque livrable intermédiaire.

---

## 1. Grille d'évaluation

| Critère | Poids | Plan A | Plan B | Plan C |
| --- | :---: | :---: | :---: | :---: |
| Conformité à la notation par version | 25 % | **5/5** | 2/5 | 1/5 |
| Parallélisme équipe (5 pers.) | 20 % | 2/5 | **5/5** | 4/5 |
| Robustesse aux retards | 15 % | 2/5 | 3/5 | **5/5** |
| Simplicité de coordination | 15 % | **5/5** | 2/5 | 3/5 |
| Couverture des risques techniques | 10 % | 2/5 | 3/5 | **5/5** |
| Qualité du tagging git | 10 % | **5/5** | 3/5 | 2/5 |
| Charge cognitive du chef de projet | 5 % | **4/5** | 2/5 | 2/5 |
| **Total pondéré** | 100 % | **3,55** | 3,05 | 3,15 |

## 2. Plan retenu — *Hybride A + B*

> **Stratégie :** sprint *par version* (squelette du Plan A — la notation l'impose), mais à l'intérieur de chaque sprint on **parallélise** entre équipiers (graine du Plan B). Un sprint = un tag = un push. Trois rôles tournants : `[D]` *dev*, `[T]` *testeur*, `[R]` *reviewer*. Le chef de projet `[CP]` est *coordinateur*, pas codeur.

Conventions :

- ☐ = case à cocher au fur et à mesure.
- `[CP]` `[D1]` `[D2]` `[D3]` `[D4]` = équipier responsable suggéré.
- `t≈` = estimation *individuelle* en heures.
- 🔗 = dépendance bloquante.
- 🏁 = critère d'acceptation vérifiable.

---

## Sprint 0 — Préparation · S18 · ⇒ 30 avril 2026

> Constitution équipe + outillage. À ce stade, les TP Python individuels sont déjà rendus.

### S0.1 Constitution de l'équipe `[CP]` · t≈ 1 h
- ☐ Choisir 4 coéquipiers.
- ☐ Désigner le chef de projet (en gras dans le doc d'inscription).
- ☐ S'inscrire dans le document collectif d'inscription.
  🏁 Le binôme/quintet apparaît avec **CP en gras** dans le tableau partagé.

### S0.2 Mise en place GitLab IUT `[CP]` · t≈ 1 h
- ☐ Créer le sous‑groupe sur `iut-git.unice.fr/s201-25-26/<groupe>` (PAS un sous‑sous‑groupe).
- ☐ **Fork** du dépôt template `s201-25-26/herve` dans le sous‑groupe — *sans renommer* le projet.
- ☐ Vérifier que le rôle CP est `Maintainer`. Sinon, mailer l'enseignant.
- ☐ Inviter les 4 coéquipiers en `Developer`.
- ☐ Cloner localement (HTTPS pour les démarrages, SSH une fois la clé en place).
  🏁 `git clone … && ./compile_projet && ./herve` exécute sans erreur sur la machine de chacun.

### S0.3 Discipline git documentée `[CP]` · t≈ 30 min
- ☐ Ajouter `CONTRIBUTING.md` à la racine : règles de branche `v0.X`, tag `v0.X`, format de message.
- ☐ Activer la *protection* de la branche `main` côté GitLab (push direct interdit, MR obligatoire).
  🏁 Une MR de test est exigée pour merger.

### S0.4 Lecture commune du cahier des charges `[CP]` + tous · t≈ 1 h
- ☐ Tout le monde lit `docs/cahier_des_charges.md`, surligne ses questions.
- ☐ Réunion de 30 min : tour de table, lever toutes les ambiguïtés.
  🏁 Aucune question ouverte avant le démarrage de v0.1.

---

## Sprint 1 — v0.1 · Structure de base · ⇒ 15 mai 2026

> Cible : `IndexedPage` complète + `SearchEngineTests` couvrant méthodes/constructeurs.

### S1.1 Branche `v0.1` `[CP]` · t≈ 5 min
- ☐ `git checkout -b v0.1` sur le dépôt principal.
- ☐ `git push -u origin v0.1`.
  🏁 `git branch -vv` affiche `v0.1` trackée.

### S1.2 Squelette des packages `[D1]` · t≈ 30 min · 🔗 S1.1
- ☐ Créer `src/search_engine/` et `src/search_engine_tests/`.
- ☐ Créer 3 fichiers vides : `IndexedPage.java`, `SearchEngine.java`, `SearchResult.java`.
- ☐ Créer `SearchEngineTests.java` avec un `main` vide.
- ☐ `./compile_projet` doit toujours passer (classes vides compilent).
  🏁 `bin/search_engine/IndexedPage.class` existe après compilation.

### S1.3 Attributs et constructeur `IndexedPage(String[] lines)` `[D1]` · t≈ 1 h · 🔗 S1.2
- ☐ Déclarer `private String url`, `private String[] words`, `private int[] counts`.
- ☐ Constructeur : `lines[0]` → `url`. Pour chaque ligne suivante, split sur `':'`, alimenter `words` et `counts`.
- ☐ Gérer le cas où `lines` est vide (pas de ligne URL) → `IllegalArgumentException`.
  🏁 `new IndexedPage(new String[]{"http://x", "a:1"})` ne lève pas d'exception et stocke `["a"]`, `[1]`.

### S1.4 Constructeur `IndexedPage(String text)` `[D1]` · t≈ 45 min · 🔗 S1.3
- ☐ Split par `text.split("\\s+")`.
- ☐ Compter chaque mot distinct, trier alphabétiquement.
- ☐ `url` reste `null` (ou chaîne vide), c'est une *requête*.
  🏁 `new IndexedPage("hello world hello")` produit `words={hello, world}`, `counts={2,1}`.

### S1.5 Méthodes simples `[D2]` · t≈ 1 h · 🔗 S1.3
- ☐ `String getUrl()`, retourne l'URL.
- ☐ `int getCount(String word)`, recherche linéaire dans `words`, renvoie `0` si absent.
- ☐ `String toString()` : `"IndexedPage [url=" + url + "]"`.
  🏁 `page.toString()` retourne exactement la forme attendue par l'énoncé.

### S1.6 Méthodes mathématiques `[D2]` · t≈ 1 h 30 · 🔗 S1.5
- ☐ `getNorm()` : `Math.sqrt(somme des counts²)`.
- ☐ `getPonderation(String word)` : `getCount(word) / getNorm()` (`0` si norme nulle).
- ☐ `proximity(IndexedPage other)` : somme du produit des `getPonderation()` sur les mots communs.
  🏁 Sur l'exemple de l'énoncé (page1 hello:10 world:5 / page2 hello:5 ...) le score vaut `0.8304547985373998`.

### S1.7 Tests `SearchEngineTests` `[D3]` · t≈ 2 h · 🔗 S1.6
- ☐ Test 1 : reproduire l'exemple littéral du PDF, comparer la sortie attendue ligne à ligne.
- ☐ Test 2 : page vide (URL seule) → `getNorm() == 0`, `getPonderation("anything") == 0`.
- ☐ Test 3 : `getCount` sur un mot absent → `0`.
- ☐ Test 4 : `proximity` symétrique : `a.proximity(b) == b.proximity(a)`.
- ☐ Test 5 : `proximity(self) == 1` à 1e‑10 près (un document est colinéaire avec lui‑même).
  🏁 `./herve` lance le main de tests et imprime `OK` 5 fois.

### S1.8 Code review croisée `[R = D4]` · t≈ 1 h · 🔗 S1.7
- ☐ Ouvrir une MR `v0.1` → relue par `D4`.
- ☐ Vérifier indentation, javadoc minimale (1 phrase par méthode publique), pas de `printf` oublié.
- ☐ Approuver et merger dans `v0.1`.

### S1.9 Tag, push, livraison `[CP]` · t≈ 15 min · 🔗 S1.8
- ☐ `git tag v0.1 -m "version 0.1"` sur le commit final.
- ☐ `git push origin v0.1 --tags`.
- ☐ Vérifier `compile_projet` et `herve` toujours fonctionnels.
- ☐ Cocher la case rendu sur Moodle (si formulaire associé).
  🏁 La page GitLab affiche le tag `v0.1` daté avant 15 mai 20:00.

---

## Sprint 2 — v0.2 · Entrées/Sorties · ⇒ 22 mai 2026

> Cible : moteur fonctionnel sur 100 pages, CLI one‑shot + interactif.

### S2.1 Branche `v0.2` `[CP]` · t≈ 5 min · 🔗 v0.1
- ☐ `git checkout -b v0.2` depuis le tag `v0.1`.
- ☐ `git push -u origin v0.2`.

### S2.2 Constructeur `IndexedPage(Path path)` `[D1]` · t≈ 1 h · 🔗 S2.1
- ☐ Ajouter `throws IOException` à la signature.
- ☐ Lire toutes les lignes via `Files.readAllLines(path, StandardCharsets.UTF_8)`.
- ☐ Réutiliser le constructeur `IndexedPage(String[] lines)` (`new IndexedPage(lines.toArray(new String[0]))` ou refactor en helper).
  🏁 Sur un fichier d'index local (test fixture), l'objet créé contient bien l'URL et les couples mot/occurrence.

### S2.3 Classe `SearchResult` `[D2]` · t≈ 30 min · indépendant
- ☐ Attributs `private String url`, `private double score`.
- ☐ Constructeur, getters.
- ☐ `toString()` : `"SearchResult [url=" + url + ", score=" + score + "]"`.
  🏁 Test unitaire : `new SearchResult("u", 0.5).toString()` → forme exacte.

### S2.4 Constructeur `SearchEngine(Path)` `[D2]` · t≈ 2 h · 🔗 S2.2
- ☐ `Files.list(indexation_directory)` → flux des fichiers.
- ☐ Pour chaque fichier, instancier `IndexedPage(path)`.
- ☐ Stocker dans `IndexedPage[] pages`.
- ☐ Ajouter `throws IOException` à la signature du constructeur.
  🏁 `new SearchEngine(Paths.get("bin/INDEX")).getPagesNumber() == 100` sur le mini‑corpus.

### S2.5 Méthodes `getPage`, `getPagesNumber` `[D2]` · t≈ 15 min · 🔗 S2.4
- ☐ Implémentation triviale.
  🏁 Tests OK.

### S2.6 `launchRequest` + `printResults` `[D3]` · t≈ 2 h · 🔗 S2.4 + S2.3
- ☐ `launchRequest(String)` : crée un `IndexedPage(requestString)`, calcule la similarité avec chaque page, trie décroissant, renvoie `SearchResult[]`.
- ☐ `printResults` : appelle `launchRequest`, affiche les **15 premiers** dont `score > 0`, format exact `SearchResult [url=..., score=...]`.
  🏁 Sur la requête `cerise flan`, la première ligne est `Flan, score=37.71273413657018`.

### S2.7 Résolution INDEX classpath‑safe `[D1]` · t≈ 30 min · 🔗 S2.6
- ☐ Recopier le snippet du CDC (`SearchEngine.class.getProtectionDomain()...`).
  🏁 Le moteur tourne aussi bien depuis Eclipse que `java -cp bin search_engine.SearchEngine`.

### S2.8 Méthode `main` (one‑shot + interactif) `[D3]` · t≈ 1 h · 🔗 S2.6
- ☐ Si `args.length > 0` : concaténer `String.join(" ", args)` → `printResults` → exit.
- ☐ Sinon : boucle `Scanner(System.in)`. Saisie `exit` → break. Sinon `printResults`, on reboucle.
  🏁 `./herve flan cerise` retourne 3 lignes ; `./herve` ouvre l'invite et accepte 3 requêtes consécutives puis `exit`.

### S2.9 Tests v0.2 `[D4]` · t≈ 1 h 30 · 🔗 S2.8
- ☐ Compléter `SearchEngineTests` : nouveau test couvrant `Path`, `launchRequest`, `printResults`.
- ☐ Test du chemin one‑shot via `main(new String[]{"cerise","flan"})` (capture stdout).
  🏁 Tous les tests passent.

### S2.10 Code review + tag `[CP]` · t≈ 30 min · 🔗 S2.9
- ☐ MR mergée dans `v0.2`.
- ☐ Tag `v0.2` posé, push avec `--tags`.
  🏁 Tag visible sur GitLab avant **22 mai 20:00**.

---

## Sprint 3 — v0.3 · Lemmatisation · ⇒ 26 mai 2026

> *Vous n'êtes plus guidés.* Choix techniques à documenter dans `doc/decisions_v0.3.md` à mesure.

### S3.1 Branche `v0.3` `[CP]` · t≈ 5 min · 🔗 v0.2

### S3.2 Chargement du dictionnaire `[D1]` · t≈ 1 h
- ☐ Copier `french_dictionary.txt` dans `bin/` (et `src/` pour Eclipse).
- ☐ Créer `Lemmatizer.java` avec `private final HashMap<String, String> dico`.
- ☐ Constructeur : lit chaque ligne `mot:lemme`, ajoute à la map. ⚠️ UTF‑8 explicite.
  🏁 `new Lemmatizer().lemmatize("pommes")` retourne `"pomme"`.

### S3.3 Chargement de la blacklist `[D1]` · t≈ 30 min · 🔗 S3.2
- ☐ Copier `blacklist.txt` dans `bin/`.
- ☐ Charger en `Set<String>` (HashSet, recherche O(1)).
  🏁 `blacklist.contains("de") == true`.

### S3.4 Pipeline de prétraitement requête `[D2]` · t≈ 1 h 30 · 🔗 S3.2 + S3.3
- ☐ Méthode `String[] preprocess(String requete)` qui : `toLowerCase` (Locale FR) → split sur regex `[^\\p{L}]+` → lemmatize → filtre blacklist → filtre `length() < 2`.
- ☐ Retourne le tableau de mots prétraités.
  🏁 `preprocess("Les pommes ! De ?? terre")` → `{"pomme", "terre"}`.

### S3.5 Intégration dans `IndexedPage(String)` `[D2]` · t≈ 30 min · 🔗 S3.4
- ☐ Le constructeur de requête utilise `preprocess` au lieu de `split` brut.
  🏁 `new IndexedPage("les fruits")` est équivalent à `new IndexedPage("fruit")`.

### S3.6 Décisions documentées `[CP]` · t≈ 30 min · 🔗 S3.4
- ☐ Créer `doc/decisions_v0.3.md` :
  - choix de la regex de split,
  - seuil de longueur minimale,
  - traitement des mots inconnus du dictionnaire (gardés en forme de surface),
  - performance Lemmatizer (chargement unique au démarrage de SearchEngine).
  🏁 Document signé par tous les équipiers en commentaire de MR.

### S3.7 Tests v0.3 `[D3]` · t≈ 1 h 30 · 🔗 S3.5
- ☐ Test : `pommes` ≡ `pomme`.
- ☐ Test : ponctuation et chiffres ignorés.
- ☐ Test : stopwords retirés.
- ☐ Test : majuscules normalisées (`PoMmE` ≡ `pomme`).
- ☐ Test : mot inconnu (un nom propre par ex.) → conservé tel quel.
  🏁 100 % des nouveaux tests passent.

### S3.8 Code review + tag v0.3 `[CP]` · t≈ 30 min
- ☐ MR mergée.
- ☐ Tag `v0.3` avant **26 mai 20:00**.

---

## Sprint 4 — v0.4 · Passage à l'échelle · ⇒ 29 mai 2026

> Objectif KPI : ≤ **200 ms / requête** sur 38 000 pages.

### S4.1 Branche `v0.4` + import du gros corpus `[CP]` · t≈ 30 min · 🔗 v0.3
- ☐ Décompresser `INDEX_FILES.7z` dans `bin/INDEX/` (sans le commiter — `.gitignore`).
- ☐ Documenter l'emplacement attendu dans `README.md`.

### S4.2 Migration `String[] words / int[] counts` → `HashMap<String,Integer>` `[D1]` · t≈ 3 h · 🔗 S4.1
- ☐ Refactor `IndexedPage` : remplacer les deux tableaux par `Map<String,Integer> termFreq`.
- ☐ Pré‑calculer la norme à la construction (`this.norm = sqrt(sum(c² for c in termFreq.values()))`).
- ☐ Adapter `getCount`, `getPonderation`, `proximity` (itère sur la *plus petite* map → micro‑optim).
- ☐ ⚠️ **Préserver les signatures publiques** déjà testées en v0.1 / v0.2.
  🏁 Tous les tests v0.1 / v0.2 / v0.3 passent **sans modification**.

### S4.3 Chargement parallèle des fichiers `[D2]` · t≈ 2 h · 🔗 S4.2
- ☐ Utiliser `Files.list(...).parallel().map(IndexedPage::new).collect(...)` pour exploiter les cœurs.
- ☐ Mesurer : `System.nanoTime()` autour du constructeur.
  🏁 Sur 38 k pages, le temps d'indexation initial est < 60 s.

### S4.4 Bench séquence vs parallèle vs deux structures `[D3]` · t≈ 3 h · 🔗 S4.3
- ☐ Écrire `Benchmark.java` qui mesure l'indexation + 100 requêtes types sur **100 / 1 000 / 10 000 / 38 000** pages, pour `Array` et `HashMap`.
- ☐ Sortie : table CSV → `doc/bench_v0.4.csv`.
- ☐ Plot rapide (Excel ou Python externe) → `doc/bench_v0.4.png`.
  🏁 Le tableau du CDC §5.4 est rempli avec des chiffres réels.

### S4.5 Profilage mémoire `[D4]` · t≈ 1 h 30 · 🔗 S4.4
- ☐ `Runtime.getRuntime().totalMemory() - freeMemory()` après chargement complet.
- ☐ Si > 1 Go : tenter `String.intern()` sur les mots du vocabulaire.
  🏁 RAM résidente ≤ 1 Go sur 38 k pages.

### S4.6 Tests v0.4 `[D3]` · t≈ 1 h
- ☐ Test « non‑régression » : sur 100 pages, le résultat de `cerise flan` est **identique** à v0.2 (mêmes scores).
- ☐ Test perf : assertion `temps_moyen_par_requete < 200 ms` sur 38 k pages.

### S4.7 Code review + tag v0.4 `[CP]` · t≈ 30 min
- ☐ MR mergée, tag `v0.4` avant **29 mai 20:00**.

---

## Sprint 5 — v0.5 · Interface web · ⇒ 12 juin 2026

> Travail parallèle avec Sprint 6 si possible (équipe scindée).

### S5.1 Branche `v0.5` `[CP]` · t≈ 5 min · 🔗 v0.4

### S5.2 Serveur HTTP minimal `[D2]` · t≈ 2 h
- ☐ Créer `WebServer.java` qui utilise `com.sun.net.httpserver.HttpServer.create(addr, 0)`.
- ☐ Routes : `GET /` (sert `index.html`), `GET /search?q=...` (sert le JSON).
- ☐ Executor : `Executors.newFixedThreadPool(4)`.
- ☐ Démarrage via `./herve serve` (mettre à jour le script).
  🏁 `curl http://localhost:8080/search?q=flan` renvoie un JSON 200 OK.

### S5.3 Sérialisation JSON sans dépendance `[D2]` · t≈ 1 h · 🔗 S5.2
- ☐ Helper `toJson(SearchResult[] results)` — concat de `String`, échappement basique des `"` et `\\`.
- ☐ `Content-Type: application/json; charset=utf-8`.
  🏁 `JSON.parse(...)` côté navigateur fonctionne sans erreur.

### S5.4 Frontend statique `[D3]` · t≈ 3 h
- ☐ `web/index.html` : un `<input type="search">`, un `<button>`, un `<ul>` pour les résultats.
- ☐ `web/style.css` : minimaliste type GitHub, fond blanc, max‑width 720 px.
- ☐ `web/app.js` : `fetch('/search?q=' + encodeURIComponent(...))` → render.
- ☐ Affichage du temps de réponse côté serveur (header `X-Search-Time-Ms`).
  🏁 Démo manuelle : la page tape *flan*, 3 résultats apparaissent en < 300 ms.

### S5.5 Servir les fichiers statiques depuis le serveur Java `[D4]` · t≈ 1 h · 🔗 S5.2 + S5.4
- ☐ Une route catch‑all qui mappe les fichiers du dossier `web/` (mime type basique : html/css/js).
  🏁 `http://localhost:8080/` charge la page sans erreur 404 sur les assets.

### S5.6 Tests d'intégration `[D4]` · t≈ 1 h 30
- ☐ Test : démarrer le serveur, faire 5 requêtes via `HttpClient`, vérifier les 200 OK.
- ☐ Test : `q` manquant → 400.
- ☐ Test : utf‑8 dans la requête (`café`) → réponse correcte.

### S5.7 Code review + tag v0.5 `[CP]` · t≈ 30 min
- ☐ Tag `v0.5` avant **12 juin 20:00**.

---

## Sprint 6 — Rendu final créatif · ⇒ 12 juin 2026

> **Choix d'une seule piste** parmi A / B / C ci‑dessous, à valider avec l'enseignant **avant le 5 juin** si on diverge des suggestions du CDC.

### S6.0 Choix de la piste `[CP] + équipe` · t≈ 1 h · 🔗 v0.5
- ☐ Réunion : voter A (indexation à froid), B (autocorrection) ou C (recherche littérale).
- ☐ Mailer l'enseignant si proposition perso.
  🏁 Décision actée dans `doc/decisions_finales.md`.

### S6.A — Si « Indexation à froid » `[D1+D2]` · t≈ 12 h
- ☐ S6.A.1 — `Crawler.java` : `HttpClient.newHttpClient()`, parser regex liens, file BFS, `visited Set`.
- ☐ S6.A.2 — Politesse : 1 s entre 2 requêtes même hôte, header `User-Agent: HeRVe/1.0 (educational)`.
- ☐ S6.A.3 — Extraction texte : `replaceAll("<[^>]+>", " ")` + nettoyage entités HTML.
- ☐ S6.A.4 — Lemmatisation locale (réutilise Lemmatizer de v0.3).
- ☐ S6.A.5 — Génération de fichiers d'index identiques au format v0.2.
- ☐ S6.A.6 — Reprise après interruption : journal d'URLs visitées sur disque.
- ☐ S6.A.7 — Test : indexer 50 pages d'un site jouet (un petit blog), relancer la recherche dessus.

### S6.B — Si « Autocorrection » `[D3+D4]` · t≈ 8 h
- ☐ S6.B.1 — Construire un index n‑gram (n=2) du vocabulaire.
- ☐ S6.B.2 — Pré‑sélection Jaccard : top 50 candidats par similarité de bigrammes.
- ☐ S6.B.3 — Levenshtein DP sur ces 50, garder le meilleur si distance ≤ 2.
- ☐ S6.B.4 — Si correction appliquée, l'afficher en bandeau (« recherche suggérée : *X* »).
- ☐ S6.B.5 — Tests : `pomes` → `pomme` ; `cerice` → `cerise`.

### S6.C — Si « Recherche littérale `"…"` » `[D2+D3]` · t≈ 6 h
- ☐ S6.C.1 — Décompresser `contenus_textuels_bruts.7z` dans `bin/CONTENT/`.
- ☐ S6.C.2 — Parser de requête : extraire les fragments entre `"…"` et le reste.
- ☐ S6.C.3 — Phase 1 : recherche vectorielle classique sur l'union des mots.
- ☐ S6.C.4 — Phase 2 : sur le top 50, charger le fichier de contenu brut, vérifier `String.contains(fragment)` (insensible casse).
- ☐ S6.C.5 — Re‑classement final : seules les pages passant phase 2 sont retenues.
- ☐ S6.C.6 — Tests : `"pommes de terre" gâteau` retourne le bon document.

### S6.X Restitution `[CP] + équipe` · t≈ 4 h
- ☐ Rédiger `doc/rapport_final.md` : démarche, choix, résultats, échecs et apprentissages.
- ☐ Préparer 8 slides pour la soutenance.
- ☐ Rehearsal interne : chaque membre présente *une* partie.

### S6.Y Tag final `[CP]` · t≈ 15 min
- ☐ Branche `final` (ou continuer sur `v0.5`).
- ☐ Tag `final` ou `v1.0`. Push avec `--tags`.
  🏁 La page GitLab affiche le tag final avant **12 juin 20:00**.

---

## Sprint 7 — Soutenance · S25 · 4 h hors passage

### S7.1 Préparation démo `[équipe]` · t≈ 2 h
- ☐ Reset machine : `compile_projet`, `herve` testés sur clé USB ou laptop équipe.
- ☐ Plan B : capture vidéo de la démo en local *au cas où* le projecteur fait défaut.

### S7.2 Répartition des points `[CP] + équipe` · t≈ 1 h
- ☐ Réunion : chacun s'auto‑évalue, le CP arbitre, on signe la grille.
  🏁 Grille signée remise à l'enseignant.

---

## Annexe — Cartographie de la charge équipe

| Équipier | Rôle dominant | Charge totale estimée |
| --- | --- | :---: |
| **CP** | coordination, MR, tags, doc | ~12 h |
| D1 | I/O, persistance, classpath | ~14 h |
| D2 | classes cœur, web server | ~14 h |
| D3 | algos avancés, NLP | ~14 h |
| D4 | tests, perf, review | ~12 h |

> Ces chiffres sont **par équipier** sur la durée totale du projet (S18 → S25). Comparer aux 44 h prévues dans la grille horaire officielle pour valider la cohérence.

## Annexe — Risques et plans de contingence

| Risque | Probabilité | Mitigation prévue |
| --- | :---: | --- |
| Tag mal nommé → rendu non détecté | M | check‑list S1.9, S2.10, …, vérification `git tag -l` avant push |
| OOM sur 38 k pages | F | profilage S4.5 dès 1 000 pages |
| Modification accidentelle de `compile_projet`/`herve` | F | branche `main` protégée + revue MR |
| Membre absent | M | binôme tournant sur chaque sprint, doc à jour pour reprise |
| Crawler banni en piste A | F | délai 1 s + backoff exponentiel sur 429 |

---

*Plan exécutable. Cocher au fur et à mesure ; tenir à jour ce fichier dans la branche `main` (commits par sprint).*
