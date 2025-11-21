from src.supabase_data_retriever import SupabaseDataRetriever
from sqlalchemy import text

r = SupabaseDataRetriever()
conn = r.engine.connect()

# Lister les colonnes de la table DVF
result = conn.execute(text("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_schema = 'dvf_plus_2025_2' 
      AND table_name = 'dvf_plus_mutation' 
    ORDER BY ordinal_position
"""))

print("Colonnes disponibles dans dvf_plus_mutation:")
print("=" * 50)
for row in result:
    print(f"  - {row[0]}")

conn.close()
