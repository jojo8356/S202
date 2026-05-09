# Contributing à HeRVé

Ce document décrit les conventions de travail de l'équipe **HeRVé** (S2.02 · UniCA 2025-2026).
Lecture obligatoire avant la première contribution.

---

## 1. Structure du dépôt

```
.
├── src/
│   ├── search_engine/         ← code de production
│   └── search_engine_tests/   ← classe de tests + classe Assert
├── bin/                       ← classes compilées (régénéré)
│   └── INDEX/                 ← fichiers d'index (extraits, non versionnés)
├── docs/                      ← documentation
├── ressources/                ← données brutes (dico, blacklist, archives)
├── compile_projet             ← script — NE PAS MODIFIER
├── herve                      ← script — NE PAS MODIFIER
├── README.md                  ← interface CLI exacte
└── CONTRIBUTING.md            ← ce fichier
```

> ⚠️ Les fichiers `compile_projet` et `herve` sont **figés**. Toute modification doit passer par une MR dédiée approuvée par 2 reviewers (filet de sécurité contre une casse accidentelle qui ferait perdre la note de rendu).

---

## 2. Workflow Git

### 2.1 Branches

| Branche | Rôle |
| --- | --- |
| `main` | branche protégée, push direct interdit, MR obligatoire avec ≥ 1 approbation |
| `v0.1`, `v0.2`, ..., `v0.5` | une branche par version, créée depuis le tag de la précédente |
| `feat/v0.X-<short-name>` | branche de feature, mergée dans `v0.X` via MR (ex. `feat/v0.1-indexed-page-tests`) |

### 2.2 Créer une nouvelle branche de version

```bash
git checkout v0.1                  # depuis le tag
git checkout -b v0.2               # nouvelle branche
git push -u origin v0.2
```

### 2.3 Tags de rendu

Chaque version se termine par un tag annoté sur le commit final.

```bash
git tag v0.1 -m "version 0.1"
git push origin v0.1 --tags
```

> ⚠️ **Discipline absolue** : un tag mal nommé = rendu non détecté = zéro (énoncé officiel v0.1).
> Vérifier avec `git tag -l` avant le push final.

---

## 3. Conventions de commits — Conventional Commits

Format reconnu en industrie (Angular, Vue, kernel Linux) :

```
<type>(<scope>): <description courte au présent>

[corps optionnel : pourquoi, contexte]

[footer optionnel : Co-Authored-By, refs issues]
```

### 3.1 Types autorisés

| Type | Quand l'utiliser |
| --- | --- |
| `feat` | nouvelle fonctionnalité |
| `fix` | correction de bug |
| `docs` | documentation seule |
| `test` | ajout/modif de tests seuls |
| `refactor` | refactoring sans changement de comportement |
| `perf` | amélioration de performance |
| `chore` | tâches techniques (config, scripts, deps) |

### 3.2 Scope

Nom de classe ou de version : `indexed-page`, `search-engine`, `v0.4`, `lemmatizer`, `web-server`.

### 3.3 Exemples

```
feat(indexed-page): ajoute les 3 constructeurs et les méthodes publiques
fix(search-engine): corrige le tri décroissant des SearchResult
refactor(v0.4): migre String[]/int[] vers HashMap<String,Integer>
docs(coquilles): documente les 8 incohérences des PDF officiels
test(lemmatizer): couvre les cas d'accents et de ponctuation
perf(search-engine): pré-calcule la norme à la construction
chore: ajoute la pipeline GitLab CI
```

### 3.4 Anti-patterns

```
Update files                         ← pas de type, scope, intention
fixed the bug                        ← passé, pas de scope
v0.1 complète                        ← monolithique, ne décrit rien
WIP                                  ← jamais en main
```

---

## 4. Merge Requests (MR)

### 4.1 Règles

- **Une MR par tâche** (S1.1, S1.2, etc. de la TDL) — jamais de MR fourre-tout.
- **Titre** = sujet du commit principal (style Conventional Commits).
- **Description** : checklist des critères d'acceptation cochés (extraits de la TDL).
- **Review** obligatoire par un autre équipier avant merge.
- **Approbation finale** de version par Johan (chef de projet).
- **Merge classique** (pas squash) — préserve l'historique fin pour la soutenance.

### 4.2 Template de description

```markdown
## Tâche TDL
Sxx.yy <titre de la tâche>

## Critères d'acceptation
- [x] critère 1
- [x] critère 2
- [ ] critère 3 (TODO)

## Tests
- [x] Tous les tests existants passent
- [x] Nouveaux tests ajoutés pour les méthodes publiques

## Notes
<contraintes, choix, points d'attention pour le reviewer>
```

### 4.3 Reviewer — checklist

- [ ] Le code respecte le **Google Java Style** (longueur ≤ 100 char, naming, organisation).
- [ ] Tous les nouveaux membres `public`/`protected` ont une **Javadoc**.
- [ ] Les **constantes** sont en `UPPER_SNAKE_CASE` `private static final`.
- [ ] Pas de **magic number** (sauf `0`, `1`, `-1`, `""`).
- [ ] Pas de **wildcard import** (`java.util.*`).
- [ ] Les nouvelles méthodes publiques ont un **test associé**.
- [ ] Le pipeline CI est **vert**.
- [ ] Aucun fichier non désiré (`.class`, IDE settings) dans le diff.
- [ ] `compile_projet` et `herve` non modifiés.

---

## 5. Lancer les tests

### 5.1 En local

```bash
# Compilation
./compile_projet

# Tests (sortie TAP sur stdout)
java -cp bin search_engine_tests.SearchEngineTests
```

Sortie attendue (exemple) :
```
1..15
ok 1 - IndexedPage(String[]) stocke l'URL et les counts
ok 2 - getCount sur mot présent
not ok 3 - getNorm sur page vide retourne 0
  # expected: 0.0, actual: NaN
...
# 14 passed, 1 failed
```

### 5.2 Sur GitLab CI

Le pipeline `.gitlab-ci.yml` lance automatiquement build + test sur chaque push.
Voir les jobs dans `CI/CD > Pipelines` du projet GitLab.

Une MR ne peut pas être mergée si le pipeline est rouge (sauf override CP).

### 5.3 Couverture obligatoire

- v0.1 énoncé : *« Cette classe devra tester **toutes les méthodes publiques** de IndexedPage »*.
- v0.3 énoncé : *« **Tout ce que vous implémentez doit être correctement testé !** »*.

➜ Chaque méthode publique de chaque classe a au moins un test.

---

## 6. Configuration locale (par IDE)

Le `.editorconfig` à la racine couvre déjà les bases (4 espaces, UTF-8, EOL `LF`, ligne max 100 char) — supporté nativement par Eclipse, IntelliJ, VSCode, et via plugin pour Neovim. Pour le formatage Java spécifique (ordre imports, accolades, alignements), chaque IDE doit charger le profil **Google Java Style** :

🔗 <https://raw.githubusercontent.com/google/styleguide/gh-pages/eclipse-java-google-style.xml>

### 6.1 Eclipse

**Profil de formatage** :
`Window > Preferences > Java > Code Style > Formatter > Import...` → choisir le XML téléchargé.

**Save Actions** :
`Preferences > Java > Editor > Save Actions` → cocher :
- Format source code (Format edited lines)
- Organize imports
- Additional actions : Add missing `@Override`, Remove unused imports.

**Warnings utiles** :
`Preferences > Java > Compiler > Errors/Warnings` → activer :
- Raw types : Warning
- Unused local or private member : Warning
- Unchecked generic type operation : Warning
- Missing `@Override` annotation : Warning

### 6.2 VSCode

**Extensions** : installer le pack officiel **Extension Pack for Java** (Microsoft, ID `vscjava.vscode-java-pack`) — il fournit `redhat.java` (LSP basé sur Eclipse JDT), Maven, debugger, tests.

**Configuration** (`.vscode/settings.json` ou settings utilisateur) :
```json
{
  "java.format.settings.url": "https://raw.githubusercontent.com/google/styleguide/gh-pages/eclipse-java-google-style.xml",
  "java.format.settings.profile": "GoogleStyle",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  },
  "java.saveActions.organizeImports": true,
  "java.completion.importOrder": ["java", "javax", "com", "org"],
  "files.encoding": "utf8",
  "files.eol": "\n"
}
```

> Le LSP `redhat.java` télécharge et applique le XML Eclipse — donc même formatter que les Eclipse-istes de l'équipe : pas de drift de style.

### 6.3 Neovim

**Stack recommandée** : `nvim-jdtls` (JDT Language Server, mêmes règles que Eclipse) + `conform.nvim` pour formater à la sauvegarde.

**Pré-requis CLI** :
```bash
# Installer google-java-format (pour conform.nvim ou usage CLI direct)
sudo apt install google-java-format          # Debian/Ubuntu, à défaut :
brew install google-java-format              # macOS
# ou télécharger le JAR depuis https://github.com/google/google-java-format/releases
```

**Avec `nvim-jdtls`** (utilisé par `lsp-zero` ou config manuelle) — pointer vers le XML Google :
```lua
require('jdtls').start_or_attach({
  cmd = { 'jdtls' },
  settings = {
    java = {
      format = {
        enabled = true,
        settings = {
          url = "https://raw.githubusercontent.com/google/styleguide/gh-pages/eclipse-java-google-style.xml",
          profile = "GoogleStyle",
        },
      },
      saveActions = { organizeImports = true },
    },
  },
})
```

**Avec `conform.nvim`** (alternative plus légère, utilise le CLI `google-java-format`) :
```lua
require("conform").setup({
  formatters_by_ft = {
    java = { "google-java-format" },
  },
  format_on_save = { lsp_fallback = true, timeout_ms = 1500 },
})
```

### 6.4 IntelliJ IDEA (si quelqu'un l'utilise)

`File > Settings > Editor > Code Style > Java > ⚙ > Import Scheme > Eclipse XML Profile...` → choisir le XML téléchargé. Activer `Reformat code` et `Optimize imports` dans les Actions on Save.

---

## 7. Procédure de rendu d'une version (chef de projet)

Checklist pre-push :

1. ☐ Tous les tests passent (`# N passed, 0 failed`).
2. ☐ `./compile_projet` passe sans warning.
3. ☐ `./herve <requête>` fonctionne en CLI.
4. ☐ Pipeline CI vert sur le dernier commit.
5. ☐ Commit final sur la branche `v0.X`.
6. ☐ Tag `v0.X` posé.
7. ☐ Push avec tags.
8. ☐ Vérifier sur GitLab : la page du tag affiche bien `v0.X` daté avant l'échéance.
9. ☐ Archive ZIP du dossier source déposée sur Moodle (canal de rendu en parallèle).

---

## 8. Coquilles connues des énoncés

Voir `docs/coquilles_enonce.md` pour la liste complète et le statut de résolution. Tant qu'une coquille est `⏳ en attente`, l'équipe utilise la **correction présumée** documentée dans ce fichier.

---

## 9. Échéances

| Version | Échéance | Branche / Tag |
| --- | --- | --- |
| v0.1 | vendredi 15 mai 2026, 20:00 | `v0.1` |
| v0.2 | vendredi 22 mai 2026, 20:00 | `v0.2` |
| v0.3 | lundi 26 mai 2026, 20:00 | `v0.3` |
| v0.4 | vendredi 29 mai 2026, 20:00 | `v0.4` |
| v0.5 | vendredi 5 juin 2026, 20:00 | `v0.5` |
| Rendu final | vendredi 12 juin 2026, 20:00 | `final` ou `v1.0` |
| Soutenance | semaine 25 (S25) | — |

---

*Dernière mise à jour : 2026-05-09. Toute évolution de ces conventions passe par une MR sur ce fichier.*
