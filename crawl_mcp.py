import io
import os
import re
import sys
import traceback
import urllib.parse
from datetime import datetime

import anyio
import click
import mcp.types as types
from mcp.server.lowlevel import Server

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy

# Configurer l'encodage UTF-8 pour toutes les sorties - Ce code reste utile
# Particulièrement sur Windows où l'encodage par défaut peut ne pas être UTF-8
# et pour garantir la cohérence du traitement des caractères internationaux
# lors du crawling de sites web multilingues
os.environ["PYTHONIOENCODING"] = "utf-8"
# Forcer l'utilisation de UTF-8 pour stdout/stderr
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Fonction améliorée pour sanitiser les textes avec remplacement explicite des caractères problématiques
def sanitize_text(text):
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    # Liste des remplacements explicites pour les caractères problématiques connus
    replacements = {
        "\u2192": "->",  # Flèche droite → devient ->
        "\u2190": "<-",  # Flèche gauche ← devient <-
        "\u2191": "^",  # Flèche haut ↑ devient ^
        "\u2193": "v",  # Flèche bas ↓ devient v
        "\u2022": "*",  # Puce • devient *
        "\u2013": "-",  # Tiret moyen – devient -
        "\u2014": "--",  # Tiret cadratin — devient --
        "\u2018": "'",  # Guillemet-apostrophe gauche ' devient '
        "\u2019": "'",  # Guillemet-apostrophe droit ' devient '
        "\u201c": '"',  # Guillemet double gauche " devient "
        "\u201d": '"',  # Guillemet double droit " devient "
        "\u2026": "...",  # Points de suspension … devient ...
        "\u00a0": " ",  # Espace insécable   devient espace normal
    }

    # Appliquer les remplacements explicites
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    # Éliminer tous les autres caractères non-ASCII qui pourraient causer des problèmes
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    return text


def generate_filename_from_url(url):
    """Génère un nom de fichier valide à partir d'une URL"""
    # Extraire le hostname et le chemin
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.netloc.replace(".", "_")

    # Ajouter un timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Créer le nom du fichier
    return f"crawl_{hostname}_{timestamp}.md"


def get_results_directory():
    """Retourne le chemin du répertoire pour stocker les résultats"""
    # Utiliser un dossier dans le projet plutôt que temp
    results_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "crawl_results"
    )

    # Créer le dossier s'il n'existe pas
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    return results_dir


async def crawl_website(
    url: str,
    max_depth: int = 2,
    include_external: bool = False,
    verbose: bool = True,
    output_file: str = None,
) -> dict:
    """
    Crawl un site web et enregistre les résultats dans un fichier

    Args:
        url: URL à crawler
        max_depth: Profondeur maximale de crawl
        include_external: Inclure les liens externes
        verbose: Afficher des informations détaillées
        output_file: Chemin du fichier de sortie (généré automatiquement si None)

    Returns:
        Un dictionnaire contenant le chemin du fichier et des statistiques
    """
    # Générer un nom de fichier si non spécifié
    if not output_file:
        # Utiliser le dossier du projet au lieu du dossier temporaire
        output_file = os.path.join(
            get_results_directory(), generate_filename_from_url(url)
        )

    if verbose:
        print(
            f"Crawling {url} (profondeur max: {max_depth}, inclure externes: {include_external})",
            file=sys.stderr,
        )
        print(f"Les résultats seront enregistrés dans: {output_file}", file=sys.stderr)

    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=max_depth,
            include_external=include_external,
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=verbose,
    )

    result_markdown = io.StringIO()
    stats = {
        "total_pages": 0,
        "successful_pages": 0,
        "failed_pages": 0,
        "not_found_pages": 0,  # Pages 404
        "forbidden_pages": 0,   # Nouvelle statistique pour les pages 403
        "start_time": datetime.now(),
    }

    try:
        async with AsyncWebCrawler(verbose=verbose) as crawler:
            # Ajouter un hook pour suivre la progression
            async def progress_callback(event_type, data):
                if event_type == "page_visit_start":
                    stats["total_pages"] += 1
                    if verbose:
                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] Visite de: {data['url']} (page {stats['total_pages']})",
                            file=sys.stderr,
                        )
                elif event_type == "page_visit_complete":
                    if data.get("success", False):
                        stats["successful_pages"] += 1
                    else:
                        stats["failed_pages"] += 1

                    if verbose:
                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] Terminé: {data['url']} (succès: {stats['successful_pages']}, échecs: {stats['failed_pages']})",
                            file=sys.stderr,
                        )

            # Ajouter le callback à notre configuration
            config.progress_callback = progress_callback

            try:
                if verbose:
                    print(
                        f"Début du crawl à {datetime.now().strftime('%H:%M:%S')}",
                        file=sys.stderr,
                    )

                results = await crawler.arun(url, config=config)

                if verbose:
                    print(
                        f"Crawl terminé à {datetime.now().strftime('%H:%M:%S')} - {len(results)} pages traitées",
                        file=sys.stderr,
                    )
                    print("Génération du fichier markdown...", file=sys.stderr)

                # S'assurer que les statistiques sont cohérentes avec les résultats
                # Compter le nombre de pages ayant du contenu comme réussies
                stats["successful_pages"] = 0  # Réinitialiser pour compter correctement
                stats["not_found_pages"] = 0  # Réinitialiser le compteur de pages 404
                stats["forbidden_pages"] = 0  # Initialiser le compteur de pages 403

                for idx, result in enumerate(results):
                    try:
                        # Détecter les pages 404
                        if hasattr(result, "status_code") and result.status_code == 404:
                            stats["not_found_pages"] += 1
                            if verbose:
                                print(
                                    f"[{datetime.now().strftime('%H:%M:%S')}] Page non trouvée (404): {result.url}",
                                    file=sys.stderr,
                                )
                            continue
                            
                        # Détecter les pages 403
                        if hasattr(result, "status_code") and result.status_code == 403:
                            stats["forbidden_pages"] += 1
                            if verbose:
                                print(
                                    f"[{datetime.now().strftime('%H:%M:%S')}] Accès interdit (403): {result.url}",
                                    file=sys.stderr,
                                )
                            continue

                        text_for_output = getattr(result, "markdown", None) or getattr(
                            result, "text", None
                        )

                        # Vérifier si le contenu ressemble à une page 404 (contient "404 Not Found")
                        if text_for_output and "404 Not Found" in text_for_output:
                            stats["not_found_pages"] += 1
                            if verbose:
                                print(
                                    f"[{datetime.now().strftime('%H:%M:%S')}] Page non trouvée (contenu 404): {result.url}",
                                    file=sys.stderr,
                                )
                            continue
                            
                        # Vérifier si le contenu ressemble à une page 403 (contient "403 Forbidden")
                        if text_for_output and "403 Forbidden" in text_for_output:
                            stats["forbidden_pages"] += 1
                            if verbose:
                                print(
                                    f"[{datetime.now().strftime('%H:%M:%S')}] Accès interdit (contenu 403): {result.url}",
                                    file=sys.stderr,
                                )
                            continue

                        if not text_for_output:
                            continue

                        # Incrémenter le compteur de pages réussies
                        stats["successful_pages"] += 1

                        # Sanitiser tous les éléments qui seront écrits
                        safe_url = sanitize_text(result.url)
                        safe_depth = sanitize_text(
                            str(result.metadata.get("depth", "N/A"))
                        )
                        safe_timestamp = sanitize_text(datetime.now().isoformat())
                        safe_content = sanitize_text(text_for_output)

                        md_content = f"""
# {safe_url}

## Métadonnées
- Profondeur : {safe_depth}
- Horodatage : {safe_timestamp}

## Contenu
{safe_content}

---
"""
                        result_markdown.write(md_content)
                    except Exception as e:
                        print(
                            f"Erreur lors du traitement du résultat {idx}: {e}",
                            file=sys.stderr,
                        )
                        # Logger le contenu problématique pour diagnostic
                        if verbose:
                            print(
                                f"Caractères problématiques possibles dans: {result.url}",
                                file=sys.stderr,
                            )
            except Exception as e:
                print(f"Erreur pendant l'exécution du crawling: {e}", file=sys.stderr)
                return {
                    "error": f"Erreur de crawling: {str(e)}",
                    "file_path": None,
                    "stats": stats,
                }
    except Exception as e:
        print(f"Erreur lors de l'initialisation du crawler: {e}", file=sys.stderr)
        return {
            "error": f"Erreur d'initialisation: {str(e)}",
            "file_path": None,
            "stats": stats,
        }

    # Écrire le contenu dans le fichier spécifié
    try:
        content = result_markdown.getvalue()

        if verbose:
            print(
                f"Écriture des résultats dans le fichier: {output_file}",
                file=sys.stderr,
            )

        # Créer le dossier parent si nécessaire
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

        # Sanitiser et écrire le contenu
        with open(output_file, "w", encoding="utf-8", errors="replace") as f:
            safe_content = sanitize_text(content)
            f.write(safe_content)

        # Finaliser les stats
        stats["end_time"] = datetime.now()
        stats["duration_seconds"] = (
            stats["end_time"] - stats["start_time"]
        ).total_seconds()

        if verbose:
            print(
                f"Crawl terminé en {stats['duration_seconds']:.2f} secondes",
                file=sys.stderr,
            )
            print(
                f"Pages traitées: {stats['successful_pages']} réussies, {stats['failed_pages']} échouées, "
                f"{stats['not_found_pages']} non trouvées (404), {stats['forbidden_pages']} accès interdits (403)",
                file=sys.stderr,
            )
            print(f"Résultats enregistrés dans: {output_file}", file=sys.stderr)

        return {"file_path": output_file, "stats": stats, "error": None}
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return {
            "error": f"Erreur d'écriture: {str(e)}",
            "file_path": None,
            "stats": stats,
        }


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(port: int, transport: str) -> int:
    app = Server("mcp-web-crawler")

    @app.call_tool()
    async def crawl_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name != "crawl":
            raise ValueError(f"Unknown tool: {name}")
        if "url" not in arguments:
            raise ValueError("Missing required argument 'url'")

        max_depth = arguments.get("max_depth", 2)
        include_external = arguments.get("include_external", False)
        verbose = arguments.get("verbose", True)
        output_file = arguments.get("output_file", None)

        try:
            result = await crawl_website(
                arguments["url"],
                max_depth=max_depth,
                include_external=include_external,
                verbose=verbose,
                output_file=output_file,
            )

            if result["error"]:
                return [
                    types.TextContent(type="text", text=f"Erreur: {result['error']}")
                ]

            file_path = result["file_path"]
            stats = result["stats"]

            # Créer un message de résumé
            summary = f"""
## Crawl terminé avec succès
- URL: {arguments["url"]}
- Fichier de résultat: {file_path}
- Durée: {stats["duration_seconds"]:.2f} secondes
- Pages traitées: {stats["successful_pages"]} réussies, {stats["failed_pages"]} échouées, 
  {stats.get("not_found_pages", 0)} non trouvées (404), {stats.get("forbidden_pages", 0)} accès interdits (403)

Vous pouvez consulter les résultats dans le fichier: {file_path}
(Les résultats sont désormais stockés dans le dossier 'crawl_results' de votre projet)
            """

            return [types.TextContent(type="text", text=summary)]
        except Exception as e:
            print(f"Erreur dans crawl_tool: {e}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            return [
                types.TextContent(type="text", text=f"Erreur: {sanitize_text(str(e))}")
            ]

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="crawl",
                description="Crawls a website and saves its content as structured markdown to a file",
                inputSchema={
                    "type": "object",
                    "required": ["url"],
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to crawl",
                        },
                        "max_depth": {
                            "type": "integer",
                            "description": "Maximum crawling depth",
                            "default": 2,
                        },
                        "include_external": {
                            "type": "boolean",
                            "description": "Whether to include external links",
                            "default": False,
                        },
                        "verbose": {
                            "type": "boolean",
                            "description": "Enable verbose output",
                            "default": True,
                        },
                        "output_file": {
                            "type": "string",
                            "description": "Path to output file (generated if not provided)",
                            "default": None,
                        },
                    },
                },
            )
        ]

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request.send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="127.0.0.1", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erreur principale: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
