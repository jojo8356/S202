
package search_engine;

import search_engine.IndexedPage;

public class SearchEngineTests {
    public static void main(String[] args) {
        String[] lines = {
            "https://site.com",
            "java:3",
            "moteur:2"
        };

        IndexedPage page = new IndexedPage(lines);
        page.afficher();
    }
}