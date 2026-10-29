import sys
from pathlib import Path

# Обеспечение доступности модуля app при прямом запуске скрипта
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.db.db import get_db
from app.db.crud import get_categories, get_books


def display_catalog() -> None:
    """Чтение и форматированный вывод каталога категорий и книг из PostgreSQL."""
    with get_db() as db:
        categories = get_categories(db)
        books = get_books(db)

        print("=" * 70)
        print("          КАТАЛОГ ТОВАРОВ И КНИГ (PostgreSQL + SQLAlchemy)          ")
        print("=" * 70)
        print(f"Всего категорий: {len(categories)} | Всего книг: {len(books)}\n")

        for category in categories:
            print(f"[Категория #{category.id}] {category.title.upper()}")
            print("-" * 70)

            if not category.books:
                print("  (В данной категории пока нет книг)")
            else:
                for book in category.books:
                    url_str = f" [URL: {book.url}]" if book.url else ""
                    print(f"  • ID {book.id}: «{book.title}» — {book.price:,.2f} руб.{url_str}")
                    print(f"    Описание: {book.description}")
            print()

        print("=" * 70)
        print("Чтение данных из PostgreSQL успешно завершено.")
        print("=" * 70)


if __name__ == "__main__":
    display_catalog()
