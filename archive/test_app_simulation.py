"""
Test exact de ce que fait l'application Streamlit
"""
from src.utils.geocoding import geocode_address
from src.supabase_data_retriever import SupabaseDataRetriever

# Simuler exactement ce que fait l'app
address = "177 Rte de Leucy, 74500 Thollon-les-Mémises, France"
surface = 160
tolerance = 0.20  # 20%

print("="*70)
print("SIMULATION EXACTE DE L'APPLICATION STREAMLIT")
print("="*70)

# 1. Géocodage
print(f"\n1. Géocodage de: {address}")
suggestions = geocode_address(address)
if suggestions:
    geocoded = suggestions[0]
    print(f"   Résultat: {geocoded['formatted_address']}")
    print(f"   Latitude: {geocoded['latitude']}")
    print(f"   Longitude: {geocoded['longitude']}")
    
    # 2. Récupération comparables
    print(f"\n2. Récupération comparables avec:")
    surface_min = surface * (1 - tolerance)
    surface_max = surface * (1 + tolerance)
    print(f"   - Surface: {surface_min:.0f} - {surface_max:.0f} m²")
    print(f"   - Rayon: 3 km")
    print(f"   - Type: Maison")
    
    retriever = SupabaseDataRetriever()
    df = retriever.get_comparables(
        latitude=geocoded['latitude'],
        longitude=geocoded['longitude'],
        type_bien='Maison',
        surface_min=surface_min,
        surface_max=surface_max,
        rayon_km=3,
        annees=3,
        limit=50
    )
    
    print(f"\n3. Résultats: {len(df)} comparables trouvés")
    if len(df) > 0:
        print("\n   Premiers résultats:")
        print(df[['adresse', 'distance_km', 'sbati', 'valeurfonc']].head(10))
        
        # Vérifier si Thollon est présent
        thollon_results = df[df['adresse'].str.contains('Thollon', case=False, na=False)]
        print(f"\n   Comparables à Thollon-les-Mémises: {len(thollon_results)}")
        if len(thollon_results) > 0:
            print(thollon_results[['adresse', 'distance_km', 'sbati']])
    else:
        print("   ❌ AUCUN RÉSULTAT - C'EST LE PROBLÈME!")
else:
    print("   ❌ Échec du géocodage")

print("\n" + "="*70)
