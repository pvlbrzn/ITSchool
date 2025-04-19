import requests
from bs4 import BeautifulSoup as Bs
from faker import Faker

from django.utils import timezone

from .models import Blog

# Инициализация Faker для генерации фейковых данных
fake = Faker('ru_RU')


def fetch_blog_html(url: str) -> str:
    """
    Загружает HTML-страницу блога по указанному URL.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f'Ошибка: не удалось получить HTML, статус: {response.status_code}')
    return response.text


def extract_image_url(block) -> str:
    """
    Извлекает URL изображения из блока блога.
    """
    meta_tag = block.select_one("meta[itemprop='image']")
    return meta_tag["content"] if meta_tag and "content" in meta_tag.attrs else ""


def extract_blog_blocks(html: str):
    """
    Парсит HTML и возвращает список блоков с постами блога.
    """
    soup = Bs(html, 'lxml')
    container = soup.select_one('#rec220606141 > div > div.t-card__container.t-container')
    if not container:
        raise RuntimeError("❌ Контейнер блогов не найден.")
    return container.select("div > div")


def generate_fake_content() -> str:
    """
    Генерирует фейковое длинное содержание поста.
    """
    return fake.text(max_nb_chars=5000)


def save_blog(title, annotation, content, image_url, publication_date, author):
    """
    Сохраняет пост блога в базу данных, избегая дублирования.
    """
    obj, created = Blog.objects.get_or_create(
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


def parse_blog():
    """
    Главная функция: очищает БД, парсит посты с сайта и сохраняет их в базу.
    """
    Blog.objects.all().delete()  # Очистка перед парсингом
    url = 'https://teachmeskills.by/blog'
    html = fetch_blog_html(url)
    blocks = extract_blog_blocks(html)

    for block in blocks:
        title_tag = block.select_one("div.t-name")
        annotation_tag = block.select_one("div.t-descr")
        image_url = extract_image_url(block)

        if not title_tag or not annotation_tag:
            print(f"⚠️ Пропущена запись блога (отсутствуют данные): {block}")
            continue

        title = title_tag.get_text(strip=True)
        annotation = annotation_tag.get_text(strip=True)
        content = generate_fake_content()
        date = timezone.now()
        author = "TeachMeSkills"

        created = save_blog(title, annotation, content, image_url, date, author)
        if created:
            print(f"🟢 Добавлено: {title} ({date.strftime('%d.%m.%Y')})")
        else:
            print(f"ℹ️ Уже существует: {title}")
