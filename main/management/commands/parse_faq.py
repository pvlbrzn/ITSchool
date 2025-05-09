import asyncio
from asgiref.sync import sync_to_async
from playwright.async_api import async_playwright

from django.core.management.base import BaseCommand

from main.models import FAQ


class Command(BaseCommand):
    """
    Django management команда для асинхронного парсинга FAQ с сайта TeachMeSkills.
    """
    help = 'Парсит FAQ с сайта TeachMeSkills и сохраняет их в базу данных.'

    def handle(self, *args, **options) -> None:
        """
        Запускает асинхронную функцию парсинга через asyncio.run().
        """
        asyncio.run(parse_and_save_faq())


async def parse_and_save_faq() -> None:
    """
    Асинхронно загружает страницу, парсит вопросы и ответы, сохраняет их в базу данных.
    """
    # Очистка старых записей
    await sync_to_async(FAQ.objects.all().delete)()
    print("База очищена от старых записей.")

    async with async_playwright() as p:
        # Запуск браузера в headless-режиме
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Переход на сайт
        url = 'https://teachmeskills.by/'
        await page.goto(url, timeout=60000)
        print(f"Загрузка страницы: {url}")

        # Ожидание загрузки нужных элементов
        await page.wait_for_selector('span.t668__title')
        print("Найдены элементы вопросов.")

        # Извлечение текста вопросов и ответов
        questions: list[str] = await page.locator('span.t668__title').all_text_contents()
        answers: list[str] = await page.locator('div.t668__textwrapper').all_text_contents()

        # Проверка совпадения количества вопросов и ответов
        if len(questions) != len(answers):
            print(f"⚠Внимание: количество вопросов ({len(questions)}) и ответов ({len(answers)}) не совпадает.")

        # Сохранение вопросов и ответов в базу
        for question, answer in zip(questions, answers):
            await sync_to_async(FAQ.objects.create)(
                question=question,
                answer=answer
            )
        await browser.close()

    print(f"✅ Успешно добавлено {len(questions)} FAQ вопросов и ответов.")

'''
pip install playwright
playwright install
'''
