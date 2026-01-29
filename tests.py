import pytest
from main import BooksCollector


class TestBooksCollector:
    def test_add_new_book(self, collector):
        collector.add_new_book('Загадочная история Бенджамина Баттона')
        assert 'Загадочная история Бенджамина Баттона' in collector.books_genre
        assert collector.books_genre['Загадочная история Бенджамина Баттона'] == ''

    def test_set_book_genre(self, collector):
        collector.add_new_book('Солярис')
        collector.set_book_genre('Солярис', 'Фантастика')
        assert collector.books_genre['Солярис'] == 'Фантастика'

    def test_set_genre_for_nonexistent_book(self, collector):
        collector.set_book_genre('Несуществующая книга', 'Фантастика')
        assert 'Несуществующая книга' not in collector.books_genre


    def test_get_book_genre(self, collector):
        collector.genre.extend(['Драма'])
        collector.add_new_book('Грозовой перевал')
        collector.set_book_genre('Грозовой перевал', 'Драма')
        genre = collector.get_book_genre('Грозовой перевал')
        assert genre == 'Драма'
        assert collector.books_genre['Грозовой перевал'] == 'Драма'

    def test_get_books_genre(self, collector):
        collector.genre.extend(['Роман', 'Драма'])
        collector.add_new_book('Анна Каренина')
        collector.set_book_genre('Анна Каренина', 'Роман')

        collector.add_new_book('Обломов')
        collector.set_book_genre('Обломов', 'Роман')

        collector.add_new_book('451 градус по Фаренгейту')
        collector.set_book_genre('451 градус по Фаренгейту', 'Фантастика')

        books_in_romance = collector.get_books_with_specific_genre('Роман')

        assert isinstance(books_in_romance, list)
        assert 'Анна Каренина' in books_in_romance

    def test_get_books_with_specific_genre_found(self, collector):
        collector.add_new_book('Солярис')
        collector.set_book_genre('Солярис', 'Фантастика')

        collector.add_new_book('Грозовой перевал')
        collector.set_book_genre('Грозовой перевал', 'Драма')

        result = collector.get_books_with_specific_genre('Фантастика')
        assert 'Солярис' in result
        assert 'Грозовой перевал' not in result

    def test_get_books_with_specific_genre_no_matches(self, collector):
        collector.add_new_book('Солярис')
        collector.set_book_genre('Солярис', 'Фантастика')

        result = collector.get_books_with_specific_genre('Драма')
        assert result == []

    def test_get_books_for_children_no_books(self, collector):
        result = collector.get_books_for_children()
        assert result == []

    def test_get_books_for_children_with_books(self, collector):
        collector.add_new_book('Путешествие Алисы')
        collector.set_book_genre('Путешествие Алисы', 'Мультфильмы')
        result = collector.get_books_for_children()
        assert 'Путешествие Алисы' in result


    def test_get_books_for_children_excludes_age_rated(self, collector):
        horror_book = 'Оно'
        collector.add_new_book(horror_book)
        collector.set_book_genre(horror_book, 'Ужасы')
        crime_book = 'Грозовой перевал'
        collector.add_new_book(crime_book)
        collector.set_book_genre(crime_book, 'Драма')

        books_for_children = collector.get_books_for_children()

        assert horror_book not in books_for_children
        assert crime_book not in books_for_children


    @pytest.mark.parametrize("book_name", [
        'Загадочная история Бенджамина Баттона',
        'Игра'
    ])
    def test_add_to_favorites(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)

        favorites = collector.get_list_of_favorites_books()

        assert book_name in favorites


    def test_get_list_of_favorites_books_have_books(self, collector):
        books = ['451 градус по Фаренгейту', 'Грозовой перевал', 'Загадочная история Бенджамина Баттона']
        for book in books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        favorites = collector.get_list_of_favorites_books()
        for book in books:
            assert book in favorites


    @pytest.mark.parametrize("book_name", [
        'Загадочная история Бенджамина Баттона',
        'Игра'
    ])
    def test_delete_from_favorites(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        favorites = collector.get_list_of_favorites_books()
        assert book_name not in favorites


    def test_add_duplicate_in_favorites(self, collector):
        book_name = 'Дивергент'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)

        favorites = collector.get_list_of_favorites_books()

        assert favorites.count(book_name) == 1
