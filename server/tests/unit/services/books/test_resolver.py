from app.services.books.resolver import resolve_books

def test_resolve_books_cache_hit(mocker):
    """Returns cached book without calling external services."""
    db = mocker.Mock()
    cached_book = object()

    mocker.patch("app.services.books.resolver.check_book_cache", return_value=cached_book)
    mocker.patch("app.services.books.resolver.search_google_books")

    result = resolve_books(db, ["Some Book"])

    assert result == [cached_book]

def test_resolve_books_cache_miss_success(mocker):
    """Fetches from API and creates book on cache miss."""
    db = mocker.Mock()

    mocker.patch("app.services.books.resolver.check_book_cache", return_value=None)
    mocker.patch("app.services.books.resolver.search_google_books", return_value={"volumeInfo": {}})
    mocker.patch("app.services.books.resolver.extract_book_data", return_value={"description": "desc"})
    mocker.patch("app.services.books.resolver.generate_embedding", return_value=[0.1, 0.2])
    
    created_book = object()
    mocker.patch("app.services.books.resolver.create_book", return_value=created_book)

    result = resolve_books(db, ["Some Book"])

    assert result == [created_book]

def test_resolve_books_no_api_result(mocker):
    """Skips book when API returns no result."""
    db = mocker.Mock()

    mocker.patch("app.services.books.resolver.check_book_cache", return_value=None)
    mocker.patch("app.services.books.resolver.search_google_books", return_value=None)

    result = resolve_books(db, ["Some Book"])

    assert result == None

def test_resolve_books_handles_exception(mocker):
    """Continues processing when an exception occurs."""
    db = mocker.Mock()

    mocker.patch("app.services.books.resolver.check_book_cache", return_value=None)
    mocker.patch("app.services.books.resolver.search_google_books", side_effect=Exception("fail"))

    result = resolve_books(db, ["Book 1", "Book 2"])

    assert result == None

def test_resolve_books_mixed(mocker):
    """Handles mix of cache hits and misses."""
    db = mocker.Mock()

    cached = object()
    created = object()

    mocker.patch(
        "app.services.books.resolver.check_book_cache",
        side_effect=[cached, None],
    )
    mocker.patch("app.services.books.resolver.search_google_books", return_value={"volumeInfo": {}})
    mocker.patch("app.services.books.resolver.extract_book_data", return_value={"description": "desc"})
    mocker.patch("app.services.books.resolver.generate_embedding", return_value=[1])
    mocker.patch("app.services.books.resolver.create_book", return_value=created)

    result = resolve_books(db, ["Book 1", "Book 2"])

    assert result == [cached, created]