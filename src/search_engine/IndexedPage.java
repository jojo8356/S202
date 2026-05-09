package search_engine;

import java.util.Arrays;
import java.util.TreeMap;

public class IndexedPage {
    private String url;
    private String[] words;
    private int[] counts;

    // S1.3 - Constructeur depuis un tableau de lignes (fichier index)
    public IndexedPage(String[] lines) {
        if (lines == null || lines.length == 0) {
            throw new IllegalArgumentException("lines ne peut pas être vide");
        }

        url = lines[0];
        words = new String[lines.length - 1];
        counts = new int[lines.length - 1];

        for (int i = 1; i < lines.length; i++) {
            String[] parts = lines[i].split(":");
            words[i - 1] = parts[0];
            counts[i - 1] = Integer.parseInt(parts[1]);
        }
    }

    // S1.4 - Constructeur depuis un texte brut (requête)
    public IndexedPage(String text) {
        url = null;
        String[] tokens = text.split("\\s+");

        // On utilise une TreeMap pour compter et trier automatiquement
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

    // S1.5 - toString obligatoire (remplace afficher)
    public String toString() {
        return "IndexedPage [url=" + url + "]";
    }

    // Méthode afficher gardée pour tes tests perso
    public void afficher() {
        System.out.println("URL : " + url);
        for (int i = 0; i < words.length; i++) {
            System.out.println(words[i] + " : " + counts[i]);
        }
    }
}