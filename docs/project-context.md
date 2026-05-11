---
project_name: 'HeRVé — Moteur de recherche vectoriel'
user_name: 'Johan'
date: '2026-05-09'
status: 'complete'
sections_completed:
  - technology_stack
  - language_specific
  - project_specific
  - testing
  - code_style
  - workflow_git
  - critical_dont_miss
optimized_for_llm: true
---

# Project Context for AI Agents

_Ce fichier rassemble les règles et patterns critiques que les agents IA doivent respecter pour implémenter du code dans HeRVé. Il met l'accent sur les détails non évidents qu'un agent risquerait d'ignorer._

> **Source de vérité** : les PDF officiels Moodle des versions v0.1 → v0.5 priment sur le CDC interne en cas de conflit. Le CDC et la TDL sont des synthèses, pas l'énoncé officiel.

---

## Technology Stack & Versions

### Versions imposées (énoncés officiels)

| Élément | Choix | Source |
| --- | --- | --- |
| Langage | **Java 17 (OpenJDK)** | imposé par le CDC |
| Dépendances | **aucune hors JDK** | imposé — pas de Maven/Gradle, pas de Jackson/Gson/jsoup/jericho, **pas de JUnit** (tests via `main` qui imprime `OK`) |
| Plateforme cible | **Linux Debian 12** | imposé pour évaluation |
| Build | scripts shell `compile_projet` & `herve` | **NE PAS MODIFIER** (revue MR systématique sur ces fichiers) |
| Encodage | **UTF-8 strict**, EOL `\n` (UNIX) | énoncé v0.2 explicite |
| IDE de référence | Eclipse | autorisé : autres IDE *si* arborescence `src/`/`bin/` respectée |
| Port serveur web (v0.5) | **2026** (et non 8080) | énoncé v0.5 : *« afin que tous les groupes utilisent le même port »* |

### APIs JDK couvertes en cours R201 (utilisation libre)

`java.util.*` → HashMap, HashSet, ArrayList, LinkedList, Scanner, Iterator, Comparable, Arrays
`java.io.*` → File, BufferedReader/Writer, FileReader/Writer, FileInputStream/OutputStream
`java.lang.*` → String, Math, System, Object, exceptions standards
généricité `<T>`, interfaces, classes abstraites, héritage, polymorphisme, `instanceof`.

### APIs JDK imposées par les énoncés mais hors programme R201 (autodidacte)

- **`java.nio.file.Path` + `Files.readAllLines`** — signature `IndexedPage(Path path)` imposée v0.2. Officiellement autorisée par l'enseignante (énoncé v0.2 : *« vous pouvez pour l'instant vous contenter d'utiliser `Files.readAllLines()` … vous verrez ultérieurement en TD d'autres méthodes »*).
- **`com.sun.net.httpserver.HttpServer`** — v0.5 (port 2026). Référence : <https://blog.ronanlefichant.fr/2019/05/java-http-server.html> (avec correctif UTF-8).
- **`java.net.http.HttpClient`** (JDK 11+) — Sprint 6 piste A (indexation à froid) uniquement.
- **`java.util.concurrent.Executors.newFixedThreadPool`** — v0.5 (concurrence basique).
- **`java.util.regex` + `Pattern`/`Matcher`** — v0.3 (regex `[^\\p{L}]+` pour split).

### Constructions à éviter (hors programme R201 et non requises)

`var` (Java 10), records, sealed classes, pattern matching (switch arrows), lambdas, méthode-références, Streams API non triviaux (`.stream()`, `.map()`, `.filter()`, `.collect()`), `Optional`, `try-with-resources` (préférer `try/finally + close()` comme vu en cours).

### Référence algorithmique (Python, hors rendu)

Le code Python du TP préparatoire dans `tp_preparatoire/td3_modele_vectoriel/` (`librairie.py`, `moteur_de_recherche.py`, `verifier_calculs.py`) sert de **référence numérique** pour valider les calculs (cosinus, TF-IDF). **Non versionné dans le rendu Java**.

## Critical Implementation Rules

### Règles Java (calibrées sur R201 + énoncés officiels)

#### Conventions de nommage
- **Packages** : `lower_case_avec_underscores` — imposé par les énoncés (`search_engine`, `search_engine_tests`).
- **Classes** : `PascalCase` (ex. `IndexedPage`, `SearchEngine`).
- **Méthodes / variables** : `camelCase` (ex. `getCount`, `launchRequest`).
- **Constantes** : `MAJUSCULES_AVEC_UNDERSCORES` (ex. `TAILLE_MAX`).
- **`launchRequest()`** est en camelCase (énoncé v0.1 — l'énoncé v0.2 contenait une coquille `launch_request()` ; confirmée et corrigée le 2026-05-10, cf. `coquilles_enonce.md` C2.2).

#### Visibilité & encapsulation
- Tous les attributs **`private`** (énoncé v0.1 explicite : `- url: String`, `- words: String[]`, etc.).
- Pas d'attributs `public` sauf constantes `public static final`.
- Getters/setters publics quand l'accès externe est requis.
- **Signatures publiques GELÉES** dès qu'une version les valide — l'optimisation v0.4 se fait *derrière* l'interface (énoncé v0.4 textuel : *« la signature de vos méthodes publiques reste la même »*).

#### Object & redéfinitions
- `toString()` au format strict imposé : `"IndexedPage [url=...]"` et `"SearchResult [url=..., score=...]"` (énoncé v0.1).
- `@Override` à chaque redéfinition (vu en cours, vérification compilateur).
- Si on redéfinit `equals`, on respecte les contrats : symétrie, réflexivité, transitivité, `a.equals(null) == false` (vu en cours).
- Comparaison de `String` : **toujours `.equals()`**, jamais `==` (vu en cours).

#### Types & flottants
- **Comparaison de doubles** : jamais `==`, toujours via un epsilon. **Tolérance projet : `1e-10`** (CDC + énoncé v0.1 : sortie `0.8304547985373998` à respecter à 10⁻¹⁰ près).
  ```java
  private static final double EPSILON = 1e-10;
  if (Math.abs(a - b) < EPSILON) { ... }
  ```
- Préférer **types primitifs** (`int`, `double`) dans les calculs ; **Wrappers** (`Integer`, `Double`) uniquement dans les collections génériques (cours R201 explicite).
- `getNorm()` retourne **`double`** (suivre le diagramme officiel v0.1 ; coquille `int getNorm()` du texte confirmée et corrigée le 2026-05-10, cf. `coquilles_enonce.md` C1.2).

#### Locale & accents
- **Toujours** utiliser `Locale.FRANCE` explicite avec `toLowerCase()` pour gérer correctement les accents français (« ÉTÉ » → « été ») :
  ```java
  s.toLowerCase(Locale.FRANCE)  // ✅
  s.toLowerCase()               // ❌ dépend de la locale système
  ```
- Idem pour `toUpperCase` si besoin.

#### Collections (cours R201)
- Toujours typer les génériques : `HashMap<String, Integer>`, jamais `HashMap` brut.
- Pour la perf v0.4 : `HashMap<String, Integer>` à la place de `String[] words / int[] counts` (recommandation explicite énoncé v0.4).
- **Blacklist v0.3** : `HashSet<String>` (recherche O(1)), jamais `String[]` ni `ArrayList<String>` (O(n) sur `.contains()`).
- Itération : `for (T x : collection)` (for-each vu en cours) — pas de Streams.

#### Tableaux (cours R201)
- `array.length` (attribut, pas méthode).
- Tri : `Arrays.sort(tableau)` (énoncé v0.1 explicite : *« vous pouvez utiliser ... `Arrays.sort(Object[] a)` »*).
- Découpe de chaîne : `String.split(String regex)` (énoncé v0.1 explicite).

#### Exceptions (cours R201 + énoncé v0.2)
- Propagation préférée à l'absorption silencieuse : `throws IOException` plutôt que `catch (IOException e) { /* vide */ }`.
- v0.2 : énoncé indique explicitement d'ajouter `throws IOException` aux constructeurs `IndexedPage(Path)` et `SearchEngine(Path)` (Eclipse le propose).
- Exceptions custom : héritent de `java.lang.Exception` (cours R201).

#### I/O fichiers — **try-with-resources** (Java 7+)
- Pour toute ouverture de fichier, utiliser `try-with-resources` : la fermeture est garantie même en cas d'exception, et le code est plus court.
  ```java
  try (BufferedReader reader = new BufferedReader(
          new FileReader(path.toFile()))) {
      String line;
      while ((line = reader.readLine()) != null) {
          // traiter line
      }
  }
  // close() appelé automatiquement, même si exception
  ```
- Pour les **petits fichiers** (index v0.2, dictionnaire v0.3) : `Files.readAllLines(path, StandardCharsets.UTF_8)` officiellement autorisé par l'énoncé v0.2 (pas besoin de try-with-resources, l'API gère la fermeture).
- Pour le **gros corpus** (38 000 pages v0.4) : `BufferedReader` en streaming (vu en cours), plus efficace que `readAllLines` qui charge tout en RAM.
- **Toujours UTF-8 explicite** : `StandardCharsets.UTF_8` ou `"UTF-8"`, jamais le charset par défaut (dépend de l'OS).

#### `final` (cours R201)
- Constantes : `private static final int TAILLE_MAX = 100;`
- Attributs immuables après construction : `private final HashMap<String, String> dico;`
- Pas de `final` sur les paramètres de méthode (overkill ici).

### Règles spécifiques HeRVé (issues des PDF officiels)

#### Format des fichiers d'index (énoncé v0.2)
- Ligne 1 : URL canonique de la page (ex. `https://fr.vikidia.org/wiki/Tarte`).
- Lignes 2..n : `<lemme>:<entier>` — exactement un `:`, pas d'espace, pas de quote.
- Encodage **UTF-8**, fin de ligne **`\n`** (UNIX).
- Mots déjà lemmatisés à l'indexation — la requête doit appliquer la même lemmatisation pour matcher.

#### Diagramme de classes officiel (énoncé v0.1) — source de vérité
- `IndexedPage` : 3 attributs privés (`url: String`, `words: String[]`, `counts: int[]`), 3 constructeurs publics (`String[] lines`, `Path path`, `String text`), 6 méthodes publiques.
- `SearchEngine` : 2 attributs privés (`indexationDirectory: Path`, `pages: IndexedPage[]`), constructeur, 4 méthodes publiques.
- `SearchResult` : 2 attributs privés (`url: String`, `score: double`), constructeur, 3 méthodes publiques.

#### Coquilles connues des énoncés
Voir `docs/coquilles_enonce.md` pour la liste complète et le statut de résolution. Tant qu'une coquille est `⏳ en attente`, l'équipe utilise la **correction présumée** documentée dans ce fichier.

#### Résolution du chemin INDEX (snippet imposé énoncé v0.2)
```java
URL location = SearchEngine.class.getProtectionDomain()
                                  .getCodeSource()
                                  .getLocation();
Path binFolder = Paths.get(location.toURI());
Path indexFolder = binFolder.resolve("INDEX");
SearchEngine se = new SearchEngine(indexFolder);
```
- **Ne pas utiliser** `Paths.get("INDEX")` directement : ça dépend du `cwd`, ça ne marche ni dans Eclipse ni en CLI selon le contexte.
- Le dossier `bin/INDEX/` doit contenir les fichiers d'index (extraits de `INDEX.zip` v0.2 ou `INDEX_FILES.7z` v0.4).

#### Affichage `printResults` (énoncé v0.2 textuel)
- Affiche les **15 résultats les plus pertinents**, du plus pertinent au moins pertinent.
- **Scores nuls exclus** — donc il peut y avoir moins de 15 résultats affichés.
- Format ligne par ligne : `SearchResult [url=..., score=...]`.

#### Mode CLI (énoncé v0.2)
- One-shot : `java -cp . search_engine.SearchEngine flan cerise` → résultats puis exit.
- Interactif : `java -cp . search_engine.SearchEngine` → boucle prompt jusqu'à `exit`.
- Concaténation des args : `String.join(" ", args)`.

#### Lemmatisation v0.3 (énoncé textuel)
- **Interdiction de modifier** `french_dictionary.txt` — *« puisque ce n'est pas vous qui générez l'indexation »*.
- La blacklist `blacklist.txt` est modifiable (mais ce n'est pas l'essentiel).
- Pipeline : `toLowerCase(Locale.FRANCE)` → split par `[^\\p{L}]+` → lemmatize → filtre blacklist → filtre `length() < 2`.
- Mot inconnu du dictionnaire : décision à documenter dans `doc/decisions_v0.3.md` (gardé en forme de surface conseillé).

#### Serveur web v0.5 (énoncé textuel)
- **Port 2026 imposé** (et non 8080).
- Commande unique : `herve web --recherche "<requête>"`.
- Routes : `GET /test` → `OK` (heartbeat), `GET /?recherche=<q>` → page HTML.
- Rendu **HTML+CSS côté serveur** (pas de JSON, pas de framework JS).
- ⚠️ **Bug officiellement signalé par l'énoncé** :
  ```java
  // ❌ FAUX (compte les caractères) :
  exchange.sendResponseHeaders(200, response.length());

  // ✅ CORRECT (compte les octets) :
  exchange.sendResponseHeaders(200, response.getBytes("UTF-8").length);
  ```

#### Sprint 6 — Crawler (piste A, optionnel)
- Politesse réseau **obligatoire** : 1 seconde minimum entre 2 requêtes au même hôte.
- `User-Agent` explicite : `HeRVe/1.0 (educational)`.
- Respect de `robots.txt`.
- `HttpClient.newHttpClient()` (JDK 11+).

#### Tests d'acceptation officiels (à respecter strictement)
- **v0.1** — sortie de référence sur `hello:10, world:5` :
  - `getPonderation("hello")` → `0.8944271909999159`
  - `getPonderation("other")` → `0.0`
  - `proximity(page2)` → `0.8304547985373998` (avec `page2` = `hello:5, ...`)
  - **tolérance 10⁻¹⁰** sur tous les flottants.
- **v0.2** — sur la requête `cerise flan` (corpus 100 pages) :
  ```
  SearchResult [url=https://fr.vikidia.org/wiki/Flan,      score=37.71273413657018]
  SearchResult [url=https://fr.vikidia.org/wiki/Clafoutis, score=16.116459280507602]
  SearchResult [url=https://fr.vikidia.org/wiki/Tarte,     score=5.076730825668095]
  ```
- **v0.3** — équivalences attendues :
  - `"les fruits"` ≡ `"fruit"` (lemmatisation + stopword retiré).
  - `"pommes ! de ?? terre."` ≡ `"pomme terre"` (regex split + stopwords).
  - `"PoMmE"` ≡ `"pomme"` (casse).
- **v0.4** — non-régression sur 100 pages : mêmes scores qu'à v0.2. Performance : `temps_moyen_par_requete < 200 ms` sur 38 000 pages.
- **v0.5** — heartbeat : `GET http://127.0.0.1:2026/test` → `OK` ; recherche : `GET http://127.0.0.1:2026/?recherche=flan` → page HTML 200 OK.

### Règles de tests (conventions TAP + Clean Code, calibrées sur R201)

#### Pas de framework de test
- **Pas de JUnit, pas de Mockito** — contrainte « zéro dépendance ».
- Tests = classe `SearchEngineTests` (package `search_engine_tests`) avec un `main` qui exécute des assertions maison.

#### Format de sortie : TAP (Test Anything Protocol)
Standard universel, parsable par CI/CD, lisible humain. Format minimal :
```
1..N                              ← plan : N = nombre total de tests
ok 1 - description du test 1
not ok 2 - description du test 2
  # expected: 0.83, actual: 0.84
ok 3 - description du test 3
```
- Chaque test = une ligne `ok <i> - <description>` ou `not ok <i> - <description>`.
- Lignes commençant par `#` = diagnostic informatif.
- Plan en première ou dernière ligne : `1..N`.

#### Helper d'assertions : classe `Assert` dédiée (DSL de tests)
Pour respecter DRY + Clean Code, extraire les assertions dans une classe `Assert` du package `search_engine_tests`, réutilisée par tous les sprints :
```java
package search_engine_tests;

public class Assert {
    private static final double EPSILON = 1e-10;
    private static int testNumber = 0;
    private static int passed = 0, failed = 0;

    public static void assertEquals(double expected, double actual, String label) {
        testNumber++;
        if (Math.abs(expected - actual) < EPSILON) {
            System.out.println("ok " + testNumber + " - " + label);
            passed++;
        } else {
            System.out.println("not ok " + testNumber + " - " + label);
            System.out.println("  # expected: " + expected + ", actual: " + actual);
            failed++;
        }
    }

    public static void assertEquals(String expected, String actual, String label) { /* idem */ }
    public static void assertEquals(int expected, int actual, String label) { /* idem */ }
    public static void assertTrue(boolean condition, String label) { /* idem */ }
    public static void assertNotNull(Object o, String label) { /* idem */ }

    public static void plan(int total) { System.out.println("1.." + total); }
    public static void summary() { System.out.println("# " + passed + " passed, " + failed + " failed"); }
}
```

#### Couverture obligatoire (énoncés v0.1 + v0.3)
- v0.1 : *« Cette classe devra tester **toutes les méthodes publiques** de IndexedPage »*
- v0.3 : *« **Tout ce que vous implémentez doit être correctement testé !** »*
- ➜ Chaque méthode publique de chaque classe a au moins un test.

#### Principes Clean Code appliqués
- **F.I.R.S.T.** : Fast, Independent, Repeatable, Self-validating, Timely.
- **One concept per test** : pas une assertion par test, un concept par test. Le nom du test doit dire ce qu'il vérifie.
- **Pattern AAA** : Arrange / Act / Assert dans chaque méthode de test.
  ```java
  private static void testProximityIsSymmetric() {
      // Arrange
      IndexedPage a = new IndexedPage(new String[]{"http://x", "hello:10"});
      IndexedPage b = new IndexedPage(new String[]{"http://y", "hello:5"});
      // Act
      double ab = a.proximity(b);
      double ba = b.proximity(a);
      // Assert
      Assert.assertEquals(ab, ba, "proximity is symmetric");
  }
  ```
- **Test code = production code** : mêmes standards (naming, indentation, pas de duplication).

#### Tests v0.5 : serveur réel sur port 2026
- Démarrer le `WebServer` au début de la classe de test, faire des `HttpClient` réels, arrêter le serveur à la fin (`server.stop(0)`).
- **Pas de mock** de `HttpExchange` (hors-programme R201, et serveur réel = plus simple).
- Penser à libérer le port 2026 entre deux runs.

#### Anti-patterns à éviter
- **Pas de tests qui dépendent du `cwd`** — utiliser le snippet `getProtectionDomain` pour les chemins.
- **Pas d'accès réseau externe** — uniquement `127.0.0.1:2026`.
- **Pas de tests qui modifient les ressources partagées** (`bin/INDEX/`, `french_dictionary.txt`) — toujours en lecture seule.
- **Pas de `Thread.sleep(...)` arbitraire** dans les tests — utiliser `server.start()` synchrone.

#### Lancement
```bash
./compile_projet
java -cp bin search_engine_tests.SearchEngineTests
```
Sortie attendue (exemple TAP) :
```
1..15
ok 1 - IndexedPage(String[]) stocke l'URL et les counts
ok 2 - getCount sur mot présent
not ok 3 - getNorm sur page vide retourne 0
  # expected: 0.0, actual: NaN
...
# 14 passed, 1 failed
```

### Code Quality & Style (Google Java Style + Spring conventions)

#### Indentation et formatage
- **4 espaces** d'indentation, jamais de tabs.
- **Longueur de ligne max : 100 caractères** (standard Google, adopté par la majorité de l'industrie). Lignes plus longues à wrapper, sauf URL Javadoc / package / imports.
- **Une instruction par ligne**.
- Accolade ouvrante en **fin de ligne** : `if (x) {`, jamais `if (x)\n{`.

#### Organisation des fichiers (step-down rule — Spring/Clean Code)
- **Une classe publique par fichier**, nom du fichier = nom de la classe + `.java`.
- Ordre dans une classe :
  1. Constantes `private static final` (UPPER_SNAKE_CASE).
  2. Attributs d'instance (`private`).
  3. Constructeurs (groupés ; multiples constructeurs **contigus**).
  4. Méthodes publiques, **chacune suivie immédiatement de ses méthodes privées d'aide**.
  5. Méthodes utilitaires statiques en bas.
- Les méthodes du même nom (surcharges, multiples constructeurs) sont **toujours contiguës** (Google).
- `package` en première ligne, `import` après, classe ensuite.
- **Pas de wildcard imports** (`import java.util.*;`) — toujours nominatif.

#### Documentation (Javadoc — règles Google)
- Javadoc **obligatoire** sur :
  - toute classe `public`/`protected`
  - toute méthode `public`/`protected`
  - toute constante `public`
- Exceptions tolérées : *self-explanatory* (`getFoo()` simple, méthodes `@Override`).
- Format strict :
  - Première ligne = phrase de résumé capitalisée et ponctuée.
  - Tags dans cet ordre : `@param`, `@return`, `@throws`, `@deprecated`.
  - Pas de description vide.
- **Pas de `@author`, `@version`, `@since`** — bruit visuel, l'info est dans Git.
- Exemple :
  ```java
  /**
   * Calcule la similarité cosinus entre cette page et la page passée.
   *
   * @param page la page à comparer
   * @return le produit scalaire normalisé, dans [0, 1]
   */
  public double proximity(IndexedPage page) { ... }
  ```

#### Commentaires dans le code
- Privilégier le **code expressif** (nom de variable/méthode > commentaire).
- Commentaires utiles seulement pour le **pourquoi** (intention, contrainte, workaround).
- Anti-pattern : `i++; // incrémente i`.
- Cas spécifique projet : commenter ponctuellement une **divergence d'énoncé non encore tranchée** (cf. `docs/coquilles_enonce.md`). Une fois la coquille confirmée par l'enseignante et l'énoncé local corrigé, on retire le commentaire.

#### Naming
- **Variables / méthodes / params** : `camelCase`.
- **Classes / interfaces** : `PascalCase`.
- **Constantes** (`static final` deeply immutable) : `UPPER_SNAKE_CASE`.
- **Packages** : `lowercase` (les énoncés imposent `search_engine` avec underscore).
- Variables = **rôle métier** (`lemmatizedQuery`, pas `str2`).
- Méthodes = **verbe** (`computeNorm`, `loadDictionary`).
- Booléens = **prédicat** (`isEmpty`, `hasResults`, `containsWord`).

#### Magic numbers & strings (constantes locales à la classe)
- Toute constante non-triviale → `private static final` **dans la classe qui l'utilise** (cohésion forte). **Pas de classe `Constants` globale** (couplage fort, anti-pattern enterprise).
- Si une constante est partagée entre 2 classes : la mettre dans la classe sémantiquement la plus pertinente, y accéder via le nom (`WebServer.PORT`).
- Exemples HeRVé :
  ```java
  // dans IndexedPage
  private static final double EPSILON = 1e-10;

  // dans SearchEngine
  private static final int TOP_RESULTS = 15;
  private static final String EXIT_COMMAND = "exit";

  // dans WebServer
  private static final int PORT = 2026;
  private static final String HEARTBEAT_RESPONSE = "OK";
  ```
- Exception : `0`, `1`, `-1`, `""`, `" "` peuvent rester littéraux quand le contexte est évident.
- ⚠️ Une `HashMap` `static final` n'est **pas** une constante (Google) — elle est mutable. Nommer en `camelCase` (ex. `private static final HashMap<String, String> dictionary`).

#### Méthodes courtes (Clean Code)
- Cible **15-20 lignes** par méthode (max 30). Au-delà, extraire en privées.
- Max **3 niveaux d'imbrication** (`if`/`while`/`for`). Au-delà, extraire ou utiliser early-return.
- **Un seul niveau d'abstraction** par méthode : ne pas mélanger I/O et calcul.
- Step-down rule : la méthode appelante juste au-dessus de l'appelée privée.

#### DRY (Don't Repeat Yourself)
- Si tu copies-colles un bloc, extrais-le en méthode privée.
- Si une logique se répète entre classes, extrais-la dans une classe utilitaire dédiée (ex. `TextUtils` pour lemmatisation/stopwords si réutilisée par le crawler Sprint 6).

#### Eclipse — configuration recommandée
- Importer le profil **Google Java Style** : <https://github.com/google/styleguide/blob/gh-pages/eclipse-java-google-style.xml> via `Preferences > Java > Code Style > Formatter > Import`.
- Activer `Save Actions` : auto-format, organize imports, remove unused imports, missing `@Override`.
- Warnings utiles : raw types, unused variables, unchecked casts.

### Workflow Git & équipe

#### Hébergeur & accès
- **GitLab IUT** : `https://iut-git.unice.fr/s201-25-26/<groupe>/herve` (fork du dépôt template, sans renommer).
- Accès SSH depuis l'extérieur du réseau IUT → **VPN universitaire** requis.
- Rôles : chef de projet **Maintainer**, équipiers **Developer**.

#### Branches (imposé par les énoncés + GitLab Flow)
- **`main`** : branche protégée. Push direct interdit, MR obligatoire.
- **`v0.1`, `v0.2`, ..., `v0.5`** : une branche par version, créée depuis le tag de la précédente.
- **Branches de feature** (recommandé) : `feat/v0.X-<short-name>` (ex. `feat/v0.1-indexed-page-tests`), mergées dans la branche de version via MR.
- ⚠️ **Tags** : `v0.1`, `v0.2`, ..., `v0.5` sur le commit final de chaque version.
- **Discipline absolue** : un tag mal nommé = rendu non détecté = zéro (énoncé v0.1 textuel).
- **Vérifier avant push final** : `git tag -l` puis comparer avec ce qui est attendu.

#### Messages de commit — Conventional Commits
Format pro reconnu (Angular, Vue, kernel Linux) :
```
<type>(<scope>): <description courte au présent>
```
Types autorisés : `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`.
Scope : nom de classe ou de version (`indexed-page`, `v0.4`).

Exemples :
```
feat(indexed-page): ajoute les 3 constructeurs et les méthodes publiques
fix(search-engine): corrige le tri décroissant des SearchResult
refactor(v0.4): migre String[]/int[] vers HashMap<String,Integer>
test(lemmatizer): couvre les cas d'accents et de ponctuation
```

#### Merge Requests (MR)
- **Une MR par tâche** (S1.1, S1.2, etc.) — pas de MR fourre-tout.
- Titre = sujet du commit principal (style Conventional Commits).
- Description : checklist des critères d'acceptation cochés (issus de la TDL).
- **Review obligatoire** par un autre équipier avant merge. Le **chef de projet (Johan, casquette CP)** approuve les MR de fin de version.
- **Merge classique** (pas squash) vers les branches `v0.X` — préserve l'historique fin des commits de feature pour la traçabilité en soutenance.
- ⚠️ **`compile_projet` et `herve` ne doivent jamais apparaître dans le diff d'une MR** — sauf MR dédiée et approuvée par 2 reviewers.

#### CI/CD GitLab (`.gitlab-ci.yml` à la racine)
- Pipeline minimal qui s'exécute sur chaque push :
  1. Job `build` : `./compile_projet` (vérifie que ça compile sans warning).
  2. Job `test` : lance `SearchEngineTests`, sortie TAP parsée par GitLab.
- Image Docker : `eclipse-temurin:17-jdk` (OpenJDK 17 officiel).
- Job rouge → MR bloquée → discipline d'équipe.

#### Fichier `CONTRIBUTING.md` à la racine
Documente les conventions pour l'équipe : branches, tags, commits, MR, tests.

#### Rôles & responsabilités (issu de la TDL)
- **Haithem (D1)** : I/O, persistance, classpath.
- **Hoang Xuan Mai (D3)** : TALN, algos avancés, frontend.
- **Theo (D2 unique)** : Sprint 0 + classes cœur sur toutes les versions.
- **Johan (CP + D4 + Sprint 6 solo)** : coordination, tests/perf/review, rendu créatif.
- Pour qu'un agent IA sache à qui adresser une question : `[Nom]` ou `[Nom/Rôle]` dans le commit/MR.

#### Anti-patterns à éviter
- **Pas de `force-push`** sur `main` / `v0.X` — historique partagé, jamais réécrit.
- **Pas de commits monolithiques** type "v0.1 complète".
- **Pas de fichiers binaires** committés (`.class`, `INDEX_FILES.7z` extrait).
- **Pas de modifs sur `main` directement** sauf le merge final via MR du CP.
- **Pas de `.idea/`, `.vscode/`, `.settings/`** dans le repo.

#### Procédure de rendu (par version) — checklist pre-push
1. ☐ Tous les tests passent (`SearchEngineTests` → `# N passed, 0 failed`).
2. ☐ `./compile_projet` passe sans warning.
3. ☐ `./herve <requête>` fonctionne en CLI.
4. ☐ Pipeline GitLab CI vert sur le dernier commit.
5. ☐ Commit final sur la branche `v0.X`.
6. ☐ Tag `v0.X` posé : `git tag v0.X -m "version 0.X"`.
7. ☐ Push avec tags : `git push origin v0.X --tags`.
8. ☐ Vérifier sur GitLab : la page du tag affiche bien `v0.X` daté avant l'échéance.
9. ☐ Archive ZIP du dossier source déposée sur Moodle.

### Critical Don't-Miss Rules

#### 🚫 Pièges Java récurrents
- **Comparaison de doubles** : jamais `==`, toujours `Math.abs(a-b) < EPSILON`. Le calcul de norme/cosinus génère des écarts en 10⁻¹⁶.
- **`String == String`** : compare les références, pas le contenu. Toujours `.equals()`.
- **`new Integer(int)`** : déprécié depuis Java 9. Utiliser `Integer.valueOf(int)` ou autoboxing.
- **`int / int` → `int`** : `1 / 2 == 0`, pas `0.5`. Forcer `(double) a / b`.
- **Locale par défaut** : `String.toLowerCase()` sans `Locale.FRANCE` casse les accents (cf. *Turkish I problem*).

#### 🚫 Pièges I/O
- **Charset par défaut** : toujours UTF-8 explicite (`StandardCharsets.UTF_8` ou `"UTF-8"`).
- **`Files.readAllLines` charge tout en RAM** : OK petits fichiers, KO 38k pages → `BufferedReader` en streaming.
- **`Paths.get("INDEX")`** : dépend du `cwd`. Toujours utiliser le snippet `getProtectionDomain()` officiel.
- **Oublier `close()`** : utiliser `try-with-resources`.

#### 🚫 Pièges Collections
- **`Arrays.asList()` est immuable en taille** : `list.add(...)` lève `UnsupportedOperationException`.
- **Itérer + modifier** : `ConcurrentModificationException`. Utiliser `Iterator.remove()`.
- **`HashMap` n'a pas d'ordre** : si l'ordre compte, utiliser `LinkedHashMap` ou trier.
- **Capacité initiale `HashMap`** : pour 38k pages, prédimensionner (`new HashMap<>(50_000)`).

#### 🚫 Pièges spécifiques HeRVé
- **`getNorm()`** retourne `double` (suivre diagramme v0.1 ; coquille texte confirmée le 2026-05-10).
- **`launchRequest()`** en camelCase, attribut/paramètre **`indexationDirectory`** en camelCase aussi (coquilles v0.2 `launch_request` / `indexation_directory` confirmées le 2026-05-10).
- **`toString()` format strict** : `"IndexedPage [url=...]"`, pas `"IndexedFile"`.
- **`printResults`** : 15 max, scores nuls exclus.
- **`exit`** comparaison avec `.equals()`.
- **Snippet INDEX** : `new SearchEngine(indexFolder)`, pas `index` (coquille v0.2 confirmée le 2026-05-10).

#### 🚫 Pièges v0.3 (lemmatisation)
- **NE PAS modifier `french_dictionary.txt`** (énoncé textuel).
- **Charger le dictionnaire UNE SEULE FOIS** au démarrage de `SearchEngine`.
- **Stopwords avant ou après lemmatisation ?** Choix à documenter dans un ADR.
- **Mots de 1-2 lettres** : décision documentée à prendre.

#### 🚫 Pièges v0.4 (passage à l'échelle)
- **`String.intern()`** en boucle massive peut saturer Metaspace.
- **`parallelStream()`** sur petites collections : overhead > gain.
- **OutOfMemoryError sur 38k pages** : pré-dimensionner les `HashMap`, fermer les readers.
- **Benchmark naïf** : faire un *warm-up* avant de mesurer (JIT compile après quelques itérations).

#### 🚫 Pièges v0.5 (interface web)
- **`response.length()` vs `response.getBytes("UTF-8").length`** : bug officiellement signalé. Toujours octets.
- **Port 2026 occupé** : `BindException`. Toujours `server.stop(0)` à la fin des tests.
- **Charset HTTP** : header `Content-Type: text/html; charset=utf-8` obligatoire.
- **HTML injection** : toujours échapper via `HtmlEscape.body(...)` (cf. ADR-0004).
- **URL decoding** : utiliser `URLDecoder.decode(s, "UTF-8")`, pas un `replace('+', ' ')` artisanal.

#### 🚫 Pièges Sprint 6
Voir `docs/sprint6/` (un fichier par piste). Règles communes :
- Politesse réseau pour le crawler (1 s minimum entre 2 requêtes même hôte).
- `User-Agent` explicite : `HeRVe/1.0 (educational)`.
- Respect de `robots.txt`.

#### 🚫 Pièges Git
- **Tag mal nommé** = rendu non détecté = zéro. Toujours `git tag -l` avant push.
- **Push sans `--tags`** : tag local invisible côté GitLab.
- **`compile_projet`/`herve` modifiés par mégarde** : vérifier `git diff` avant commit.

#### 🚫 Pièges soutenance
- **Ne pas savoir expliquer un choix** = points perdus → utiliser les **ADR** dans `docs/adr/`.
- **Démo qui plante** : tester sur un autre poste avant.
- **Plan B** : capture vidéo de la démo en local.
- **QCM possibles** sur les structures de données (énoncé v0.4) : connaître HashMap, HashSet, ArrayList, LinkedList.

---

## Documents de référence (à consulter quand pertinent)

| Doc | Rôle |
| --- | --- |
| `docs/cahier_des_charges.md` | Synthèse projet (v1.0, à jour avec PDF v0.5 officiel) |
| `TDL.md` | Plan d'exécution détaillé par sprint, par équipier |
| `CONTRIBUTING.md` | Conventions Git, MR, tests, format de commit |
| `docs/adr/` | Architecture Decision Records (justification des choix) |
| `docs/sprint6/` | Pistes A/B/C du rendu final (charger uniquement la piste choisie) |
| `docs/coquilles_enonce.md` | Liste des coquilles repérées dans les PDF officiels + statut |
| `msg_pourcelot.txt` | Mail à envoyer à l'enseignante pour clarifier les coquilles |

---

## Usage Guidelines

### Pour les agents IA
- **Lire ce fichier en intégralité** avant toute implémentation.
- En cas de doute, **suivre la règle la plus restrictive**.
- Quand un PDF d'énoncé entre en conflit avec ce document : **le PDF gagne**, mais signaler la divergence dans `docs/coquilles_enonce.md`.
- Pour une décision structurante non couverte ici : **proposer un nouvel ADR** (cf. `docs/adr/template.md`) plutôt que de trancher seul.

### Pour les humains de l'équipe
- Garder ce fichier **lean** — pas de duplication avec `CONTRIBUTING.md` ou les ADR.
- Mettre à jour quand :
  - une coquille d'énoncé est tranchée par Mme Pourcelot
  - une décision structurante change (nouvel ADR `Supersedes`)
  - une nouvelle convention émerge en équipe
- Revue **à chaque fin de version** (`v0.X`) pour purger ce qui est devenu obvious.

*Dernière mise à jour : 2026-05-09.*


