# Web Crawler MCP

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Un outil de web crawling puissant qui s'intègre avec les assistants IA via le protocole MCP (Machine Conversation Protocol). Ce projet permet de crawler des sites web et d'enregistrer leur contenu sous forme de fichiers Markdown structurés.

## 📋 Fonctionnalités

- Crawling de sites web avec profondeur configurable
- Support des liens internes et externes
- Génération de fichiers Markdown structurés
- Intégration native avec les assistants IA via MCP
- Statistiques détaillées des résultats de crawl
- Gestion des erreurs et des pages non trouvées

## 🚀 Installation

### Prérequis

- Python 3.13 ou supérieur
- pip (gestionnaire de packages Python)

### Étapes d'installation

1. Clonez ce dépôt :

```bash
git clone laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Créez un environnement virtuel et activez-le :

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python -m venv .venv
source .venv/bin/activate
```

3. Installez les dépendances requises :

```bash
pip install -r requirements.txt
```

## 🔧 Configuration

### Configuration MCP pour les assistants IA

Pour utiliser ce crawler avec des assistants IA comme VScode Cline, configurez votre fichier `cline_mcp_settings.json` :

```json
{
  "mcpServers": {
    "crawl": {
      "command": "CHEMIN\\VERS\\VOTRE\\ENVIRONNEMENT\\.venv\\Scripts\\python.exe",
      "args": [
        "CHEMIN\\VERS\\VOTRE\\PROJET\\crawl_mcp.py"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

Remplacez `CHEMIN\\VERS\\VOTRE\\ENVIRONNEMENT` et `CHEMIN\\VERS\\VOTRE\\PROJET` par les chemins appropriés sur votre système.

#### Exemple concret (Windows)

```json
{
  "mcpServers": {
    "crawl": {
      "command": "C:\\Python\\crawl4ai-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\Python\\crawl4ai-mcp\\crawl_mcp.py"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

## 🖥️ Utilisation

### Utilisation avec un assistant IA (via MCP)

Une fois configuré dans votre assistant IA, vous pouvez utiliser le crawler en demandant à l'assistant d'effectuer un crawl avec la syntaxe suivante :

```
Pouvez-vous crawler le site web https://exemple.com avec une profondeur de 2 ?
```

L'assistant utilisera le protocole MCP pour exécuter l'outil de crawling avec les paramètres spécifiés.

### Exemples d'utilisation avec Claude

Voici des exemples de requêtes que vous pouvez faire à Claude après avoir configuré l'outil MCP :

- **Crawl simple** : "Peux-tu crawler le site example.com et m'en donner un résumé ?"
- **Crawl avec options** : "Peux-tu crawler https://example.com avec une profondeur de 3 et en incluant les liens externes ?"
- **Crawl avec sortie personnalisée** : "Peux-tu crawler le blog example.com et enregistrer les résultats dans un fichier nommé 'analyse_blog.md' ?"

## 📁 Structure des résultats

Les résultats du crawl sont enregistrés dans le dossier `crawl_results` à la racine du projet. Chaque fichier de résultat est au format Markdown avec la structure suivante :

```markdown
# https://example.com/page

## Métadonnées
- Profondeur : 1
- Horodatage : 2023-07-01T12:34:56

## Contenu
Contenu extrait de la page...

---
```

## 🛠️ Paramètres disponibles

L'outil de crawl accepte les paramètres suivants :

| Paramètre | Type | Description | Valeur par défaut |
|-----------|------|-------------|-------------------|
| url | string | URL à crawler (obligatoire) | - |
| max_depth | integer | Profondeur maximale de crawling | 2 |
| include_external | boolean | Inclure les liens externes | false |
| verbose | boolean | Activer les sorties détaillées | true |
| output_file | string | Chemin du fichier de sortie | généré automatiquement |

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
