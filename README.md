# Video Game Database System

A final project built with **Python, Tkinter, and MySQL**.

This project is a simple desktop application for managing video game information. It allows users to add new games, search for games, display all saved records, and delete records from the database.

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
- `video_game_project.sql` — SQL schema and database setup
- `video_game_project.mwb` — MySQL Workbench ER model

## How to Run

1. Start your MySQL server
2. Import the SQL file into MySQL
3. Make sure the database name is `video_game_db`
4. Update the database password in the Python file if needed
5. Run the Python program

```bash
python video_game_project.py
