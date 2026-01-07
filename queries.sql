-- queries.sql

-- 1) отримати всі завдання певного користувача (за user_id)
SELECT *
FROM tasks
WHERE user_id = 1;

-- 2) вибрати завдання за певним статусом (наприклад 'new') через підзапит
SELECT *
FROM tasks
WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- 3) оновити статус конкретного завдання (наприклад task id = 5 -> 'in progress')
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 5;

-- 4) отримати список користувачів, які не мають жодного завдання (select + where not in + підзапит)
SELECT *
FROM users
WHERE id NOT IN (SELECT user_id FROM tasks);

-- 5) додати нове завдання для конкретного користувача
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
  'new task title',
  'some description',
  (SELECT id FROM status WHERE name = 'new'),
  1
);

-- 6) отримати всі завдання, які ще не завершено
SELECT t.*
FROM tasks t
JOIN status s ON s.id = t.status_id
WHERE s.name <> 'completed';

-- 7) видалити конкретне завдання (за id)
DELETE FROM tasks
WHERE id = 10;

-- 8) знайти користувачів з певною електронною поштою (like)
SELECT *
FROM users
WHERE email LIKE '%gmail%';

-- 9) оновити ім'я користувача
UPDATE users
SET fullname = 'updated name'
WHERE id = 1;

-- 10) отримати кількість завдань для кожного статусу (select count group by)
SELECT s.name, COUNT(t.id) AS task_count
FROM status s
LEFT JOIN tasks t ON t.status_id = s.id
GROUP BY s.name
ORDER BY s.name;

-- 11) отримати завдання, призначені користувачам з певним доменом пошти (join + like)
SELECT t.*
FROM tasks t
JOIN users u ON u.id = t.user_id
WHERE u.email LIKE '%@example.com';

-- 12) отримати список завдань, що не мають опису
SELECT *
FROM tasks
WHERE description IS NULL OR TRIM(description) = '';

-- 13) вибрати користувачів та їхні завдання зі статусом 'in progress' (inner join)
SELECT u.fullname, u.email, t.id AS task_id, t.title
FROM users u
INNER JOIN tasks t ON t.user_id = u.id
INNER JOIN status s ON s.id = t.status_id
WHERE s.name = 'in progress';

-- 14) отримати користувачів та кількість їхніх завдань (left join + group by)
SELECT u.id, u.fullname, u.email, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON t.user_id = u.id
GROUP BY u.id, u.fullname, u.email
ORDER BY task_count DESC, u.id;
