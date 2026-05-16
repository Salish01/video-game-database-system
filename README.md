# Video Game Database System

A final project built with **Python, Tkinter, and MySQL**.

This project is a desktop application for managing video game information. It allows users to add new games, search for games, display all saved records, and delete records from the database.

## Features

- Add a new game
- Select platform and genre
- Search games by title
- Show all games
- Delete a game by `game_id`

## Database Structure

This project uses 5 tables:

- `games`
- `platforms`
- `genres`
- `game_platforms`
- `game_genres`

The database uses junction tables to handle many-to-many relationships between games and platforms, and between games and genres.

## Technologies Used

- Python
- Tkinter
- MySQL
- mysql-connector-python

## Files

- `video_game_project.py` — main Tkinter application
- `video_game_project.sql` — database schema
- `sample_data.sql` — sample records for testing
- `video_game_project.mwb` — MySQL Workbench ER model

## How to Run

1. Start your MySQL server
2. Import `video_game_project.sql`
3. Import `sample_data.sql`
4. Make sure the database name is `video_game_db`
5. Update the database password in the Python file if needed
6. Run the Python program


Requirements
Install the dependency with:
pip install -r requirements.txt
