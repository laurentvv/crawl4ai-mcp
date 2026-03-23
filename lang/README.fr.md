# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Un puissant outil de crawl Web qui s'intègre aux assistants IA via le MCP (Model Context Protocol). Ce projet permet aux assistants IA de parcourir des sites Web, d'extraire du contenu dynamique, de naviguer via des liens et d'enregistrer directement des fichiers Markdown structurés.

## 📋 Fonctionnalités

- Intégration native avec les assistants IA via MCP
- Renvoie le contenu Markdown extrait directement à l'IA
- Extrait et affiche les liens internes/externes pour la navigation de l'IA
- Attend les sélecteurs CSS dynamiques avant l'extraction (support SPA)
- Crawl de sites Web avec profondeur configurable
- Statistiques détaillées des résultats du crawl
- Gestion des erreurs et des pages non trouvées

## 🚀 Configuration MCP

Le moyen le plus simple et recommandé d'utiliser cet outil est via `uvx`, qui télécharge et exécute automatiquement la dernière version depuis GitHub sans vous obliger à cloner le dépôt manuellement.

### Prérequis

- [uv](https://github.com/astral-sh/uv) installé sur votre système.

### Configuration pour les assistants IA (ex: Claude Desktop, Cline)

Ajoutez ce qui suit au fichier de configuration MCP de votre assistant IA (ex: `cline_mcp_settings.json` ou `claude_desktop_config.json`) :

> **Note pour les utilisateurs Windows** : Il est fortement recommandé de spécifier `--python 3.12` pour éviter les problèmes de compilation avec certaines dépendances.

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uvx",
      "args": [
        "--python",
        "3.12",
        "--from",
        "git+https://github.com/laurentvv/crawl4ai-mcp",
        "crawl4ai-mcp"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

### Important : Installation du navigateur

Le crawler utilise Playwright pour gérer le contenu dynamique. Vous devez installer les navigateurs requis après avoir configuré l'outil :

```bash
uv run playwright install chromium
```

## 🖥️ Utilisation

Une fois configuré, vous pouvez utiliser le crawler en demandant à votre assistant IA d'effectuer un crawl.

### Exemples d'utilisation avec Claude/Cline

- **Crawl simple** : "Peux-tu crawler le site example.com et me donner un résumé ?"
- **Crawl avec options** : "Peux-tu crawler https://example.com avec une profondeur de 3 et inclure les liens externes ?"
- **Contenu dynamique** : "Crawle cette application React et attends que le sélecteur `.main-content` soit chargé."

## 🛠️ Paramètres disponibles (Outil MCP)

L'outil `crawl` accepte les paramètres suivants :

| Paramètre | Type | Description | Valeur par défaut |
|-----------|------|-------------|-------------------|
| `url` | string | URL à crawler (requis) | - |
| `max_depth` | integer | Profondeur maximale de crawl | 2 |
| `include_external` | boolean | Inclure les liens externes | false |
| `verbose` | boolean | Activer la sortie détaillée | true |
| `wait_for_selector` | string | Sélecteur CSS à attendre avant d'extraire le contenu. Utile pour les applications monopages (SPA). | None |
| `return_content` | boolean | S'il faut renvoyer le contenu extrait directement dans la réponse MCP (tronqué à 50k caractères si nécessaire). | true |
| `output_file` | string | Chemin du fichier de sortie | généré automatiquement |

## 👨‍💻 Développement

Si vous souhaitez modifier le crawler ou l'exécuter localement :

1. Clonez ce dépôt :
```bash
git clone https://github.com/laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Installez les dépendances avec `uv` :
```bash
uv sync
```

3. Lancez le serveur MCP directement :
```bash
uv run crawl4ai-mcp
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir un ticket ou à soumettre une pull request.

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
