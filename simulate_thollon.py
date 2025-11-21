from src.supabase_data_retriever import SupabaseDataRetriever
import pandas as pd

# Paramètres simulés (Thollon)
# Coordonnées approx de l'adresse
lat = 46.3913
lon = 6.7024
surface = 160
type_bien = "Maison"
rayon_km = 3
annees = 3
limit = 100 # Valeur mise à jour

print(f"Simulation recherche: Lat={lat}, Lon={lon}, Surf={surface}, Rayon={rayon_km}km, Limit={limit}")

retriever = SupabaseDataRetriever()
df = retriever.get_comparables(
    latitude=lat,
    longitude=lon,
    type_bien=type_bien,
    surface_min=surface * 0.8, # Tolerance 20%
    surface_max=surface * 1.2,
    rayon_km=rayon_km,
    annees=annees,
    limit=limit
)

print(f"Nombre de résultats trouvés : {len(df)}")

if len(df) > 0:
    # Vérifier type de sbati
    # print(df.dtypes)
    
    try:
        # Chercher la maison de 160m2
        found = df[ (df['sbati'] >= 159) & (df['sbati'] <= 161) ]
        
        if not found.empty:
            print("\n✅ MAISON DE 160m² TROUVÉE DANS LE DATAFRAME :")
            cols_to_show = ['datemut', 'valeurfonc', 'sbati', 'distance_km']
            if 'nb_pieces' in found.columns: cols_to_show.append('nb_pieces')
            if 'nblocmut' in found.columns: cols_to_show.append('nblocmut')
            
            print(found[cols_to_show])
            
            # Vérifier les colonnes de pièces si présentes
            cols = [c for c in df.columns if 'nb' in c or 'pp' in c]
            print(f"\nColonnes de pièces disponibles : {cols}")
            if cols:
                print(found[cols].iloc[0])
        else:
            print("\n❌ Maison de 160m² NON trouvée dans les résultats.")
            print("Top 5 résultats les plus proches :")
            print(df[['datemut', 'valeurfonc', 'sbati', 'distance_km']].head(5))
    except Exception as e:
        print(f"Erreur lors du filtrage : {e}")
        print(df.head())
else:
    print("❌ Aucun résultat trouvé.")
