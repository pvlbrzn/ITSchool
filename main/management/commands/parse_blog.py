import asyncio
from playwright.async_api import async_playwright, Page

from django.utils import timezone
from django.core.management.base import BaseCommand
from main.models import Blog
from asgiref.sync import sync_to_async
from typing import Optional


class Command(BaseCommand):
    """
    Django команда для парсинга блогов с сайта TeachMeSkills.
    """
    help = 'Парсит блоги с сайта TeachMeSkills и сохраняет их в базу данных.'

    def handle(self, *args, **options):
        asyncio.run(parse_and_save_blogs())


async def fetch_blog_html(url: str, page: Page) -> bool:
    """
    Загружает страницу по URL и проверяет наличие заголовка h1.

    :param url: Ссылка на блог.
    :param page: Экземпляр страницы Playwright.
    :return: Успешность загрузки.
    """
    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_selector("h1.tn-atom", timeout=60000)
        return True
    except Exception as e:
        print(f"❌ Ошибка при обработке {url}: {e}")
        return False


async def parse_and_save_blogs() -> None:
    """
    Основная функция: очищает базу, парсит блог-посты и сохраняет их.
    """
    await sync_to_async(Blog.objects.all().delete)()
    print("🧹 База очищена перед парсингом!")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Переход на страницу со всеми блогами
        await page.goto('https://teachmeskills.by/blog', timeout=60000)

        # Извлечение всех уникальных ссылок на блог-посты
        links = await page.locator('div.t-card__title a').evaluate_all(
            'elements => elements.map(element => element.href)'
        )
        links = list(set(links))
        print(f"🔗 Найдено ссылок для парсинга: {len(links)}")

        # Ограничим до первых 15
        for url in links[:15]:
            try:
                await page.goto(url, timeout=30000)

                try:
                    await page.wait_for_selector('h1', timeout=10000)
                except Exception as e:
                    print(f"❗ Не найден заголовок на {url}. Пропускаем. Причина: {e}")
                    continue

                # Заголовок
                title: str = await page.locator('h1').inner_text()

                # Картинка (первая подходящая)
                try:
                    image_url: Optional[str] = await page.locator('img.t-img.t-width').first.get_attribute('src')
                except Exception as e:
                    print(f"⚠️ Ошибка при извлечении картинки на {url}: {e}")
                    image_url = None

                # Аннотация — первый абзац внутри div
                try:
                    annotation_block = page.locator('div.t-text.t-text_md p')
                    annotation: str = await annotation_block.first.inner_text() if await annotation_block.count() > 0 else ''
                except Exception:
                    annotation = ''

                # Контент — объединяем все текстовые блоки
                content_blocks = await page.locator('div.t-col.t-col_10.t-prefix_1').all_inner_texts()
                content: str = "\n\n".join(content_blocks)

                # Автор и дата
                author = "TeachMeSkills"
                date_obj = timezone.now()

                # Сохраняем запись
                created = await save_blog(title, annotation, content, image_url, date_obj, author)

                if created:
                    print(f"🟢 Добавлено: {title} ({date_obj.strftime('%d.%m.%Y')})")
                else:
                    print(f"ℹ️ Уже существует: {title}")

            except Exception as e:
                print(f"❌ Ошибка при обработке {url}: {str(e)}")
                continue

        await browser.close()


async def save_blog(
    title: str,
    annotation: str,
    content: str,
    image_url: Optional[str],
    publication_date,
    author: str
) -> bool:
    """
    Сохраняет блог в базу, если он ещё не существует.

    :param title: Заголовок статьи.
    :param annotation: Краткое описание.
    :param content: Основной текст.
    :param image_url: Ссылка на изображение.
    :param publication_date: Дата публикации.
    :param author: Автор статьи.
    :return: True, если объект был создан, False — если уже существует.
    """
    obj, created = await sync_to_async(Blog.objects.get_or_create)(
        title=title,
        defaults={
            "annotation": annotation,
            "content": content,
            "image": image_url,
            "date": publication_date,
            "author": author
        }
    )
    return created
