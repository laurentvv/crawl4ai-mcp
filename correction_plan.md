# Plan de Correction & Bilan du Crawl `docs.z.ai`

Suite à l'exécution de notre test d'intégration sur l'URL `https://docs.z.ai/devpack/overview` (avec une profondeur `max_depth = 2`), nous avons récupéré et analysé 121 pages avec succès.

Voici le constat de la qualité du fichier Markdown récupéré ainsi que les propositions de correction/amélioration.

## 1. Bilan de la qualité du fichier Markdown extrait

### Points Positifs (✅)
- **Quantité des pages et navigation** : Le crawler identifie très bien les liens du menu latéral (Claude Code, Cline, OpenCode, Kilo Code, Roo Code, etc.). Les 121 pages capturées montrent que l'exploration en profondeur fonctionne bien.
- **Récupération du contenu** : Le texte principal de la page `overview` et des autres pages est correctement extrait. On y trouve bien les descriptions des offres (Lite Plan, Pro Plan, Max Plan) et les modèles supportés (GLM-5.1, GLM-5-Turbo, etc.).
- **Nettoyage basique** : Les informations liées au code source et aux scripts semblent expurgées.

### Défauts constatés (❌ - Bruit et structure)
En observant les 200 premières lignes de la page extraite, on note la présence d'éléments superflus qui altèrent la lisibilité (bruit de navigation) :
- **Bruit du Header / Search / Footer** :
  - `Skip to main content`
  - `English`
  - `Search... Ctrl K`
  - `API Keys / Payment Method`
  - Le footer répétitif (`xgithubdiscordlinkedin Powered byThis documentation is built and hosted on Mintlify...`).
- **Bruit du Menu Latéral (Navigation)** :
  - Le crawler extrait le menu en tant que contenu textuel (`Navigation GLM Coding Plan Overview GuidesAPI ReferenceScenario...`), et ce, de manière répétitive sur chaque page.
- **Artefacts de UI / Boutons** :
  - `Copy page` qui apparaît en double (`Copy page \n Copy page`).
  - `Was this page helpful? YesNo`
  - `Ctrl+I`
- **Caractères d'espacement et balises de structuration redondantes** :
  - Présence de titres vides ou de puces non pertinentes (`## \n​\n### \n​\n`).

---

## 2. Plan d'Action & Propositions de Corrections

Afin d'obtenir un Markdown plus propre (qui sera bien plus performant si ces données sont ingérées par un LLM dans un workflow MCP), voici les étapes de correction à implémenter :

### Action A : Ciblage intelligent du contenu (Wait For Selector / Main Element)
La documentation de Z.AI utilise probablement Mintlify (comme indiqué dans le footer). Dans ces outils, le contenu pertinent est toujours encapsulé dans un bloc sémantique comme `<main>`, `<article>`, ou des identifiants spécifiques (`#content`, `.prose`).
- **Correction** : Lors de l'appel à `crawl4ai` dans notre MCP, nous devons cibler le contenu principal pour ignorer les `navbar`, `sidebar` et `footer`.
- **Implémentation** : Paramétrer le crawler pour qu'il privilégie l'extraction du bloc central, par exemple en utilisant un paramètre `css_selector="main"` ou `article`.

### Action B : Post-processing et nettoyage par expressions régulières (Regex)
Dans le fichier `src/crawl4ai_mcp/__init__.py`, on peut enrichir la logique de nettoyage (`_format_markdown_page` ou équivalent) pour supprimer automatiquement :
- Les patterns exacts liés à Mintlify ou aux documentations standards :
  - `Skip to main content`
  - `Was this page helpful\? YesNo`
  - `Copy page\nCopy page`
  - `Powered byThis documentation is built and hosted on Mintlify`
- **Implémentation** : Ajouter une liste de "stop-words/phrases" UI à purger du rendu final avant l'écriture dans le fichier `.md`.

### Action C : Nettoyage des balises Markdown vides
Les artefacts comme `## \n​\n` proviennent d'ancres ou de titres sans texte.
- **Correction** : Ajouter un filtre pour supprimer les lignes contenant uniquement des balises `## ` suivies de caractères invisibles ou d'espaces.

### Action D : Gestion des erreurs de navigation (Playwright)
Pendant le test, la page `https://z.ai/manage-apikey/rate-limits` a échoué avec l'erreur : `Unable to retrieve content because the page is navigating and changing the content`.
- **Correction** : Augmenter la robustesse du crawler face aux redirections ou implémenter un "wait_for_timeout" ou "wait_until='networkidle'" pour Playwright lorsque le crawler de base remonte cette exception.

---

### Résumé de la stratégie :
1. **Patcher `_format_markdown_page`** : pour retirer le bruit (les phrases UI en dur).
2. **Utiliser un sélecteur sémantique (si possible via crawl4ai)** : pour ignorer le layout global.
3. **Patcher la robustesse Playwright** : pour éviter que des pages plantent en cours de chargement/redirection.
