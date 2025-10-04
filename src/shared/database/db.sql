DROP DATABASE IF EXISTS cs_stats;
CREATE DATABASE cs_stats;
USE cs_stats;

-- Jogadores
CREATE TABLE player (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    nick VARCHAR(60) NOT NULL
);

-- Mapas
CREATE TABLE map (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    is_active TINYINT NOT NULL
);

-- Partidas
CREATE TABLE game (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dt DATETIME NOT NULL,
    status ENUM('win', 'lose', 'draw') NOT NULL,
    adversary_rounds INT,
    allies_rounds INT,
    fk_map INT NOT NULL,
    
    FOREIGN KEY (fk_map) REFERENCES map(id)
);

-- Estatísticas individuais
CREATE TABLE game_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fk_player INT,
    fk_game INT,
    kills INT,
    deaths INT,
    assists INT,
    headshot INT,
    damage INT,
    tag VARCHAR(45),
    
    FOREIGN KEY (fk_player) REFERENCES player(id),
    FOREIGN KEY (fk_game) REFERENCES game(id)
);

INSERT INTO player (name, nick) VALUES
('Lucas', 'Lucas Foguetes ツ'), 
('Iago', 'Mr.Azeitona'),         
('Ranier', 'raynier'),                 
('Tu-π', 'Tu-π'),                        
('Dnailo', 'Латинский алфави'), 
('Biel', 'setter'),                   
('João Bahia', 'Khalid Kashmiri'); 

INSERT INTO map (name, is_active) VALUES
('Inferno', 1),    
('Mirage', 1),    
('Nuke', 1),       
('Anubis', 1),    
('Overpass', 1),   
('Dust2', 1),      
('Ancient', 1),    
('Train', 1),
('Vertigo', 1);      

INSERT INTO game (dt, status, adversary_rounds, allies_rounds, fk_map) VALUES
('2025-09-25 19:26:44', 'win',  4, 13, 1),    
('2025-09-25 19:42:43', 'draw', 12, 12, 2), 
('2025-09-25 21:05:04', 'win',  9, 13, 3),   
('2025-09-25 21:24:43', 'win',  11, 13, 4),   
('2025-09-25 21:43:24', 'draw', 12, 12, 5);   

-- Partida 1 (Vitória - Inferno)
INSERT INTO game_data (fk_player, fk_game, kills, deaths, assists, headshot, damage) VALUES
(1, 1, 25, 16, 2, 0, 0), 
(2, 1, 18, 11, 3, 0, 0), 
(3, 1, 29, 7, 2, 0, 0), 
(4, 1, 18, 10, 2, 0, 0),
(5, 1, 11, 14, 2, 0, 0); 

INSERT INTO game_data (fk_player, fk_game, kills, deaths, assists, headshot, damage) VALUES
(1, 2, 29, 16, 0, 0, 0), 
(3, 2, 26, 18, 2, 0, 0), 
(5, 2, 22, 14, 2, 0, 0), 
(6, 2, 10, 10, 1, 0, 0),
(2, 2, 18, 16, 1, 0, 0); 

INSERT INTO game_data (fk_player, fk_game, kills, deaths, assists, headshot, damage) VALUES
(1, 3, 26, 12, 0, 0, 0), 
(2, 3, 19, 10, 0, 0, 0), 
(3, 3, 23, 14, 0, 0, 0),
(7, 3, 14, 11, 0, 0, 0), 
(6, 3, 9, 14, 0, 0, 0);  

INSERT INTO game_data (fk_player, fk_game, kills, deaths, assists, headshot, damage) VALUES
(1, 4, 28, 14, 1, 0, 0),
(3, 4, 25, 12, 1, 0, 0), 
(2, 4, 24, 16, 0, 0, 0), 
(4, 4, 16, 16, 0, 0, 0),
(5, 4, 18, 14, 0, 0, 0); 

INSERT INTO game_data (fk_player, fk_game, kills, deaths, assists, headshot, damage) VALUES
(1, 5, 16, 10, 1, 0, 0), 
(2, 5, 22, 12, 2, 0, 0), 
(3, 5, 23, 13, 0, 0, 0), 
(6, 5, 14, 13, 0, 0, 0), 
(7, 5, 10, 11, 0, 0, 0); 