import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="video_game_db"
    )


def load_combobox_data():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT platform_name FROM platforms ORDER BY platform_name;")
        platform_results = cursor.fetchall()
        platform_values = [row[0] for row in platform_results]
        platform_combo["values"] = platform_values

        cursor.execute("SELECT genre_name FROM genres ORDER BY genre_name;")
        genre_results = cursor.fetchall()
        genre_values = [row[0] for row in genre_results]
        genre_combo["values"] = genre_values

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def add_game():
    title = title_entry.get().strip()
    release_year = year_entry.get().strip()
    developer = developer_entry.get().strip()
    platform_name = platform_combo.get().strip()
    genre_name = genre_combo.get().strip()

    if not title or not release_year or not developer or not platform_name or not genre_name:
        messagebox.showwarning("Missing Information", "Please fill in all fields.")
        return

    if not release_year.isdigit():
        messagebox.showwarning("Invalid Input", "Release Year must be a number.")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        sql_game = """
        INSERT INTO games (title, release_year, developer)
        VALUES (%s, %s, %s)
        """
        values_game = (title, release_year, developer)
        cursor.execute(sql_game, values_game)

        new_game_id = cursor.lastrowid

        cursor.execute(
            "SELECT platform_id FROM platforms WHERE platform_name = %s",
            (platform_name,)
        )
        platform_result = cursor.fetchone()
        if platform_result is None:
            raise ValueError("Selected platform was not found in the database.")
        platform_id = platform_result[0]

        cursor.execute(
            "SELECT genre_id FROM genres WHERE genre_name = %s",
            (genre_name,)
        )
        genre_result = cursor.fetchone()
        if genre_result is None:
            raise ValueError("Selected genre was not found in the database.")
        genre_id = genre_result[0]

        cursor.execute(
            "INSERT INTO game_platforms (game_id, platform_id) VALUES (%s, %s)",
            (new_game_id, platform_id)
        )

        cursor.execute(
            "INSERT INTO game_genres (game_id, genre_id) VALUES (%s, %s)",
            (new_game_id, genre_id)
        )

        conn.commit()

        messagebox.showinfo("Success", f"Game '{title}' added successfully!")

        title_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        developer_entry.delete(0, tk.END)
        platform_combo.set("")
        genre_combo.set("")

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def show_all_games():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        sql = """
        SELECT g.game_id, g.title, g.release_year, g.developer,
               GROUP_CONCAT(DISTINCT p.platform_name SEPARATOR ', ') AS platforms,
               GROUP_CONCAT(DISTINCT ge.genre_name SEPARATOR ', ') AS genres
        FROM games g
        LEFT JOIN game_platforms gp ON g.game_id = gp.game_id
        LEFT JOIN platforms p ON gp.platform_id = p.platform_id
        LEFT JOIN game_genres gg ON g.game_id = gg.game_id
        LEFT JOIN genres ge ON gg.genre_id = ge.genre_id
        GROUP BY g.game_id, g.title, g.release_year, g.developer
        ORDER BY g.title;
        """

        cursor.execute(sql)
        results = cursor.fetchall()

        results_text.delete("1.0", tk.END)

        for row in results:
            game_id, title, year, developer, platforms, genres = row

            if platforms is None:
                platforms = "None"
            if genres is None:
                genres = "None"

            output = (
                f"ID: {game_id}\n"
                f"Title: {title}\n"
                f"Year: {year}\n"
                f"Developer: {developer}\n"
                f"Platforms: {platforms}\n"
                f"Genres: {genres}\n"
                f"{'-' * 40}\n"
            )

            results_text.insert(tk.END, output)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def search_game():
    keyword = search_entry.get().strip()

    try:
        conn = connect_db()
        cursor = conn.cursor()

        sql = """
        SELECT g.game_id, g.title, g.release_year, g.developer,
               GROUP_CONCAT(DISTINCT p.platform_name SEPARATOR ', ') AS platforms,
               GROUP_CONCAT(DISTINCT ge.genre_name SEPARATOR ', ') AS genres
        FROM games g
        LEFT JOIN game_platforms gp ON g.game_id = gp.game_id
        LEFT JOIN platforms p ON gp.platform_id = p.platform_id
        LEFT JOIN game_genres gg ON g.game_id = gg.game_id
        LEFT JOIN genres ge ON gg.genre_id = ge.genre_id
        WHERE g.title LIKE %s
        GROUP BY g.game_id, g.title, g.release_year, g.developer
        ORDER BY g.title;
        """

        cursor.execute(sql, ("%" + keyword + "%",))
        results = cursor.fetchall()

        results_text.delete("1.0", tk.END)

        if not results:
            results_text.insert(tk.END, "No matching game found.")
        else:
            for row in results:
                game_id, title, year, developer, platforms, genres = row

                if platforms is None:
                    platforms = "None"
                if genres is None:
                    genres = "None"

                output = (
                    f"ID: {game_id}\n"
                    f"Title: {title}\n"
                    f"Year: {year}\n"
                    f"Developer: {developer}\n"
                    f"Platforms: {platforms}\n"
                    f"Genres: {genres}\n"
                    f"{'-' * 40}\n"
                )

                results_text.insert(tk.END, output)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def delete_game():
    game_id = delete_entry.get().strip()

    if not game_id:
        messagebox.showwarning("Missing Information", "Please enter a Game ID to delete.")
        return

    if not game_id.isdigit():
        messagebox.showwarning("Invalid Input", "Game ID must be a number.")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT title FROM games WHERE game_id = %s", (game_id,))
        result = cursor.fetchone()

        if result is None:
            messagebox.showwarning("Not Found", f"No game found with ID {game_id}.")
            cursor.close()
            conn.close()
            return

        game_title = result[0]

        cursor.execute("DELETE FROM game_platforms WHERE game_id = %s", (game_id,))
        cursor.execute("DELETE FROM game_genres WHERE game_id = %s", (game_id,))
        cursor.execute("DELETE FROM games WHERE game_id = %s", (game_id,))

        conn.commit()

        messagebox.showinfo("Success", f"Game '{game_title}' (ID {game_id}) deleted successfully.")

        delete_entry.delete(0, tk.END)

        cursor.close()
        conn.close()

        show_all_games()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


root = tk.Tk()
root.title("Video Game Information Database")
root.geometry("650x500")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Add Game")

title_label = ttk.Label(tab1, text="Game Title:")
title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
title_entry = ttk.Entry(tab1, width=30)
title_entry.grid(row=0, column=1, padx=10, pady=10)

year_label = ttk.Label(tab1, text="Release Year:")
year_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
year_entry = ttk.Entry(tab1, width=30)
year_entry.grid(row=1, column=1, padx=10, pady=10)

developer_label = ttk.Label(tab1, text="Developer:")
developer_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
developer_entry = ttk.Entry(tab1, width=30)
developer_entry.grid(row=2, column=1, padx=10, pady=10)

platform_label = ttk.Label(tab1, text="Platform:")
platform_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
platform_combo = ttk.Combobox(tab1, width=27, state="readonly")
platform_combo.grid(row=3, column=1, padx=10, pady=10)

genre_label = ttk.Label(tab1, text="Genre:")
genre_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
genre_combo = ttk.Combobox(tab1, width=27, state="readonly")
genre_combo.grid(row=4, column=1, padx=10, pady=10)

add_button = ttk.Button(tab1, text="Add Game", command=add_game)
add_button.grid(row=5, column=1, padx=10, pady=20, sticky="e")

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Search / View Games")

search_label = ttk.Label(tab2, text="Search by Title:")
search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

search_entry = ttk.Entry(tab2, width=30)
search_entry.grid(row=0, column=1, padx=10, pady=10)

search_button = ttk.Button(tab2, text="Search", command=search_game)
search_button.grid(row=0, column=2, padx=10, pady=10)

show_all_button = ttk.Button(tab2, text="Show All Games", command=show_all_games)
show_all_button.grid(row=1, column=1, padx=10, pady=10)

delete_label = ttk.Label(tab2, text="Delete by Game ID:")
delete_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

delete_entry = ttk.Entry(tab2, width=20)
delete_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

delete_button = ttk.Button(tab2, text="Delete Game", command=delete_game)
delete_button.grid(row=2, column=2, padx=10, pady=10)

results_label = ttk.Label(tab2, text="Results:")
results_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

results_text = tk.Text(tab2, width=90, height=22)
results_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

load_combobox_data()

root.mainloop()