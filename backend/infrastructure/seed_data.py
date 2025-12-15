import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastructure.db import AsyncSessionLocal
from backend.infrastructure import models


async def seed():
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        tel_aviv = models.CityModel(name_i18n={"ar": "تل أبيب", "he": "תל אביב", "en": "Tel Aviv"})
        haifa = models.CityModel(name_i18n={"ar": "حيفا", "he": "חיפה", "en": "Haifa"})
        session.add_all([tel_aviv, haifa])
        await session.flush()

        areas = [
            models.AreaModel(city_id=tel_aviv.id, name_i18n={"ar": "يافا", "he": "יפו", "en": "Jaffa"}),
            models.AreaModel(city_id=tel_aviv.id, name_i18n={"ar": "رمت غان", "he": "רמת גן", "en": "Ramat Gan"}),
            models.AreaModel(city_id=haifa.id, name_i18n={"ar": "الكرمل", "he": "כרמל", "en": "Carmel"}),
        ]
        session.add_all(areas)

        categories = [
            models.CategoryModel(
                name_i18n={"ar": "كهربائي", "he": "חשמלאי", "en": "Electrician"}
            ),
            models.CategoryModel(
                name_i18n={"ar": "سبّاك", "he": "אינסטלטור", "en": "Plumber"}
            ),
            models.CategoryModel(
                name_i18n={"ar": "نظافة", "he": "ניקיון", "en": "Cleaning"}
            ),
        ]
        session.add_all(categories)
        await session.commit()
        print("Seeded cities, areas, categories")


if __name__ == "__main__":
    asyncio.run(seed())
