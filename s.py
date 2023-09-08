import sqlite3


def create_connection():
    return sqlite3.connect('stephen_king_adaptations.db')


def read_file(file_path):
    with open(file_path) as f:
        return f.read().splitlines()


def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
        (movieID text, movieName text, movieYear integer, imdbRating real)
    ''')


def clear_table(cursor):
    cursor.execute("DELETE FROM stephen_king_adaptations_table")


def insert_movies_to_table(cursor, movies_list):
    for movie in movies_list:
        movie_data = movie.split(',')
        cursor.execute("INSERT INTO stephen_king_adaptations_table VALUES (?, ?, ?, ?)",
                       (movie_data[0], movie_data[1], int(movie_data[2]), float(movie_data[3])))


def search_by_name(cursor, title):
    cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (title,))
    return cursor.fetchone()


def search_by_year(cursor, year):
    cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (year,))
    return cursor.fetchall()


def search_by_rating(cursor, rating):
    cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating>=?", (rating,))
    return cursor.fetchall()


def main():
    conn = create_connection()
    cursor = conn.cursor()

    movies_list = read_file('stephen_king_adaptations.txt')

    create_table(cursor)
    clear_table(cursor)
    insert_movies_to_table(cursor, movies_list)

    conn.commit()

    while True:
        print("\nOptions:")
        print("1. Search by movie name")
        print("2. Search by movie year")
        print("3. Search by rating")
        print("4. Exit")

        option = input("Enter your choice: ")

        if option == "1":
            title = input("Enter movie title: ")
            result = search_by_name(cursor, title)
            if result:
                print(result)
            else:
                print("No such movie exists in our database.")

        elif option == "2":
            year = input("Enter movie year: ")
            results = search_by_year(cursor, year)
            if results:
                for movie in results:
                    print(movie)
            else:
                print("No movies found for that year in our database.")

        elif option == "3":
            rating = float(input("Enter minimum rating: "))
            results = search_by_rating(cursor, rating)
            if results:
                for movie in results:
                    print(movie)
            else:
                print("No movies at or above that rating were found in the database.")

        elif option == "4":
            conn.close()
            break

        else:
            print("Invalid option selected")


main()
