"""
Script pour extraire les Epics et User Stories depuis le PRD Notion
basé sur la structure détectée dans la section Navigation
"""
import json
import re
from typing import Dict, List, Any


def parse_prd_structure(file_path: str) -> Dict[str, Any]:
    """
    Parse le fichier PRD pour extraire les Epics et User Stories
    basé sur la structure visible dans la section Navigation
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    structure = {
        "project_name": "Estimateur Immobilier Automatise v1.0",
        "mission": "Reduire le temps de production des estimations immobilieres de 50% en automatisant la collecte, l'analyse et le calcul de 4 methodes d'estimation complementaires",
        "epics": []
    }

    # Extraction des informations de navigation (lignes 10-21)
    lines = content.split("\n")

    # Détecter les Epics
    epic_pattern = re.compile(r"^\s*\d+\.\s+Epic\s+(\d+)\s*:\s*(.+?)\s*-\s*(\d+)\s*pts\s*-\s*(Phase\s+\d+)", re.IGNORECASE)
    us_section_found = False
    current_sprint = None

    for line in lines:
        # Détecter les Epics
        epic_match = epic_pattern.match(line)
        if epic_match:
            epic_num = epic_match.group(1)
            epic_name = epic_match.group(2).strip()
            epic_points = int(epic_match.group(3))
            epic_phase = epic_match.group(4)

            epic = {
                "id": int(epic_num),
                "name": epic_name,
                "story_points": epic_points,
                "phase": epic_phase,
                "description": "",
                "user_stories": []
            }

            # Enrichir la description selon l'Epic
            if "Comparables Vendues" in epic_name or "DVF+" in epic_name:
                epic["description"] = "Analyser les transactions passees similaires au bien estime. Calcul automatique score similarite, filtrage manuel, selection checkbox, metriques calculees (mediane, prix/m2, boxplot). Carte interactive avec Street View."
                epic["onglet"] = "Onglet 1"
            elif "Comparables en Vente" in epic_name or "Perplexity" in epic_name:
                epic["description"] = "Analyser les annonces actuelles du marche. Scan web via API Perplexity (SeLoger, LeBonCoin, etc.). Filtrage manuel, selection, metriques."
                epic["onglet"] = "Onglet 2"
            elif "Additionnelle" in epic_name or "Maisons" in epic_name:
                epic["description"] = "Calculer valeur terrain + cout construction + ajustements. Automatisation Perplexity pour recherche prix/m2 terrain et cout construction neuf dans la zone."
                epic["onglet"] = "Onglet 3"
            elif "Locative" in epic_name or "Appartements" in epic_name:
                epic["description"] = "Calculer valeur basee sur rendement locatif. Automatisation Perplexity pour recherche taux de rendement espere."
                epic["onglet"] = "Onglet 4"
            elif "Synthese" in epic_name or "Ponderation" in epic_name:
                epic["description"] = "Agreger les 4 methodes avec ponderation ajustable. Logique conditionnelle Maisons vs Appartements. Graphique comparatif horizontal."
                epic["onglet"] = "Onglet 5"

            structure["epics"].append(epic)

        # Détecter les User Stories (lignes 16-21)
        if "User Stories" in line or "Sprint" in line:
            us_section_found = True

        if us_section_found and "Sprint" in line:
            sprint_match = re.search(r"Sprint\s+(\d+)", line)
            if sprint_match:
                current_sprint = int(sprint_match.group(1))

            # Extraire les User Stories de cette ligne
            us_pattern = re.compile(r"US(\d+)\s*:\s*([^•]+)")
            for us_match in us_pattern.finditer(line):
                us_num = int(us_match.group(1))
                us_title = us_match.group(2).strip()

                # Déterminer à quel Epic appartient cette US
                epic_id = determine_epic_for_us(us_num)
                epic = next((e for e in structure["epics"] if e["id"] == epic_id), None)

                if epic:
                    us = {
                        "id": us_num,
                        "title": us_title,
                        "sprint": current_sprint,
                        "acceptance_criteria": [],
                        "priority": "Must Have" if us_num <= 7 else "Should Have",
                        "effort": estimate_effort(us_num)
                    }

                    # Enrichir avec critères d'acceptation basés sur le PRD
                    us["acceptance_criteria"] = get_acceptance_criteria_for_us(us_num, us_title)

                    epic["user_stories"].append(us)

    return structure


def determine_epic_for_us(us_id: int) -> int:
    """Détermine l'Epic auquel appartient une User Story"""
    # Mapping basé sur la lecture du PRD
    if us_id in [1, 2, 3, 4, 5, 6, 7]:
        return 1  # Epic 1: Comparables Vendues (DVF+)
    elif us_id in [8, 9]:
        return 2  # Epic 2: Comparables en Vente (Perplexity)
    elif us_id == 10:
        return 3  # Epic 3: Méthode Additionnelle (Maisons)
    elif us_id == 11:
        return 4  # Epic 4: Méthode Locative (Appartements)
    elif us_id in [12, 13]:
        return 5  # Epic 5: Synthèse et Pondération
    return 1


def estimate_effort(us_id: int) -> str:
    """Estime l'effort pour une User Story"""
    effort_map = {
        1: "3 SP",
        2: "5 SP",
        3: "3 SP",
        4: "2 SP",
        5: "3 SP",
        6: "2 SP",
        7: "3 SP",
        8: "5 SP",
        9: "8 SP",
        10: "8 SP",
        11: "5 SP",
        12: "5 SP",
        13: "8 SP"
    }
    return effort_map.get(us_id, "3 SP")


def get_acceptance_criteria_for_us(us_id: int, title: str) -> List[str]:
    """Retourne les critères d'acceptation basés sur le PRD"""
    criteria_map = {
        1: [
            "Formulaire contient tous les champs obligatoires (adresse, type bien, surface, pieces, DPE)",
            "Geocodage automatique via API Adresse Etalab fonctionnel",
            "Champs conditionnels apparaissent selon type bien (terrain pour Maison)",
            "Validation des champs obligatoires avant calcul",
            "Donnees stockees dans session_state pour utilisation dans autres onglets"
        ],
        2: [
            "Algorithme calcule score similarite base sur ponderation definie (surface 25%, pieces 15%, DPE 15%, distance 20%, anciennete 10%, type bien 15%)",
            "Top 30 comparables affiches dans tableau avec toutes colonnes requises",
            "Scores de similarite affiches en pourcentage (0-100%)",
            "Calcul < 3 secondes pour recherche dans rayon 10km",
            "Donnees DVF+ correctement recuperees depuis Supabase"
        ],
        3: [
            "Carte interactive Folium affichee au-dessus du tableau",
            "Marqueur rouge pour bien a estimer + points colores pour comparables (gradient selon similarite)",
            "Clic sur marqueur ouvre panneau avec Street View + details bien",
            "Carte centre automatiquement sur bien a estimer",
            "Performance: chargement carte < 2 secondes"
        ],
        4: [
            "Integration Google Street View API fonctionnelle",
            "Photo Street View affichee au clic sur marqueur",
            "Fallback si Street View indisponible (message + photo generique)",
            "Panneau affiche adresse, prix, surface, date, score",
            "Budget API Google Maps respecte (200 euros/mois max)"
        ],
        5: [
            "Sliders pour rayon km (1-20km), annees (1-10 ans), similarite min (0-100%)",
            "Filtrage temps reel du tableau selon criteres",
            "Nombre de resultats mis a jour dynamiquement",
            "Performance: filtrage < 1 seconde",
            "Valeurs par defaut pertinentes (rayon 5km, 5 ans, 50% similarite)"
        ],
        6: [
            "Checkbox pour chaque ligne du tableau",
            "Selection multiple possible (5-7 biens recommandes)",
            "Calcul automatique metriques: mediane, prix/m2, boxplot Plotly",
            "Metriques mis a jour en temps reel lors selection/deselection",
            "Validation: minimum 3 biens selectionnes pour calcul valide"
        ],
        7: [
            "Colonne prix ajuste affichee dans tableau avec formule basee sur taux emprunt historique",
            "Source donnees taux emprunt Banque de France identifiee et integree",
            "Calcul ajustement pouvoir achat correct (variation selon annee transaction)",
            "Explication formule disponible (tooltip ou note)",
            "Valeurs ajustees utilisees dans calculs metriques"
        ],
        8: [
            "Integration API Perplexity fonctionnelle pour scan annonces web",
            "Prompt structure pour recherche annonces similaires au bien",
            "Output JSON structure avec adresse, prix, surface, URL annonce",
            "Gestion erreurs API (retry, fallback, messages utilisateur)",
            "Budget API Perplexity respecte"
        ],
        9: [
            "Onglet 2 reprend pattern Onglet 1: carte + tableau + filtres + selection",
            "Donnees Perplexity affichees dans tableau avec colonnes identiques",
            "Carte avec points verts pour biens en vente",
            "Filtres fonctionnels (rayon, prix, surface)",
            "Selection checkbox + calcul metriques identique Onglet 1"
        ],
        10: [
            "API Perplexity recherche prix/m2 terrain et cout construction neuf dans zone",
            "Champs auto-remplies avec valeurs recherchees",
            "Sliders ajustement coefficients vetuste et environnement",
            "Calcul valeur brute et ajustee affiche en temps reel",
            "Formule detaillee visible pour transparence"
        ],
        11: [
            "Input loyer mensuel fonctionnel",
            "API Perplexity recherche taux rendement espere pour type bien + commune",
            "Affichage 3 scenarios: prudent, moyen, optimiste",
            "Calcul valeur bien pour chaque scenario (Loyer annuel / Taux rendement)",
            "Validation: taux rendement coherents (2-8%)"
        ],
        12: [
            "Affichage des 3-4 valeurs calculees selon type bien",
            "Sliders % pour chaque methode avec contrainte total = 100%",
            "Logique conditionnelle Maisons vs Appartements (methodes actives/desactivees)",
            "Calcul estimation finale ponderee en temps reel",
            "Valeurs par defaut: 50% vendus, 30% vente, 20% additionnelle/locative"
        ],
        13: [
            "Graphique Plotly horizontal avec tous biens retenus (onglets 1+2)",
            "Code couleur: bleu pour vendus, vert pour en vente",
            "Lignes medianes affichees pour detecter surestimation/sous-estimation",
            "Graphique interactif (zoom, hover details)",
            "Performance: generation graphique < 2 secondes"
        ]
    }
    return criteria_map.get(us_id, ["Criteres d'acceptation a definir"])


def format_structure_to_markdown(structure: Dict[str, Any]) -> str:
    """Formate la structure en Markdown detaille"""
    output = [f"# {structure['project_name']}\n"]
    output.append(f"\n**Mission:** {structure['mission']}\n")
    output.append(f"\n**Total Epics:** {len(structure['epics'])}\n")

    total_sp = sum(epic['story_points'] for epic in structure['epics'])
    total_us = sum(len(epic['user_stories']) for epic in structure['epics'])
    output.append(f"**Total Story Points:** {total_sp}\n")
    output.append(f"**Total User Stories:** {total_us}\n")

    output.append("\n---\n")

    for epic in structure['epics']:
        output.append(f"\n## Epic {epic['id']}: {epic['name']}\n")
        output.append(f"\n**Story Points:** {epic['story_points']} | **Phase:** {epic['phase']} | **Onglet:** {epic.get('onglet', 'N/A')}\n")
        output.append(f"\n**Description:**\n{epic['description']}\n")

        if epic['user_stories']:
            output.append(f"\n**User Stories ({len(epic['user_stories'])}):**\n")

            for us in epic['user_stories']:
                output.append(f"\n### US-{us['id']}: {us['title']}\n")
                output.append(f"\n**Sprint:** {us['sprint']} | **Priorite:** {us['priority']} | **Effort:** {us['effort']}\n")

                if us['acceptance_criteria']:
                    output.append("\n**Criteres d'acceptation:**\n")
                    for idx, criteria in enumerate(us['acceptance_criteria'], 1):
                        output.append(f"{idx}. {criteria}\n")

                output.append("\n")

        output.append("\n---\n")

    return "".join(output)


def main():
    """Point d'entree principal"""
    print("Extraction structure EPIC/US depuis PRD Notion...\n")

    input_file = "c:\\Users\\jbcho\\Estimation-immo-1\\docs\\NOTION_PRD_RAW.md"
    output_md = "c:\\Users\\jbcho\\Estimation-immo-1\\docs\\EPICS_USER_STORIES.md"
    output_json = "c:\\Users\\jbcho\\Estimation-immo-1\\docs\\EPICS_USER_STORIES.json"

    # Parse structure
    print("Parsing du fichier PRD...")
    structure = parse_prd_structure(input_file)

    # Sauvegarde JSON
    print(f"Sauvegarde structure JSON: {output_json}")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

    # Sauvegarde Markdown
    print(f"Sauvegarde structure Markdown: {output_md}")
    markdown = format_structure_to_markdown(structure)
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(markdown)

    # Resume
    print("\n" + "="*60)
    print("Extraction terminee!")
    print("="*60)
    print(f"\nResume:")
    print(f"  - {len(structure['epics'])} Epics")
    print(f"  - {sum(len(e['user_stories']) for e in structure['epics'])} User Stories")
    print(f"  - {sum(e['story_points'] for e in structure['epics'])} Story Points total")

    print("\nDetail par Epic:")
    for epic in structure['epics']:
        print(f"  Epic {epic['id']}: {epic['name']}")
        print(f"    - {len(epic['user_stories'])} US, {epic['story_points']} SP, {epic['phase']}")


if __name__ == "__main__":
    main()
