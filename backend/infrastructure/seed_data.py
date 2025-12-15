import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastructure.db import AsyncSessionLocal
from backend.infrastructure import models


async def seed():
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        cities_data = [
            {
                "name": {"ar": "حيفا", "he": "חיפה", "en": "Haifa"},
                "areas": [
                    {"ar": "الكرمل", "he": "כרמל", "en": "Carmel"},
                    {"ar": "وادي النسناس", "he": "ואדי ניסנאס", "en": "Wadi Nisnas"},
                    {"ar": "حيفا التحتا", "he": "העיר התחתית", "en": "Downtown"}
                ],
            },
            {
                "name": {"ar": "الناصرة", "he": "נצרת", "en": "Nazareth"},
                "areas": [
                    {"ar": "الناصرة العليا", "he": "נצרת עילית", "en": "Upper Nazareth"},
                    {"ar": "حي الصفافرة", "he": "ספאפרה", "en": "Safafra"}
                ],
            },
            {
                "name": {"ar": "أم الفحم", "he": "אום אל-פחם", "en": "Umm al-Fahm"},
                "areas": [
                    {"ar": "وادي عارة", "he": "ואדי עארה", "en": "Wadi Ara"},
                    {"ar": "عرب العرايدة", "he": "ערערה", "en": "Ar'ara"}
                ],
            },
            {
                "name": {"ar": "سخنين", "he": "סכנין", "en": "Sakhnin"},
                "areas": [
                    {"ar": "دير حنا", "he": "דיר חנא", "en": "Deir Hanna"},
                    {"ar": "عرابة", "he": "עראבה", "en": "Arraba"}
                ],
            },
            {
                "name": {"ar": "الطيبة", "he": "טייבה", "en": "Tayibe"},
                "areas": [
                    {"ar": "قلنسوة", "he": "קלנסווה", "en": "Qalansawe"},
                    {"ar": "كفر قاسم", "he": "כפר קאסם", "en": "Kafr Qasim"}
                ],
            },
            {
                "name": {"ar": "راهط", "he": "רהט", "en": "Rahat"},
                "areas": [
                    {"ar": "تل السبع", "he": "תל שבע", "en": "Tel as-Sabi"},
                    {"ar": "شقيب السلام", "he": "שגב שלום", "en": "Segev Shalom"}
                ],
            },
            {
                "name": {"ar": "شفاعمرو", "he": "שפרעם", "en": "Shefa-Amr"},
                "areas": [
                    {"ar": "كابول", "he": "כאוכב אבו אל-היג'א", "en": "Kaabiyye"},
                    {"ar": "طمرة", "he": "טמרה", "en": "Tamra"}
                ],
            },
            {
                "name": {"ar": "عكا", "he": "עכו", "en": "Akko"},
                "areas": [
                    {"ar": "عكا القديمة", "he": "עכו העתיקה", "en": "Old Akko"},
                    {"ar": "الميناء", "he": "הנמל", "en": "Harbor"}
                ],
            },
        ]

        city_models = []
        for c in cities_data:
            city = models.CityModel(name_i18n=c["name"])
            session.add(city)
            await session.flush()
            city_models.append(city)
            for area in c["areas"]:
                session.add(models.AreaModel(city_id=city.id, name_i18n=area))

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
