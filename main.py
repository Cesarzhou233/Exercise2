import sqlite3

# Step 1: Read the file and copy its content to a list
with open('stephen_king_adaptations.txt', 'r') as file:
    stephen_king_adaptations_list = [line.strip().split(',') for line in file]

# Step 2: Establish a connection with a new SQLite database
conn = sqlite3.connect('stephen_king_adaptations.db')
c = conn.cursor()

# Step 3: Create a table in the database
c.execute('''
          CREATE TABLE stephen_king_adaptations_table
          (movieID TEXT, movieName TEXT, movieYear INTEGER, imdbRating REAL)
          ''')

# Step 4: Insert content into the table
for movie in stephen_king_adaptations_list:
    c.execute('INSERT INTO stephen_king_adaptations_table VALUES (?, ?, ?, ?)', movie)

# Commit the changes to the database
conn.commit()

# Step 5: User interaction loop
while True:
    print("\nOptions:")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. STOP")

    option = input("Enter your choice (1-4): ")

    if option == '1':
        movie_name = input("Enter the movie name: ")
        c.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieName=?', (movie_name,))
        result = c.fetchone()
        if result:
            print(f"Movie ID: {result[0]}, Movie Name: {result[1]}, Year: {result[2]}, Rating: {result[3]}")
        else:
            print("No such movie exists in our database")

    elif option == '2':
        movie_year = input("Enter the movie year: ")
        c.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?', (movie_year,))
        result = c.fetchall()
        if result:
            for row in result:
                print(f"Movie ID: {row[0]}, Movie Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
        else:
            print("No movies were found for that year in our database")

    elif option == '3':
        rating_limit = input("Enter the minimum rating: ")
        c.execute('SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?', (rating_limit,))
        result = c.fetchall()
        if result:
            for row in result:
                print(f"Movie ID: {row[0]}, Movie Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
        else:
            print("No movies at or above that rating were found in the database")

    elif option == '4':
        break

# Step 6: Close the connection
conn.close()
