import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from models.product import Base
from models.chat import ChatHistory
from models.user_interaction import GlobalUserPreference
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def migrate_database():
    """Migrar la base de datos al nuevo esquema sin sesiones"""
    engine = create_async_engine(settings.database_url, echo=True)
    
    async with engine.begin() as conn:
        try:
            # Crear nuevas tablas
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tablas creadas exitosamente")
            
            # Migrar datos existentes de user_preferences a global_user_preferences
            try:
                # Verificar si existe la tabla antigua
                result = await conn.execute(text(
                    "SELECT COUNT(*) FROM user_preferences"
                ))
                count = result.scalar()
                
                if count and count > 0:
                    # Combinar todas las preferencias en una sola global
                    await conn.execute(text("""
                        INSERT INTO global_user_preferences 
                        (preferred_categories, preferred_brands, price_range_min, price_range_max, interaction_count, last_updated)
                        SELECT 
                            json_group_array(DISTINCT json_extract(preferred_categories, '$')),
                            json_group_array(DISTINCT json_extract(preferred_brands, '$')),
                            MIN(price_range_min),
                            MAX(price_range_max),
                            SUM(interaction_count),
                            MAX(last_updated)
                        FROM user_preferences
                    """))
                    logger.info("Preferencias migradas exitosamente")
            except Exception as e:
                logger.info(f"No se encontraron preferencias antiguas para migrar: {e}")
            
            # Migrar interacciones (eliminar session_id)
            try:
                await conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS user_interactions_new (
                        id INTEGER PRIMARY KEY,
                        product_id INTEGER,
                        category_viewed VARCHAR,
                        search_query TEXT,
                        interaction_type VARCHAR,
                        timestamp DATETIME,
                        FOREIGN KEY(product_id) REFERENCES products(id)
                    )
                """))
                
                await conn.execute(text("""
                    INSERT INTO user_interactions_new 
                    (id, product_id, category_viewed, search_query, interaction_type, timestamp)
                    SELECT id, product_id, category_viewed, search_query, interaction_type, timestamp
                    FROM user_interactions
                """))
                
                await conn.execute(text("DROP TABLE IF EXISTS user_interactions"))
                await conn.execute(text("ALTER TABLE user_interactions_new RENAME TO user_interactions"))
                logger.info("Interacciones migradas exitosamente")
            except Exception as e:
                logger.info(f"No se encontraron interacciones antiguas para migrar: {e}")
                
        except Exception as e:
            logger.error(f"Error durante la migración: {e}")
            raise
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(migrate_database()) 