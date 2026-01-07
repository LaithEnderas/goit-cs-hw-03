# seed.py
# fills users status tasks with fake data

import os
import argparse
import random

import psycopg2
from psycopg2.extras import execute_values
from faker import Faker


def get_conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "task_manager"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
    )


def reset_tables(cur):
    cur.execute("TRUNCATE TABLE tasks, users, status RESTART IDENTITY;")


def seed_statuses(cur):
    statuses = [("new",), ("in progress",), ("completed",)]
    execute_values(
        cur,
        "INSERT INTO status (name) VALUES %s ON CONFLICT (name) DO NOTHING;",
        statuses,
    )
    cur.execute("SELECT id, name FROM status;")
    return {name: sid for sid, name in cur.fetchall()}


def seed_users(cur, fake, n_users):
    rows = []
    for _ in range(n_users):
        rows.append((fake.name(), fake.unique.email()))
    execute_values(cur, "INSERT INTO users (fullname, email) VALUES %s;", rows)

    cur.execute("SELECT id FROM users;")
    return [r[0] for r in cur.fetchall()]


def seed_tasks(cur, fake, user_ids, status_ids, n_tasks, no_desc_ratio):
    status_id_list = list(status_ids.values())

    rows = []
    for _ in range(n_tasks):
        title = fake.sentence(nb_words=4)[:100].rstrip(".")
        if random.random() < no_desc_ratio:
            description = None
        else:
            description = fake.paragraph(nb_sentences=3)

        rows.append(
            (
                title,
                description,
                random.choice(status_id_list),
                random.choice(user_ids),
            )
        )

    execute_values(
        cur,
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES %s;",
        rows,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--users", type=int, default=20)
    parser.add_argument("--tasks", type=int, default=100)
    parser.add_argument("--locale", type=str, default="uk_UA")
    parser.add_argument("--no-desc-ratio", type=float, default=0.2)
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    fake = Faker(args.locale)
    Faker.seed(42)
    random.seed(42)

    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                if args.reset:
                    reset_tables(cur)

                status_ids = seed_statuses(cur)
                user_ids = seed_users(cur, fake, args.users)
                seed_tasks(cur, fake, user_ids, status_ids, args.tasks, args.no_desc_ratio)

        print("seed completed")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
