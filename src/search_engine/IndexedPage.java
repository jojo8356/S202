package search_engine;

import java.util.TreeMap;

/**
 * Représente une page web indexée sous forme de vecteur de mots/occurrences.
 *
 * <p>Chaque page est caractérisée par son URL canonique et un sac de mots
 * stocké dans deux tableaux parallèles : {@code words} (les mots distincts)
 * et {@code counts} (le nombre d'occurrences de chaque mot).
 *
 * <p>Trois constructeurs sont prévus :
 * <ul>
 *   <li>depuis un tableau de lignes au format {@code mot:occurrences} (fichier index),</li>
 *   <li>depuis un fichier d'index sur disque (implémenté en v0.2),</li>
 *   <li>depuis un texte brut (utilisé pour transformer une requête en page virtuelle).</li>
 * </ul>
 */
public class IndexedPage {

    private String url;
    private String[] words;
    private int[] counts;

    /**
     * Construit une page indexée depuis un tableau de lignes.
     *
     * <p>La première ligne est l'URL de la page. Les suivantes sont au format
     * {@code mot:occurrences} (exactement un {@code :}, pas d'espace).
     *
     * @param lines les lignes de l'index (au moins l'URL)
     * @throws IllegalArgumentException si {@code lines} est null ou vide,
     *     ou si une ligne ne respecte pas le format {@code mot:occurrences}
     */
    public IndexedPage(String[] lines) {
        if (lines == null || lines.length == 0) {
            throw new IllegalArgumentException("lines ne peut pas être null ni vide");
        }

        url = lines[0];
        words = new String[lines.length - 1];
        counts = new int[lines.length - 1];

        for (int i = 1; i < lines.length; i++) {
            String[] parts = lines[i].split(":");
            if (parts.length != 2) {
                throw new IllegalArgumentException(
                    "Ligne mal formée (attendu \"mot:occurrences\") : " + lines[i]);
            }
            words[i - 1] = parts[0];
            counts[i - 1] = Integer.parseInt(parts[1]);
        }
    }

    /**
     * Construit une page virtuelle depuis un texte brut (typiquement une requête).
     *
     * <p>Le texte est découpé sur les espaces, les mots distincts sont comptés,
     * et la liste résultante est triée par ordre lexicographique (via {@link TreeMap}).
     * L'URL d'une page créée par ce constructeur reste {@code null}.
     *
     * @param text le texte source (ne peut pas être null)
     * @throws IllegalArgumentException si {@code text} est null
     */
    public IndexedPage(String text) {
        if (text == null) {
            throw new IllegalArgumentException("text ne peut pas être null");
        }

        url = null;
        String[] tokens = text.split("\\s+");

        // TreeMap : comptage + tri lexicographique en une passe.
        TreeMap<String, Integer> freq = new TreeMap<>();
        for (String token : tokens) {
            if (!token.isEmpty()) {
                freq.put(token, freq.getOrDefault(token, 0) + 1);
            }
        }

        words = freq.keySet().toArray(new String[0]);
        counts = new int[words.length];
        int i = 0;
        for (int val : freq.values()) {
            counts[i++] = val;
        }
    }

    @Override
    public String toString() {
        return "IndexedPage [url=" + url + "]";
    }
}
