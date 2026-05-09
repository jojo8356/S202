# 0004 — Classe utilitaire `HtmlEscape` (zéro dépendance)

- **Status** : Accepted
- **Date** : 2026-05-09
- **Décideur·s** : Johan (CP/D4)
- **Sprint concerné** : v0.5 (interface web), Sprint 6 piste A si rendu HTML

## Contexte

L'interface web v0.5 rend du HTML côté serveur (énoncé v0.5 : *« on récupère ensuite les résultats de la recherche correspondante et on renvoie le code HTML et le code CSS appropriés »*). La requête utilisateur sera affichée dans la page (*« vous avez recherché : <q> »*).

Sans échappement, une requête malicieuse type `<script>alert(1)</script>` est exécutée par le navigateur (XSS, OWASP A03 *Injection*). Même sans intention malicieuse, des caractères communs (`<`, `>`, `&`) cassent le HTML rendu.

La contrainte « zéro dépendance » exclut OWASP Java Encoder, Apache Commons Text, et les frameworks (Spring, Thymeleaf) qui font l'échappement automatiquement.

## Options envisagées

### A — Escape inline dans `WebServer.java`
```java
String safe = q.replace("&", "&amp;").replace("<", "&lt;")...;
```
- ✅ Pour : pas de classe supplémentaire.
- ❌ Contre : duplication si plusieurs endroits rendent du HTML, pas testable isolément, viole DRY.

### B — Classe utilitaire `HtmlEscape` dédiée
```java
HtmlEscape.body(userInput)
```
- ✅ Pour : DRY, testable isolément, signature expressive, réutilisable Sprint 6.
- ❌ Contre : une classe de plus.

### C — OWASP Java Encoder (lib externe)
- Standard pro recommandé par OWASP.
- ❌ Contre : interdit par la contrainte « zéro dépendance ».

## Décision

> **Option B — Classe utilitaire `HtmlEscape` dans `search_engine`**

Rationale :
- Aligné Clean Code (DRY, *« test code = production code »*).
- Constructeur privé pour empêcher l'instanciation (utilitaire stateless).
- Échappe les **6 caractères critiques** recommandés par l'OWASP XSS Prevention Cheat Sheet.
- ⚠️ **`&` doit être échappé en premier**, sinon double-échappement (`<` → `&lt;` → `&amp;lt;`).

## Spécification

```java
package search_engine;

/**
 * Utilitaire d'échappement HTML pour le rendu côté serveur.
 *
 * <p>Échappe les caractères critiques pour éviter les injections XSS
 * (OWASP A03) lors du rendu d'entrées utilisateur dans une page HTML.
 *
 * <p>Conforme à l'OWASP XSS Prevention Cheat Sheet — règles n°1 et 2
 * (HTML body et attribut). Pour le contexte JavaScript ou URL, des règles
 * supplémentaires s'appliquent (voir OWASP Java Encoder).
 */
public final class HtmlEscape {

    private HtmlEscape() {
        // Pas d'instanciation (utilitaire stateless).
    }

    /**
     * Échappe une chaîne destinée au corps d'une page HTML.
     *
     * @param input la chaîne brute (peut être null)
     * @return la chaîne échappée, ou "" si input est null
     */
    public static String body(String input) {
        if (input == null) {
            return "";
        }
        return input.replace("&", "&amp;")  // & en PREMIER (sinon double-escape)
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\"", "&quot;")
                    .replace("'", "&#x27;")
                    .replace("/", "&#x2F;");
    }
}
```

## Conséquences

### Positives
- Pas de dépendance externe.
- Testable isolément (cf. tests v0.5).
- Réutilisable Sprint 6 piste A (rendu d'aperçus de pages crawlées).
- Conforme aux recommandations OWASP pour le contexte HTML body.

### Négatives / risques acceptés
- Ne couvre **pas** les contextes JavaScript inline, attributs `style`, ou URL — pas nécessaires pour HeRVé.
- Si on doit rendre du contenu déjà encodé en entité HTML, double-échappement possible (vérifier la chaîne de transformation).

### Suivi
- ☐ Tâche TDL : ajouter S5.3.x — implémenter et tester `HtmlEscape`.
- ☐ Tests unitaires obligatoires :
  - `body(null)` → `""`
  - `body("")` → `""`
  - `body("<script>")` → `"&lt;script&gt;"`
  - `body("a & b")` → `"a &amp; b"` (pas `"a &amp;amp; b"`)
  - `body("\"quoted\"")` → `"&quot;quoted&quot;"`

## Références

- [OWASP XSS Prevention Cheat Sheet](https://jcarpizo.github.io/owasp-info/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP Java Encoder](https://owasp.org/www-project-java-encoder/) (référence, non utilisée)
- [Apache Commons Text — escapeHtml4](https://commons.apache.org/proper/commons-text/) (référence, non utilisée)
