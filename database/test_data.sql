INSERT INTO ecosystem(id, name, description) VALUES(1, 'Python', 'Python');
INSERT INTO ecosystem(id, name, description) VALUES(2, 'Java', 'Java');
INSERT INTO ecosystem(id, name, description) VALUES(3, 'JavaScript', 'JavaScript');

INSERT INTO package_index(id, ecosystem, name, url) VALUES(1, 1, 'Python Package Index', 'https://pypi.org/');
INSERT INTO package_index(id, ecosystem, name, url) VALUES(2, 2, 'Maven', 'https://maven.apache.org/');
INSERT INTO package_index(id, ecosystem, name, url) VALUES(3, 3, 'npm', 'https://www.npmjs.com/');
