CREATE TABLE users (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(150) UNIQUE NOT NULL,
    password VARCHAR2(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE users_seq
START WITH 1
INCREMENT BY 1;

CREATE OR REPLACE TRIGGER users_trigger
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := users_seq.NEXTVAL;
    END IF;
END;
/

CREATE TABLE repositories (
    id NUMBER PRIMARY KEY,
    user_id NUMBER NOT NULL,
    github_url VARCHAR2(500) NOT NULL,
    name VARCHAR2(255),
    description VARCHAR2(4000),
    language VARCHAR2(100),
    stars NUMBER DEFAULT 0,
    forks NUMBER DEFAULT 0,
    files CLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE repositories
ADD CONSTRAINT fk_repository_user
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;

CREATE SEQUENCE repositories_seq
START WITH 1
INCREMENT BY 1;

CREATE OR REPLACE TRIGGER repositories_trigger
BEFORE INSERT ON repositories
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := repositories_seq.NEXTVAL;
    END IF;
END;
/

CREATE TABLE analyses (
    id NUMBER PRIMARY KEY,
    repository_id NUMBER NOT NULL,
    summary CLOB,
    technologies CLOB,
    architecture CLOB,
    important_files CLOB,
    suggestions CLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE analyses
ADD CONSTRAINT fk_analysis_repository
FOREIGN KEY (repository_id)
REFERENCES repositories(id)
ON DELETE CASCADE;

CREATE SEQUENCE analyses_seq
START WITH 1
INCREMENT BY 1;

CREATE OR REPLACE TRIGGER analyses_trigger
BEFORE INSERT ON analyses
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := analyses_seq.NEXTVAL;
    END IF;
END;
/