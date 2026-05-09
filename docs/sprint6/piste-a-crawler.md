# Sprint 6 — Piste A : Indexation à froid (crawler)

> **Difficulté** : ⭐⭐⭐ (la plus complexe). Charge estimée : ~12 h.
> **Énoncé** : *« Construire son propre index, pour pouvoir indexer n'importe quel site, pas seulement Vikidia »*.

## Objectif

Permettre la commande `./herve index https://exemple.org` qui crawle le site cible et produit des fichiers d'index au **format v0.2** (URL ligne 1, `mot:occurrences` lignes suivantes).

## Sous-tâches

### S6.A.1 — Client HTTP
- `HttpClient.newHttpClient()` (JDK 11+).
- Requête GET, parsing du body (UTF-8 explicite).
- Timeout raisonnable (10 s).

### S6.A.2 — Politesse réseau (OBLIGATOIRE)
- ⚠️ **1 seconde minimum** entre 2 requêtes au même hôte (énoncé v0.6 : *« L'IP qui crawl trop vite se fait bannir — c'est de l'apprentissage par la douleur qu'on préfère éviter »*).
- Header `User-Agent: HeRVe/1.0 (educational)`.
- Backoff exponentiel sur HTTP 429 / 503.
- **Respecter `robots.txt`** : récupérer `https://<host>/robots.txt`, parser, ne pas crawler les `Disallow`.

### S6.A.3 — Extraction de texte
- `replaceAll("<[^>]+>", " ")` (suffisant selon l'énoncé).
- Décodage des entités HTML les plus courantes (`&amp;`, `&nbsp;`, `&lt;`, `&gt;`, `&quot;`, `&#39;`).
- Normalisation des espaces (`\\s+` → ` `).

### S6.A.4 — Lemmatisation locale
- Réutiliser `Lemmatizer` de v0.3.
- ⚠️ Cohérence avec l'index existant : utiliser le **même** `french_dictionary.txt`.

### S6.A.5 — Génération des fichiers d'index
- Format strict v0.2 : ligne 1 URL, lignes suivantes `mot:occurrences`.
- Encodage UTF-8, EOL `\n`.
- Nom de fichier : hash de l'URL ou slug de l'URL (cohérent avec les fichiers Vikidia fournis).

### S6.A.6 — Crawler BFS
- File d'attente d'URL à visiter (`LinkedList<URL>`, vu en cours).
- Set d'URL visitées (`HashSet<URL>`, vu en cours) — **éviter les boucles**.
- Extraction des liens via regex `href="([^"]+)"`.
- Limitation : même domaine que l'URL d'entrée, profondeur max paramétrable.

### S6.A.7 — Reprise après interruption
- Journal des URL visitées sur disque (fichier `.crawl_state`).
- Si interruption (Ctrl+C, plantage), redémarrer reprend la file là où elle s'est arrêtée.

### S6.A.8 — Tests
- Indexer 50 pages d'un **petit site jouet** (pas Vikidia entier).
- Lancer `./herve <requête>` sur le nouvel index : vérifier que les résultats remontent.
- Test unitaire de la lemmatisation cohérente entre crawler et requête.

## KPI à mesurer (pour la soutenance)

| Métrique | Cible |
| --- | --- |
| Pages crawlées sur 1 h | ≥ 3000 (limite politesse 1 s/req) |
| Précision Top-10 sur 30 requêtes étalon | ≥ 70 % |
| Reprise après crash | fonctionnelle |
| Conformité `robots.txt` | 100 % |

## Risques principaux

| Risque | Probabilité | Mitigation |
| --- | :---: | --- |
| IP bannie par le site cible | F | délai 1 s + backoff exponentiel sur 429 + User-Agent explicite |
| Boucle infinie sur les liens cycliques | M | visited-set, profondeur max |
| Encodage cassé (latin-1 vs UTF-8) | M | toujours UTF-8 explicite côté client HTTP |
| Lemmatisation différente de l'index Vikidia | M | utiliser le **même** dictionnaire fourni |

## Références

- [JDK HttpClient](https://docs.oracle.com/en/java/javase/17/docs/api/java.net.http/java/net/http/HttpClient.html)
- [robots.txt specification (RFC 9309)](https://datatracker.ietf.org/doc/rfc9309/)
- [OWASP — Server-Side Request Forgery (SSRF) Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
