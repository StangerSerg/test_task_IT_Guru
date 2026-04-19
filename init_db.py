import asyncio
from sqlalchemy import text
from app.database import engine
from app.models import Base


async def create_tables():
    try:
        async with engine.begin() as conn:
            # Проверяем, есть ли уже таблицы
            result = await conn.execute(text("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_name = 'goods'
                )
            """))
            tables_exist = result.scalar()

            if not tables_exist:
                await conn.run_sync(Base.metadata.create_all)
                print("Таблицы созданы")
            else:
                print("Таблицы уже существуют, пропускаем создание")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_tables())