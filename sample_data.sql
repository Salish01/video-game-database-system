USE video_game_db;

INSERT INTO platforms (platform_name)
VALUES
('PC'),
('Nintendo Switch'),
('PlayStation 5');

INSERT INTO genres (genre_name)
VALUES
('RPG'),
('Roguelike'),
('Simulation');

INSERT INTO games (title, release_year, developer)
VALUES
('Hades', 2020, 'Supergiant Games'),
('Elden Ring', 2022, 'FromSoftware'),
('Stardew Valley', 2016, 'ConcernedApe');

INSERT INTO game_platforms (game_id, platform_id)
VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 3),
(3, 1),
(3, 2);

INSERT INTO game_genres (game_id, genre_id)
VALUES
(1, 2),
(2, 1),
(3, 3);