"""
Script pour synchroniser le contenu Notion PRD vers documentation locale
"""
import os
import json
from typing import Dict, List, Any

# Installation requise: pip install notion-client
try:
    from notion_client import Client
except ImportError:
    print("⚠️  notion-client non installé. Exécutez: pip install notion-client")
    exit(1)


NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
PAGE_URL = "https://www.notion.so/Automatisation-des-estimations-2fc6cfd339504d1bbf444c0ae078ff5c"
# Extraction de l'ID de page depuis l'URL
PAGE_ID = "2fc6cfd339504d1bbf444c0ae078ff5c"


def init_notion_client() -> Client:
    """Initialise le client Notion"""
    return Client(auth=NOTION_TOKEN)


def extract_text_from_block(block: Dict[str, Any]) -> str:
    """Extrait le texte d'un block Notion"""
    block_type = block.get("type")

    if not block_type:
        return ""

    content = block.get(block_type, {})

    if "rich_text" in content:
        return "".join([text.get("plain_text", "") for text in content["rich_text"]])
    elif "text" in content:
        return "".join([text.get("plain_text", "") for text in content["text"]])
    elif "title" in content:
        return "".join([text.get("plain_text", "") for text in content["title"]])

    return ""


def get_page_content(client: Client, page_id: str) -> Dict[str, Any]:
    """Récupère le contenu d'une page Notion"""
    try:
        page = client.pages.retrieve(page_id=page_id)
        return page
    except Exception as e:
        print(f"ERREUR lors de la recuperation de la page: {e}")
        return {}


def get_page_blocks(client: Client, page_id: str) -> List[Dict[str, Any]]:
    """Récupère tous les blocks d'une page"""
    blocks = []
    try:
        response = client.blocks.children.list(block_id=page_id)
        blocks.extend(response.get("results", []))

        # Pagination
        while response.get("has_more"):
            response = client.blocks.children.list(
                block_id=page_id,
                start_cursor=response.get("next_cursor")
            )
            blocks.extend(response.get("results", []))

        return blocks
    except Exception as e:
        print(f"ERREUR lors de la recuperation des blocks: {e}")
        return []


def parse_blocks_to_markdown(client: Client, blocks: List[Dict[str, Any]], level: int = 0) -> str:
    """Convertit les blocks Notion en Markdown"""
    markdown = []
    indent = "  " * level

    for block in blocks:
        block_type = block.get("type")
        text = extract_text_from_block(block)

        if block_type == "heading_1":
            markdown.append(f"\n# {text}\n")
        elif block_type == "heading_2":
            markdown.append(f"\n## {text}\n")
        elif block_type == "heading_3":
            markdown.append(f"\n### {text}\n")
        elif block_type == "paragraph":
            if text.strip():
                markdown.append(f"{indent}{text}\n")
        elif block_type == "bulleted_list_item":
            markdown.append(f"{indent}- {text}\n")
        elif block_type == "numbered_list_item":
            markdown.append(f"{indent}1. {text}\n")
        elif block_type == "toggle":
            markdown.append(f"{indent}<details>\n{indent}<summary>{text}</summary>\n")
            if block.get("has_children"):
                children = get_page_blocks(client, block["id"])
                markdown.append(parse_blocks_to_markdown(client, children, level + 1))
            markdown.append(f"{indent}</details>\n")
        elif block_type == "code":
            language = block.get("code", {}).get("language", "")
            markdown.append(f"\n```{language}\n{text}\n```\n")
        elif block_type == "divider":
            markdown.append("\n---\n")
        elif block_type == "callout":
            icon = block.get("callout", {}).get("icon", {})
            emoji = icon.get("emoji", "[!]") if icon.get("type") == "emoji" else "[!]"
            markdown.append(f"\n> {emoji} {text}\n")
        elif block_type == "quote":
            markdown.append(f"\n> {text}\n")

        # Récupérer les enfants si présents
        if block.get("has_children") and block_type not in ["toggle"]:
            children = get_page_blocks(client, block["id"])
            markdown.append(parse_blocks_to_markdown(client, children, level + 1))

    return "".join(markdown)


def extract_epics_and_stories(content: str) -> Dict[str, Any]:
    """
    Parse le contenu Markdown pour extraire la structure EPIC/User Stories
    """
    lines = content.split("\n")
    structure = {
        "epics": []
    }

    current_epic = None
    current_us = None

    for line in lines:
        line_stripped = line.strip()

        # Détection d'EPIC
        if "EPIC" in line_stripped.upper() and line_stripped.startswith("#"):
            if current_epic:
                structure["epics"].append(current_epic)

            current_epic = {
                "name": line_stripped.lstrip("#").strip(),
                "description": "",
                "user_stories": []
            }
            current_us = None

        # Détection User Story
        elif ("US-" in line_stripped.upper() or "USER STORY" in line_stripped.upper()) and line_stripped.startswith("#"):
            if current_epic is None:
                current_epic = {
                    "name": "EPIC par défaut",
                    "description": "",
                    "user_stories": []
                }

            if current_us:
                current_epic["user_stories"].append(current_us)

            current_us = {
                "title": line_stripped.lstrip("#").strip(),
                "description": "",
                "acceptance_criteria": [],
                "priority": "",
                "effort": ""
            }

        # Accumulation de contenu
        elif current_us:
            if "critère" in line_stripped.lower() or "acceptance" in line_stripped.lower():
                current_us["acceptance_criteria"].append(line_stripped)
            elif "priorité" in line_stripped.lower() or "priority" in line_stripped.lower():
                current_us["priority"] = line_stripped
            elif "effort" in line_stripped.lower() or "estimation" in line_stripped.lower():
                current_us["effort"] = line_stripped
            else:
                current_us["description"] += line + "\n"
        elif current_epic:
            current_epic["description"] += line + "\n"

    # Ajouter les derniers éléments
    if current_us and current_epic:
        current_epic["user_stories"].append(current_us)
    if current_epic:
        structure["epics"].append(current_epic)

    return structure


def format_output(structure: Dict[str, Any]) -> str:
    """Formate la structure en Markdown lisible"""
    output = ["# Structure PRD - Estimation Immobilière\n"]

    for idx, epic in enumerate(structure["epics"], 1):
        output.append(f"\n## EPIC {idx}: {epic['name']}\n")
        output.append(f"{epic['description']}\n")

        for us_idx, us in enumerate(epic["user_stories"], 1):
            output.append(f"\n### US-{idx}.{us_idx}: {us['title']}\n")
            output.append(f"**Description:**\n{us['description']}\n")

            if us["acceptance_criteria"]:
                output.append("\n**Critères d'acceptation:**\n")
                for criteria in us["acceptance_criteria"]:
                    output.append(f"- {criteria}\n")

            if us["priority"]:
                output.append(f"\n**{us['priority']}**\n")

            if us["effort"]:
                output.append(f"\n**{us['effort']}**\n")

    return "".join(output)


def search_child_pages(client: Client, page_id: str) -> List[Dict[str, Any]]:
    """Recherche les pages enfants d'une page"""
    try:
        # Rechercher les blocks qui sont des pages enfants (child_page)
        blocks = get_page_blocks(client, page_id)
        child_pages = []

        for block in blocks:
            if block.get("type") == "child_page":
                child_id = block.get("id")
                child_title = extract_text_from_block(block)
                child_pages.append({
                    "id": child_id,
                    "title": child_title
                })

        return child_pages
    except Exception as e:
        print(f"ERREUR lors de la recherche de pages enfants: {e}")
        return []


def main():
    """Point d'entrée principal"""
    print("Synchronisation Notion -> Local\n")

    # 1. Initialiser le client
    print("Connexion a Notion...")
    client = init_notion_client()

    # 2. Récupérer la page principale
    print(f"Recuperation de la page principale {PAGE_ID}...")
    page = get_page_content(client, PAGE_ID)

    if not page:
        print("ERREUR: Impossible de recuperer la page")
        return

    # 3. Récupérer tous les blocks de la page principale
    print("Recuperation des blocks de la page principale...")
    blocks = get_page_blocks(client, PAGE_ID)
    print(f"   OK: {len(blocks)} blocks recuperes")

    # 4. Rechercher les pages enfants
    print("\nRecherche de pages enfants (Epics, User Stories)...")
    child_pages = search_child_pages(client, PAGE_ID)
    print(f"   OK: {len(child_pages)} page(s) enfant(s) trouvee(s)")

    for child in child_pages:
        print(f"      - {child['title']} (ID: {child['id']})")

    # 5. Convertir la page principale en Markdown
    print("\nConversion de la page principale en Markdown...")
    markdown_content = parse_blocks_to_markdown(client, blocks)

    # 6. Sauvegarder le contenu brut de la page principale
    raw_output_path = "c:\\Users\\jbcho\\Estimation-immo-1\\docs\\NOTION_PRD_RAW.md"
    with open(raw_output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"   OK: Contenu brut sauvegarde: {raw_output_path}")

    # 7. Récupérer et sauvegarder les pages enfants
    all_child_content = []
    for idx, child in enumerate(child_pages, 1):
        print(f"\nTraitement page enfant {idx}/{len(child_pages)}: {child['title']}...")
        child_blocks = get_page_blocks(client, child['id'])
        child_markdown = f"\n\n# {child['title']}\n\n"
        child_markdown += parse_blocks_to_markdown(client, child_blocks)
        all_child_content.append(child_markdown)

        # Sauvegarder chaque page enfant individuellement
        safe_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in child['title'])
        child_output_path = f"c:\\Users\\jbcho\\Estimation-immo-1\\docs\\NOTION_CHILD_{safe_filename}.md"
        with open(child_output_path, "w", encoding="utf-8") as f:
            f.write(child_markdown)
        print(f"   OK: Sauvegarde: {child_output_path}")

    # 8. Créer un document complet avec toutes les pages
    full_content = markdown_content + "\n\n" + "\n\n".join(all_child_content)
    full_output_path = "c:\\Users\\jbcho\\Estimation-immo-1\\docs\\NOTION_COMPLETE.md"
    with open(full_output_path, "w", encoding="utf-8") as f:
        f.write(full_content)
    print(f"\n   OK: Document complet sauvegarde: {full_output_path}")

    # 9. Extraire la structure EPIC/US du contenu complet
    print("\nExtraction de la structure EPIC/US...")
    structure = extract_epics_and_stories(full_content)

    # 10. Sauvegarder la structure JSON
    json_output_path = "c:\\Users\\jbcho\\Estimation-immo-1\\docs\\NOTION_PRD_STRUCTURE.json"
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    print(f"   OK: Structure JSON sauvegardee: {json_output_path}")

    # 11. Formater et sauvegarder le résultat final
    formatted_content = format_output(structure)
    final_output_path = "c:\\Users\\jbcho\\Estimation-immo-1\\docs\\NOTION_PRD_STRUCTURED.md"
    with open(final_output_path, "w", encoding="utf-8") as f:
        f.write(formatted_content)
    print(f"   OK: Structure formatee sauvegardee: {final_output_path}")

    # 12. Résumé
    print("\n" + "="*50)
    print("Synchronisation terminee!")
    print("="*50)
    print(f"\nResume:")
    print(f"   - Page principale: {len(blocks)} blocks")
    print(f"   - Pages enfants: {len(child_pages)}")
    print(f"   - EPIC(s) trouve(s): {len(structure['epics'])}")
    for epic in structure["epics"]:
        print(f"     * {epic['name']}: {len(epic['user_stories'])} User Story(ies)")


if __name__ == "__main__":
    main()
