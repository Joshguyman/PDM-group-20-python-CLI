from app.utils.rating import get_average_rating


def format_videogame_result(result, search, searchtype, sorttype, desc:bool):
    """
    Formats and prints the videogame query result nicely.

    :param result: Query result as a list of tuples (title, platforms, publishers, developers, playtimes, ratings, esrbrating).
    :param search: The search term used.
    :param searchtype: The type of search performed.
    """
    if not result:
        print(f"No results found for {searchtype}: '{search}'.")
        return
    result.sort(key=lambda x: x[sorttype], reverse=desc)
    for row in result:
        title, platforms, publishers, developers, playtimes, ratings, genres, esrbrating, _ = row

        ratings = ratings.replace(" ", "").split(",")
        ones = ratings.count("1")
        twos = ratings.count("2")
        threes = ratings.count("3")
        fours = ratings.count("4")
        fives = ratings.count("5")
        print("=" * 80)
        print(f"Title: {title}")
        print(f"Platforms: {platforms if platforms else 'N/A'}")
        print(f"Publishers: {publishers if publishers else 'N/A'}")
        print(f"Developers: {developers if developers else 'N/A'}")
        print(f"Playtimes: {playtimes if playtimes else 'N/A'}")
        print(f"Ratings: 1 stars ({ones}), 2 stars ({twos}), 3 stars ({threes}), 4 stars ({fours}), 5 stars ({fives})")
        print(f"Genres: {genres if genres else 'N/A'}")
        print(f"ESRB Rating: {esrbrating if esrbrating else 'N/A'}")
        print("=" * 80)
    return

def format_videogame_date_results(results, date):
    """
    Nicely prints the results of the videogame query.

    :param results: A list of tuples representing the query results.
    """
    if not results:
        print("No results found for this month.")
        return
    print(f"Top 5 games for \"{date}\":")
    # Print each row in the desired format
    for row in results:
        print("=" * 80)
        print(f"Title: {row[0]}")
        print(f"Platforms: {row[1]}")
        print(f"Publishers: {row[2]}")
        print(f"Developers: {row[3]}")
        print(f"Genres: {row[4]}")
        print(f"ESRB Rating: {row[5]}")
        print(f"Average Score: {round(int(row[6]))}")
        print("=" * 80)

def format_collection_result(result):
    for row in result:
        name, count, play_time, _ = row
        print(f"\"{name}\" Collection has {count} games with a total playtime of {play_time}")
    return