from src.supabase_data_retriever import SupabaseDataRetriever
from sqlalchemy import text

r = SupabaseDataRetriever()
conn = r.engine.connect()

print("="*50)
print("VERIFICATION SCHEMA BASE DE DONNEES")
print("="*50)

# 1. Lister les tables du schéma
print("\n1. Tables dans le schéma 'dvf_plus_2025_2':")
tables = conn.execute(text("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'dvf_plus_2025_2'
"""))
for row in tables:
    print(f"   - {row[0]}")

# 2. Chercher la colonne nbpprinc partout
print("\n2. Recherche de la colonne 'nbpprinc' (ou similaire) dans TOUTES les tables:")
columns = conn.execute(text("""
    SELECT table_name, column_name 
    FROM information_schema.columns 
    WHERE table_schema = 'dvf_plus_2025_2' 
      AND (column_name LIKE '%nbp%' OR column_name LIKE '%piece%')
"""))
found = False
for row in columns:
    print(f"   - Table '{row[0]}' : Colonne '{row[1]}'")
    found = True

if not found:
    print("   ❌ Aucune colonne ressemblant à 'nbpprinc' ou 'piece' trouvée.")

# 3. Re-lister les colonnes de dvf_plus_mutation pour être sûr
print("\n3. Colonnes de 'dvf_plus_mutation' (Vérification finale):")
cols_mut = conn.execute(text("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_schema = 'dvf_plus_2025_2' 
      AND table_name = 'dvf_plus_mutation'
    ORDER BY column_name
"""))
for row in cols_mut:
    if 'nb' in row[0] or 'pp' in row[0]: # Filtre pour lisibilité
        print(f"   - {row[0]}")

conn.close()
