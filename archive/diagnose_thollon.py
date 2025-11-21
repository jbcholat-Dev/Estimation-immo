from src.supabase_data_retriever import SupabaseDataRetriever
from sqlalchemy import text

r = SupabaseDataRetriever()
conn = r.engine.connect()

print("="*50)
print("DIAGNOSTIC MAISON THOLLON (163 Imp. des Vernes)")
print("="*50)

# Requête pour trouver la maison spécifique (par proximité géographique très fine)
# Coordonnées Thollon (Impasse des Vernes) : ~ 46.3907, 6.6970
lat = 46.3907
lon = 6.6970

query = text("""
    SELECT
        idmutation,
        datemut,
        valeurfonc,
        sbati,
        libtypbien,
        nblocmut,
        nbmai1pp, nbmai2pp, nbmai3pp, nbmai4pp, nbmai5pp,
        ST_Distance(
            ST_Transform(geomlocmut, 4326)::geography,
            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography
        ) as dist_m
    FROM dvf_plus_2025_2.dvf_plus_mutation
    WHERE ST_DWithin(
        ST_Transform(geomlocmut, 4326)::geography,
        ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
        500  -- Rayon de 500m pour être sûr de la trouver
    )
    AND sbati > 100 -- Filtre pour trouver la maison de ~160m2
    ORDER BY dist_m ASC
""")

result = conn.execute(query, {"lat": lat, "lon": lon})

found = False
for row in result:
    found = True
    print(f"\n🏠 MAISON TROUVÉE à {row.dist_m:.1f}m :")
    print(f"   - Date: {row.datemut}")
    print(f"   - Prix: {row.valeurfonc} €")
    print(f"   - Surface (sbati): {row.sbati} m²")
    print(f"   - Type: {row.libtypbien}")
    print(f"   - Nb Locaux (nblocmut): {row.nblocmut}")
    print("   - Détail Pièces (Maisons):")
    print(f"     * 1 pièce : {row.nbmai1pp}")
    print(f"     * 2 pièces: {row.nbmai2pp}")
    print(f"     * 3 pièces: {row.nbmai3pp}")
    print(f"     * 4 pièces: {row.nbmai4pp}")
    print(f"     * 5+ pièces: {row.nbmai5pp}")

if not found:
    print("\n❌ Aucune maison > 100m² trouvée dans les 500m.")

conn.close()
