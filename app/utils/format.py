def format_videogame_result(result, search, searchtype):
    """
    Formats and prints the videogame query result nicely.

    :param result: Query result as a list of tuples (title, platforms, publishers, developers, playtimes, ratings, esrbrating).
    :param search: The search term used.
    :param searchtype: The type of search performed.
    """
    if not result:
        print(f"No results found for {searchtype}: '{search}'.")
        return

    for row in result:
        title, platforms, publishers, developers, playtimes, ratings, genres, esrbrating = row
        print("=" * 80)
        print(f"Title: {title}")
        print(f"Platforms: {platforms if platforms else 'N/A'}")
        print(f"Publishers: {publishers if publishers else 'N/A'}")
        print(f"Developers: {developers if developers else 'N/A'}")
        print(f"Playtimes: {playtimes if playtimes else 'N/A'}")
        print(f"Ratings: {ratings if ratings else 'N/A'}")
        print(f"Genres: {genres if genres else 'N/A'}")
        print(f"ESRB Rating: {esrbrating if esrbrating else 'N/A'}")
        print("=" * 80)




    return