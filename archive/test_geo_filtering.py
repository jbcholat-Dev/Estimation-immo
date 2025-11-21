"""
Script de diagnostic pour tester le filtrage géographique DVF
"""
from src.supabase_data_retriever import SupabaseDataRetriever
from sqlalchemy import text

r = SupabaseDataRetriever()

print("="*70)
print("DIAGNOSTIC: Problème de filtrage géographique DVF")
print("="*70)

# Coordonnées de Thollon-les-Mémises
thollon_lat = 46.3907
thollon_lon = 6.6970

print(f"\n1. Coordonnées de Thollon-les-Mémises: {thollon_lat}, {thollon_lon}")

# Test 1: Compter les maisons dans la base (sans filtre géo)
print("\n2. Test: Maisons 128-192m² dans toute la base (3 dernières années)")
with r.engine.connect() as conn:
    query = text("""
        SELECT COUNT(*) FROM dvf_plus_2025_2.dvf_plus_mutation
        WHERE sbati >= 128 AND sbati <= 192
          AND valeurfonc > 0
          AND libtypbien LIKE '%MAISON%'
          AND geomlocmut IS NOT NULL
          AND datemut >= CURRENT_DATE - INTERVAL '3 years'
    """)
    result = conn.execute(query)
    count = result.fetchone()[0]
    print(f"   Total: {count} maisons")

# Test 2: Avec ST_DWithin (rayon 5km)
print(f"\n3. Test: Avec ST_DWithin (rayon 5km autour de Thollon)")
with r.engine.connect() as conn:
    query = text("""
        SELECT COUNT(*) FROM dvf_plus_2025_2.dvf_plus_mutation
        WHERE sbati >= 128 AND sbati <= 192
          AND valeurfonc > 0
          AND libtypbien LIKE '%MAISON%'
          AND geomlocmut IS NOT NULL
          AND datemut >= CURRENT_DATE - INTERVAL '3 years'
          AND ST_DWithin(
            ST_Transform(geomlocmut, 4326)::geography,
            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
            5000
          )
    """)
    result = conn.execute(query, {'lat': thollon_lat, 'lon': thollon_lon})
    count = result.fetchone()[0]
    print(f"   Total: {count} maisons")

# Test 3: Récupérer quelques exemples avec distances
print(f"\n4. Test: Récupérer 10 maisons les plus proches de Thollon")
with r.engine.connect() as conn:
    query = text("""
        SELECT 
            sbati,
            valeurfonc,
            datemut,
            ST_Distance(
                ST_Transform(geomlocmut, 4326)::geography,
                ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography
            ) / 1000 as distance_km
        FROM dvf_plus_2025_2.dvf_plus_mutation
        WHERE sbati >= 128 AND sbati <= 192
          AND valeurfonc > 0
          AND libtypbien LIKE '%MAISON%'
          AND geomlocmut IS NOT NULL
          AND datemut >= CURRENT_DATE - INTERVAL '3 years'
        ORDER BY ST_Distance(
            ST_Transform(geomlocmut, 4326)::geography,
            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography
        )
        LIMIT 10
    """)
    result = conn.execute(query, {'lat': thollon_lat, 'lon': thollon_lon})
    rows = result.fetchall()
    if rows:
        print(f"   Surface | Prix      | Date       | Distance")
        print(f"   --------|-----------|------------|----------")
        for row in rows:
            print(f"   {row[0]:6.0f}m² | {row[1]:9,.0f}€ | {row[2]} | {row[3]:6.2f} km")
    else:
        print("   Aucun résultat")

# Test 4: Via get_comparables()
print(f"\n5. Test: Via get_comparables() (rayon 5km)")
df = r.get_comparables(
    latitude=thollon_lat,
    longitude=thollon_lon,
    type_bien='Maison',
    surface_min=128,
    surface_max=192,
    rayon_km=5,
    annees=3,
    limit=50
)
print(f"   Résultats: {len(df)} comparables")
if len(df) > 0:
    print("\n   Premiers résultats:")
    print(df[['adresse', 'distance_km', 'sbati', 'valeurfonc']].head(5))

print("\n" + "="*70)
print("FIN DU DIAGNOSTIC")
print("="*70)
