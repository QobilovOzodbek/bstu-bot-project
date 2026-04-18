import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper


class BSTUScraper(BaseScraper):
    BASE_URL = "https://bstu.uz"
    NEWS_URL = "https://bstu.uz/"
    ANNOUNCEMENTS_URL = "https://bstu.uz/articles/elon"

    LEADERSHIP_PAGES = [
        {
            "position": "Rektor",
            "url": "https://bstu.uz/rahbariyat/rektor",
        },
        {
            "position": "O'quv ishlari bo'yicha prorektor",
            "url": "https://bstu.uz/rahbariyat/prorektor-po-uchebnoy-rabote",
        },
        {
            "position": "Ilmiy ishlar va innovatsiyalar bo'yicha prorektor",
            "url": "https://bstu.uz/rahbariyat/ilmiy-ishlar-va-innovatsiyalar-bo-yicha-prorektor",
        },
        {
            "position": "Xalqaro hamkorlik bo'yicha prorektor",
            "url": "https://bstu.uz/rahbariyat/xalqaro-hamkorlik-bo-yicha-prorektor",
        },
    ]
    
    @staticmethod
    def _clean_text(value: str | None) -> str:
        if not value:
            return ""
        return " ".join(value.split()).strip()

    @staticmethod
    def _is_valid_article_link(href: str | None) -> bool:
        if not href:
            return False
        return "/article/" in href or href.startswith("https://bstu.uz/article/")

    @staticmethod
    def _extract_phone(text: str) -> str:
        match = re.search(r"(\+?\d[\d\-\+\(\)\s]{7,}\d)", text)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_email(text: str) -> str:
        match = re.search(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|t\.me/[A-Za-z0-9_]+)", text)
        return match.group(1).strip() if match else ""

    def _parse_cards_from_page(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")
        items: list[dict] = []

        for link in soup.select("a[href]"):
            href = link.get("href", "").strip()
            if not self._is_valid_article_link(href):
                continue

            title = self._clean_text(link.get_text(" ", strip=True))
            if len(title) < 6:
                continue

            parent = link.find_parent()
            block_text = self._clean_text(parent.get_text(" ", strip=True)) if parent else title

            summary = ""
            if block_text and block_text != title:
                summary = block_text.replace(title, "", 1).strip(" -*\n\t")

            full_url = urljoin(self.BASE_URL, href)

            items.append(
                {
                    "title": title,
                    "summary": summary[:300],
                    "date": "",
                    "url": full_url,
                }
            )

        unique: list[dict] = []
        seen: set[tuple[str, str]] = set()

        for item in items:
            key = (item["title"], item["url"])
            if key in seen:
                continue
            seen.add(key)
            unique.append(item)

        return unique

    async def get_news(self) -> list[dict]:
        html = await self.fetch_html(self.NEWS_URL)
        items = self._parse_cards_from_page(html)
        filtered = [item for item in items if "elon" not in item["url"].lower()]
        return filtered[:10]

    async def get_announcements(self) -> list[dict]:
        html = await self.fetch_html(self.ANNOUNCEMENTS_URL)
        items = self._parse_cards_from_page(html)
        return items[:10]

    async def get_contact_info(self) -> dict:
        html = await self.fetch_html(self.BASE_URL)
        soup = BeautifulSoup(html, "lxml")
        text = self._clean_text(soup.get_text(" ", strip=True))

        address = ""
        phone = ""
        email = ""

        if "Q.MURTAZAEV" in text or "MURTAZAEV" in text:
            idx = text.find("MURTAZAEV")
            address = text[max(0, idx - 70): idx + 80].strip()

        phone = self._extract_phone(text)
        email = self._extract_email(text)

        return {
            "address": address,
            "email": email,
            "phone": phone,
        }

    async def get_quick_links(self) -> list[dict]:
        html = await self.fetch_html(self.BASE_URL)
        soup = BeautifulSoup(html, "lxml")

        candidates = []
        keywords = [
            "HEMIS",
            "Hemis",
            "student",
            "registrator",
            "Masofaviy",
            "platforma",
            "kpi.bstu.uz",
            "TTJ",
            "turar joy",
            "korrupsiya",
        ]

        for a in soup.select("a[href]"):
            title = self._clean_text(a.get_text(" ", strip=True))
            href = a.get("href", "").strip()

            if not title or not href:
                continue

            if any(k.lower() in title.lower() or k.lower() in href.lower() for k in keywords):
                candidates.append({
                    "title": title,
                    "url": urljoin(self.BASE_URL, href),
                })

        unique = []
        seen = set()
        for item in candidates:
            key = (item["title"], item["url"])
            if key in seen:
                continue
            seen.add(key)
            unique.append(item)

        return unique[:12]

    async def get_leadership(self) -> list[dict]:
        results = []

        for page in self.LEADERSHIP_PAGES:
            html = await self.fetch_html(page["url"])
            soup = BeautifulSoup(html, "lxml")
            text = self._clean_text(soup.get_text(" ", strip=True))

            name = ""
            reception_time = ""
            phone = ""
            email = ""

            h4_tags = soup.select("h4")
            for h4 in h4_tags:
                candidate = self._clean_text(h4.get_text(" ", strip=True))
                if len(candidate) > 5:
                    name = candidate
                    break

            rt_match = re.search(r"(Qabul vaqti:|Reception hours:)(.*?)(Telefon:|Phone:|Email:|$)", text, re.IGNORECASE)
            if rt_match:
                reception_time = self._clean_text(rt_match.group(2))

            phone = self._extract_phone(text)
            email = self._extract_email(text)

            results.append({
                "position": page["position"],
                "full_name": name,
                "reception_time": reception_time,
                "phone": phone,
                "email": email,
                "url": page["url"],
            })

        return results
    
    CLUB_SOURCES = [
        {
            "url": "https://bstu.uz/malumot/student-dormitory",
            "source": "Talabalar turar joyi",
            "category": "Umumiy",
        },
        {
            "url": "https://bstu.uz/fakultet/faculty-of-engineering",
            "source": "Muhandislik fakulteti",
            "category": "Fakultet",
        },
        {
            "url": "https://bstu.uz/article/youth-innovation-unite-at-bstu",
            "source": "Yangilik",
            "category": "Texnik",
        },
        {
            "url": "https://bstu.uz/markazlar/department-for-organizing-scientific-research-activities-of-talented-students",
            "source": "Iqtidorli talabalar bo‘limi",
            "category": "Ilmiy",
        },
    ]

    async def get_clubs(self) -> list[dict]:
        results = []

        # 1. Student dormitory page
        try:
            html = await self.fetch_html("https://bstu.uz/malumot/student-dormitory")
            soup = BeautifulSoup(html, "lxml")
            text = self._clean_text(soup.get_text(" ", strip=True))

            # umumiy club yo'nalishlari
            if "culture" in text.lower() or "arts" in text.lower():
                results.extend([
                    {
                        "title": "Madaniyat va san’at to‘garaklari",
                        "category": "Umumiy",
                        "description": "Talabalar uchun madaniyat, san’at, sport, AKT va kitobxonlik yo‘nalishlaridagi to‘garaklar.",
                        "source": "Talabalar turar joyi",
                        "url": "https://bstu.uz/malumot/student-dormitory",
                    },
                    {
                        "title": "Sport to‘garaklari",
                        "category": "Sport",
                        "description": "Sport majmualari asosida faoliyat yuritadigan to‘garaklar.",
                        "source": "Talabalar turar joyi",
                        "url": "https://bstu.uz/malumot/student-dormitory",
                    },
                    {
                        "title": "AKT va kitobxonlik to‘garaklari",
                        "category": "Ta’limiy",
                        "description": "IT texnologiya markazlari va axborot-kutubxona bazasidagi to‘garaklar.",
                        "source": "Talabalar turar joyi",
                        "url": "https://bstu.uz/malumot/student-dormitory",
                    },
                ])
        except Exception:
            pass

        # 2. Engineering faculty page
        try:
            html = await self.fetch_html("https://bstu.uz/fakultet/faculty-of-engineering")
            soup = BeautifulSoup(html, "lxml")
            text = self._clean_text(soup.get_text(" ", strip=True)).lower()

            if "satire and humor" in text:
                results.append({
                    "title": "Satira va yumor talabalar teatr studiyasi",
                    "category": "Madaniy",
                    "description": "Muhandislik fakultetidagi talabalar teatr studiyasi.",
                    "source": "Muhandislik fakulteti",
                    "url": "https://bstu.uz/fakultet/faculty-of-engineering",
                })

            if "zakovat" in text:
                results.append({
                    "title": "Zakovat guruhi",
                    "category": "Intellektual",
                    "description": "Muhandislik fakultetida faoliyat yurituvchi intellektual klub.",
                    "source": "Muhandislik fakulteti",
                    "url": "https://bstu.uz/fakultet/faculty-of-engineering",
                })

            if "architectural industrialization" in text:
                results.append({
                    "title": "Architectural Industrialization QVZ jamoasi",
                    "category": "Madaniy",
                    "description": "Muhandislik fakultetidagi ijodiy klub/jamoa.",
                    "source": "Muhandislik fakulteti",
                    "url": "https://bstu.uz/fakultet/faculty-of-engineering",
                })
        except Exception:
            pass

        # 3. Robotics club article
        try:
            html = await self.fetch_html("https://bstu.uz/article/youth-innovation-unite-at-bstu")
            soup = BeautifulSoup(html, "lxml")
            text = self._clean_text(soup.get_text(" ", strip=True))

            if "Robotics club" in text:
                results.append({
                    "title": "Robotics club",
                    "category": "Texnik",
                    "description": "Zamonaviy texnologiyalar, dasturlash asoslari va avtomatlashtirilgan tizimlar bo‘yicha amaliy to‘garak.",
                    "source": "Yangilik",
                    "url": "https://bstu.uz/article/youth-innovation-unite-at-bstu",
                })
        except Exception:
            pass

        # 4. Talented students department page
        try:
            html = await self.fetch_html("https://bstu.uz/markazlar/department-for-organizing-scientific-research-activities-of-talented-students")
            soup = BeautifulSoup(html, "lxml")
            text = self._clean_text(soup.get_text(" ", strip=True)).lower()

            if "scientific-creative clubs" in text or "clubs for talented students" in text:
                results.append({
                    "title": "Ilmiy-ijodiy to‘garaklar",
                    "category": "Ilmiy",
                    "description": "Iqtidorli talabalar uchun ilmiy-ijodiy tadqiqot to‘garaklari.",
                    "source": "Iqtidorli talabalar bo‘limi",
                    "url": "https://bstu.uz/markazlar/department-for-organizing-scientific-research-activities-of-talented-students",
                })
        except Exception:
            pass

        # deduplicate
        unique = []
        seen = set()
        for item in results:
            key = (item["title"], item["url"])
            if key in seen:
                continue
            seen.add(key)
            unique.append(item)

        return unique