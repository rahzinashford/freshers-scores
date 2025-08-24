-- Performance table schema for tracking cultural event performances
-- Run this script on your deployed PostgreSQL database to add performance tracking

-- Create the performance table
CREATE TABLE IF NOT EXISTS performance (
    id SERIAL PRIMARY KEY,
    performer_name VARCHAR(100) NOT NULL,
    performance_type VARCHAR(50) NOT NULL,
    year VARCHAR(10) NOT NULL,
    contact_number VARCHAR(15),
    mc_session VARCHAR(20),
    time_slot VARCHAR(50),
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    notes TEXT
);

-- Insert the performance data from Freshers Day 2025
INSERT INTO performance (performer_name, performance_type, year, contact_number, mc_session, time_slot) VALUES
-- MC-1 (9:15-9:45Am)
('Diya', 'Group Dance', 'III', NULL, 'MC-1', '9:15-9:45Am'),
('Shivada', 'Duo Dance', 'III', '6362819768', 'MC-1', '9:15-9:45Am'),
('Mizaj', 'Song', 'II', '8129795812', 'MC-1', '9:15-9:45Am'),
('Vaishnav', 'Group Dance', 'II', '8891803450', 'MC-1', '9:15-9:45Am'),
('Ayesha', 'Group Dance', 'I', '9483281379', 'MC-1', '9:15-9:45Am'),

-- MC-2 (10:10-10:35Am)
('Sagara', 'Single Dance', 'II', '9567257130', 'MC-2', '10:10-10:35Am'),
('Hiraganna', 'Song', 'I', '8618080826', 'MC-2', '10:10-10:35Am'),
('Nandhana TS', 'Group Dance', 'III', '9995845193', 'MC-2', '10:10-10:35Am'),
('Shanumol', 'Group Dance', 'II', '97455590308', 'MC-2', '10:10-10:35Am'),
('Mushayil', 'Group Dance', 'I', '8589887788', 'MC-2', '10:10-10:35Am'),
('Gouri lakshmi', 'Group Dance', 'III', '7560860551', 'MC-2', '10:10-10:35Am'),

-- MC-3 (10:35-11:00Am)
('Devna Mohanan', 'Duo Dance', 'I', '8606390525', 'MC-3', '10:35-11:00Am'),
('Antonia Elizabeth', 'Group Dance', 'II', '8590456825', 'MC-3', '10:35-11:00Am'),
('Devanjana', 'Group Dance', 'II', '8891789148', 'MC-3', '10:35-11:00Am'),
('Afsal', 'Group Dance', 'I', '9633801508', 'MC-3', '10:35-11:00Am'),
('Sillambazhagi', 'Stick Dance', 'III', '9043571145', 'MC-3', '10:35-11:00Am'),
('Ananya', 'Group Dance', 'II', '8075010479', 'MC-3', '10:35-11:00Am'),

-- MC-4 (11:00-11:25Am)
('Mohammed Shamoor', 'Group Dance', 'II', '9567266227', 'MC-4', '11:00-11:25Am'),
('Anvika Pramod', 'Group Dance', 'I', '8089034221', 'MC-4', '11:00-11:25Am'),
('Fathima Noora', 'Group Dance', 'I', '6235827872', 'MC-4', '11:00-11:25Am'),
('Fathiamath nafiya', 'Group Dance', 'III', '9747580616', 'MC-4', '11:00-11:25Am'),
('Aakil P P', 'Song', 'II', '9188294280', 'MC-4', '11:00-11:25Am'),
('Neha Sreejith', 'Group Dance', 'III', '7736502367', 'MC-4', '11:00-11:25Am'),

-- MC-5 (11:25-12:00PM)
('Mohammed Rafi T A', 'Group Dance', 'I', '6235154329', 'MC-5', '11:25-12:00PM'),
('Alona', 'Group Dance', 'II', '7025912439', 'MC-5', '11:25-12:00PM'),
('DevaSurya', 'Group Dance', 'II', '9400716943', 'MC-5', '11:25-12:00PM'),
('Niya', 'Group Dance', 'II', '7736534948', 'MC-5', '11:25-12:00PM'),
('Mohammed Nazim', 'Group Dance', 'III', '9037018545', 'MC-5', '11:25-12:00PM'),
('Rania', 'Group Dance', 'II', NULL, 'MC-5', '11:25-12:00PM'),
('Rajid', 'Group Dance', 'III', '8129282290', 'MC-5', '11:25-12:00PM'),
('Gourav', 'Group Dance', 'II', '7994470146', 'MC-5', '11:25-12:00PM'),

-- MC-6 (12:00PM-12:30PM)
('Asad Ali', 'Dance', 'II', NULL, 'MC-6', '12:00PM-12:30PM'),
('Surya Priya', 'Dance', 'III', '8590153302', 'MC-6', '12:00PM-12:30PM'),
('Amna', 'Group Dance', 'I', '8129546675', 'MC-6', '12:00PM-12:30PM'),
('Zia', 'Solo Dance', 'I', '9037866766', 'MC-6', '12:00PM-12:30PM'),
('Mazin', 'Group Dance', 'II', '7306654922', 'MC-6', '12:00PM-12:30PM'),
('Rihan', 'Group Dance', 'I', '6363921190', 'MC-6', '12:00PM-12:30PM'),

-- MC-7 - Ramp Walk (12:30-1:00PM)
('Third years', 'Ramp Walk', 'III', NULL, 'MC-7', '12:30-1:00PM'),
('Second years', 'Ramp Walk', 'II', NULL, 'MC-7', '12:30-1:00PM'),
('First years', 'Ramp Walk', 'I', NULL, 'MC-7', '12:30-1:00PM'),

-- Band (1:10-1:30PM)
('Shivaganga', 'Song', 'Band', '6235182816', 'Band', '1:10-1:30PM'),
('Nihal N', 'Song', 'Band', NULL, 'Band', '1:10-1:30PM'),
('Zaied', 'Song', 'Band', '9495840773', 'Band', '1:10-1:30PM'),
('Mohammed Ubaid', 'Song', 'Band', '9663661357', 'Band', '1:10-1:30PM');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_performance_completed ON performance(is_completed);
CREATE INDEX IF NOT EXISTS idx_performance_mc_session ON performance(mc_session);
CREATE INDEX IF NOT EXISTS idx_performance_year ON performance(year);