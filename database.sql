
CREATE TABLE students(id INTEGER PRIMARY KEY, name TEXT, code TEXT, teacher TEXT, points INTEGER);
CREATE TABLE attendance(id INTEGER PRIMARY KEY, code TEXT, date TEXT, status TEXT);
INSERT INTO students(name,code,teacher,points) VALUES
('Ahmed Ali','GDO-ST-001','Mr Ahmed',100),
('Sara Mohamed','GDO-ST-002','Ms Mona',95);
