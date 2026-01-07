# create_tables.py
# creates tables users status tasks in postgresql

import os
import psycopg2


def get_conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "task_manager"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
    )


DDL = """
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE status (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  status_id INTEGER NOT NULL REFERENCES status(id),
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status_id ON tasks(status_id);
"""


def main():
    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(DDL)
        print("tables created")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
