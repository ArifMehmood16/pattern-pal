import json
import sqlite3
from pathlib import Path

setup='''CREATE TABLE departments(id INTEGER PRIMARY KEY,name TEXT);
INSERT INTO departments VALUES(1,'Engineering'),(2,'Product'),(3,'Operations');
CREATE TABLE employees(id INTEGER PRIMARY KEY,name TEXT,salary INTEGER,department_id INTEGER,manager_id INTEGER);
INSERT INTO employees VALUES(1,'Ada',100,1,NULL),(2,'Ben',80,1,1),(3,'Cara',120,1,1),(4,'Dan',100,1,1),(5,'Eli',90,1,1),(6,'Fay',70,1,1),(7,'Gia',150,2,NULL),(8,'Hao',130,2,7),(9,'Ivy',130,2,7),(10,'Jay',NULL,2,7);
CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT);
INSERT INTO customers VALUES(1,'Ada'),(2,'Ben'),(3,'Cara'),(4,'Zed');
CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER,amount INTEGER,order_date TEXT,status TEXT);
INSERT INTO orders VALUES(1,1,100,'2026-01-01','paid'),(2,1,50,'2026-01-02','paid'),(3,2,80,'2026-01-02','paid'),(4,4,20,'2026-01-03','cancelled');
CREATE TABLE contacts(id INTEGER PRIMARY KEY,email TEXT);
INSERT INTO contacts VALUES(1,'a@example.com'),(2,'b@example.com'),(3,'a@example.com'),(4,NULL),(5,NULL);
CREATE TABLE scores(id INTEGER PRIMARY KEY,student TEXT,score INTEGER);
INSERT INTO scores VALUES(1,'A',90),(2,'B',90),(3,'C',80),(4,'D',70);
CREATE TABLE logs(id INTEGER PRIMARY KEY,num INTEGER);
INSERT INTO logs VALUES(1,1),(2,1),(3,1),(4,2),(5,1),(6,2),(7,2),(8,2);
CREATE TABLE weather(id INTEGER PRIMARY KEY,record_date TEXT,temperature INTEGER);
INSERT INTO weather VALUES(1,'2026-01-01',10),(2,'2026-01-02',20),(3,'2026-01-03',15),(4,'2026-01-04',30);
CREATE TABLE enrollment(student TEXT,course TEXT);
INSERT INTO enrollment VALUES('A','math'),('B','math'),('C','math'),('D','math'),('E','math'),('A','english'),('B','english');
CREATE TABLE signups(user_id INTEGER PRIMARY KEY);
INSERT INTO signups VALUES(1),(2),(3);
CREATE TABLE confirmations(user_id INTEGER,action TEXT);
INSERT INTO confirmations VALUES(1,'confirmed'),(1,'timeout'),(2,'confirmed'),(2,'confirmed');
CREATE TABLE activity(player_id INTEGER,event_date TEXT);
INSERT INTO activity VALUES(1,'2026-01-01'),(1,'2026-01-02'),(2,'2026-01-01'),(2,'2026-01-03'),(3,'2026-01-05');
CREATE TABLE sales(id INTEGER PRIMARY KEY,product_id INTEGER,quantity INTEGER,revenue INTEGER);
INSERT INTO sales VALUES(1,101,2,20),(2,102,1,15),(3,101,3,30);
CREATE TABLE countries(name TEXT,area INTEGER,population INTEGER);
INSERT INTO countries VALUES('A',4000000,1000000),('B',1000000,30000000),('C',1000000,1000000);
CREATE TABLE products(id INTEGER PRIMARY KEY,low_fats TEXT,recyclable TEXT);
INSERT INTO products VALUES(1,'Y','Y'),(2,'Y','N'),(3,'N','Y');'''
lessons=[]
def Q(title,category,prompt,code,tables,expected,steps,trap,pg=None,priority='Next'):
    db=sqlite3.connect(':memory:');db.executescript(setup)
    result=db.execute(code);columns=[c[0] for c in result.description];rows=[list(r) for r in result.fetchall()]
    assert rows==expected,(title,rows,expected)
    inputs=[]
    for table in tables:
        cursor=db.execute(f'SELECT * FROM {table}')
        inputs.append(dict(name=table,columns=[c[0] for c in cursor.description],values=[list(r) for r in cursor.fetchall()]))
    db.close()
    lessons.append(dict(id=len(lessons),title=title,category=category,prompt=prompt,code=code.strip(),postgres=pg.strip() if pg else code.strip(),
                        inputs=inputs,setup=setup,expected=dict(columns=columns,values=rows),steps=steps,trap=trap,priority=priority))

Q('Big Countries','Filtering','Return countries with area ≥ 3,000,000 OR population ≥ 25,000,000. Sort by name.',
  'SELECT name FROM countries WHERE area >= 3000000 OR population >= 25000000 ORDER BY name;', ['countries'],[['A'],['B']],
  ['FROM starts with every country.','WHERE retains a row satisfying either condition.','SELECT projects name; ORDER BY makes output deterministic.'], 'OR and AND express different contracts.',priority='Tonight')
Q('Recyclable and Low Fat Products','Filtering','Return IDs whose low_fats and recyclable flags are both Y; sort IDs.',
  "SELECT id FROM products WHERE low_fats = 'Y' AND recyclable = 'Y' ORDER BY id;",['products'],[[1]],
  ['Filter both columns with AND.','Project the ID and sort it.'],'Use single quotes for text literals.',priority='Tonight')
Q('Customers Who Never Order','Joins','Return customers with no order of any status, sorted by ID.',
  '''SELECT c.id, c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL
ORDER BY c.id;''',['customers','orders'],[[3,'Cara']],
  ['LEFT JOIN preserves each customer, even with no matched order.','Unmatched order IDs are NULL.','Filter the missing match and sort customer IDs.'],'A filter on a right-table column in WHERE can unintentionally turn a LEFT JOIN into an inner join.',priority='Tonight')
Q('Employees Earning More Than Managers','Joins','Return employees whose salary exceeds their manager’s salary; sort IDs.',
  '''SELECT e.id, e.name
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary
ORDER BY e.id;''',['employees'],[[3,'Cara']],
  ['Use two aliases for the same table: employee and manager.','Join on the manager’s ID, not department.','Compare salaries; NULL salary comparisons do not evaluate True.'],'A self-join represents two different roles, not duplicate output by itself.',priority='Tonight')
Q('Duplicate Emails','Grouping','Return each non-NULL email occurring more than once, sorted alphabetically.',
  '''SELECT email
FROM contacts
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY email;''',['contacts'],[['a@example.com']],
  ['Exclude NULL emails before grouping.','Group identical emails and count rows.','HAVING filters groups after aggregation.'],'WHERE filters input rows; HAVING filters aggregated groups.',priority='Tonight')
Q('Second Highest Salary','Subqueries','Return one row with the second-highest distinct non-NULL salary, or NULL if absent.',
  '''SELECT MAX(salary) AS second_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);''',['employees'],[[130]],
  ['The subquery obtains the highest salary.','Keep only salaries strictly below it, excluding all ties for first.','MAX on those remaining values is second highest; an empty aggregate yields NULL.'],'Second employee is different from second distinct salary.',priority='Tonight')
Q('Nth Highest Distinct Salary','Ranking','For n=3, return the third-highest distinct salary, or NULL if absent.',
  '''WITH ranked AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS position
  FROM employees WHERE salary IS NOT NULL
)
SELECT MAX(salary) AS third_salary FROM ranked WHERE position = 3;''',['employees'],[[120]],
  ['Filter NULL salaries before ranking.','DENSE_RANK assigns one consecutive rank per distinct salary.','Filter rank 3 in an outer query and use MAX to return exactly one row.'],'Filter window results in an outer query or CTE, not the same SELECT’s WHERE.',priority='Tonight')
Q('Department Highest Salary','Ranking','Return every employee tied for highest salary in each department. Sort department and employee IDs.',
  '''WITH ranked AS (
  SELECT e.*, DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS position
  FROM employees e WHERE salary IS NOT NULL
)
SELECT d.name AS department, r.name AS employee, r.salary
FROM ranked r JOIN departments d ON d.id = r.department_id
WHERE position = 1
ORDER BY d.id, r.id;''',['employees','departments'],[['Engineering','Cara',120],['Product','Gia',150]],
  ['PARTITION BY restarts ranking for each department.','Ranking excludes unknown salaries.','Join department labels and retain every rank-one row.'],'ROW_NUMBER would arbitrarily keep one tie rather than all top earners.',priority='Tonight')
Q('Department Top Three Salaries','Ranking','Return employees in each department’s top three distinct salary levels; keep ties.',
  '''WITH ranked AS (
  SELECT e.*, DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS position
  FROM employees e WHERE salary IS NOT NULL
)
SELECT department_id, name, salary
FROM ranked WHERE position <= 3
ORDER BY department_id, salary DESC, id;''',['employees'],[[1,'Cara',120],[1,'Ada',100],[1,'Dan',100],[1,'Eli',90],[2,'Gia',150],[2,'Hao',130],[2,'Ivy',130]],
  ['Rank distinct salaries independently per department.','Keep ranks 1–3, possibly yielding more than three employees.','Add a deterministic tie-breaker in the final ORDER BY.'],'ROW_NUMBER, RANK and DENSE_RANK have different tie and gap semantics.')
Q('Rank Scores','Ranking','Return students and their dense rank by score, highest first; break output ties by ID.',
  '''SELECT student, score,
       DENSE_RANK() OVER (ORDER BY score DESC) AS position
FROM scores ORDER BY score DESC, id;''',['scores'],[['A',90,1],['B',90,1],['C',80,2],['D',70,3]],
  ['Use score alone in the window ordering so equal scores tie.','The outer ORDER BY includes ID for repeatable presentation.'],'Adding ID to DENSE_RANK’s ORDER BY would destroy the score ties.',priority='Tonight')
Q('Consecutive Numbers','Window functions','Return numbers occurring in at least three consecutive log rows ordered by ID; return each once.',
  '''WITH history AS (
  SELECT num, LAG(num,1) OVER (ORDER BY id) AS previous,
         LAG(num,2) OVER (ORDER BY id) AS two_back
  FROM logs
)
SELECT DISTINCT num FROM history
WHERE num = previous AND num = two_back ORDER BY num;''',['logs'],[[1],[2]],
  ['LAG retrieves values one and two rows before the current row.','A current value matching both proves a run of three.','DISTINCT prevents a longer run from appearing repeatedly.'],'This contract means consecutive rows in ID order, not necessarily consecutive numeric IDs.')
Q('Rising Temperature','Dates','Return weather IDs warmer than the previous calendar day; sort IDs.',
  '''SELECT today.id
FROM weather today
JOIN weather yesterday ON today.record_date = date(yesterday.record_date, '+1 day')
WHERE today.temperature > yesterday.temperature
ORDER BY today.id;''',['weather'],[[2],[4]],
  ['Self-join weather on a calendar-day relation.','Compare temperatures after joining the correct day.'],'LAG alone compares the previous available row, which may not be the previous calendar day.',
  pg='''SELECT today.id FROM weather today
JOIN weather yesterday ON today.record_date::date = yesterday.record_date::date + 1
WHERE today.temperature > yesterday.temperature ORDER BY today.id;''')
Q('Managers With Five Direct Reports','Grouping','Return manager IDs and names with at least five direct reports; sort IDs.',
  '''SELECT m.id, m.name
FROM employees m JOIN employees e ON e.manager_id = m.id
GROUP BY m.id, m.name HAVING COUNT(*) >= 5 ORDER BY m.id;''',['employees'],[[1,'Ada']],
  ['Join employees to their direct managers.','Group the joined rows by manager.','HAVING checks the direct-report count.'],'Descendants below direct reports are not counted by this join.')
Q('Classes With At Least Five Students','Grouping','Return classes with at least five distinct students; sort course names.',
  '''SELECT course FROM enrollment
GROUP BY course HAVING COUNT(DISTINCT student) >= 5 ORDER BY course;''',['enrollment'],[['math']],
  ['Group enrollments by course.','Count distinct student identifiers so duplicate enrollment records would not inflate the answer.'],'COUNT(*) and COUNT(DISTINCT student) differ when duplicate records exist.',priority='Tonight')
Q('Confirmation Rate','Conditional aggregation','For every signup, return confirmed attempts divided by all attempts, rounded to two decimals; no attempts means 0.',
  '''SELECT s.user_id,
       ROUND(COALESCE(1.0 * SUM(CASE WHEN c.action = 'confirmed' THEN 1 ELSE 0 END)
                      / NULLIF(COUNT(c.action),0), 0), 2) AS rate
FROM signups s LEFT JOIN confirmations c ON c.user_id = s.user_id
GROUP BY s.user_id ORDER BY s.user_id;''',['signups','confirmations'],[[1,0.5],[2,1.0],[3,0.0]],
  ['LEFT JOIN includes users with no attempts.','CASE counts confirmed attempts; COUNT(c.action) ignores the NULL placeholder for no match.','Use 1.0 to force noninteger division, NULLIF for a zero denominator, then COALESCE.'],'COUNT(*) would count the unmatched placeholder row. PostgreSQL may need a numeric cast when adapting floating expressions for ROUND.',priority='Tonight')
Q('Paid Revenue by Customer','Grouping','Include every customer. Sum only paid order amounts; customers without paid orders receive zero.',
  '''SELECT c.id, c.name, COALESCE(SUM(o.amount),0) AS revenue
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'paid'
GROUP BY c.id, c.name ORDER BY c.id;''',['customers','orders'],[[1,'Ada',150],[2,'Ben',80],[3,'Cara',0],[4,'Zed',0]],
  ['Put the paid-status restriction inside ON to preserve unmatched customers.','Group each customer’s paid matches.','SUM over no matches is NULL; COALESCE converts it to zero.'],'WHERE o.status = paid would remove zero-revenue customers.',priority='Tonight')
Q('Running Revenue','Window functions','Aggregate paid revenue by date, then show its cumulative total in chronological order.',
  '''WITH daily AS (
  SELECT order_date, SUM(amount) AS revenue FROM orders
  WHERE status = 'paid' GROUP BY order_date
)
SELECT order_date, revenue,
       SUM(revenue) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM daily ORDER BY order_date;''',['orders'],[['2026-01-01',100,100],['2026-01-02',130,230]],
  ['First collapse multiple orders on one date into one daily row.','Then sum the daily values over an explicit growing ROWS frame.'],'Aggregates collapse rows; window aggregates retain each row. Use an explicit frame when duplicates matter.',priority='Tonight')
Q('Rolling Two-Row Average','Window functions','For each paid-revenue date, show the average of that row and the preceding revenue row, rounded to two decimals.',
  '''WITH daily AS (
  SELECT order_date, SUM(amount) AS revenue FROM orders
  WHERE status = 'paid' GROUP BY order_date
)
SELECT order_date,
       ROUND(AVG(revenue) OVER (ORDER BY order_date ROWS BETWEEN 1 PRECEDING AND CURRENT ROW),2) AS moving_average
FROM daily ORDER BY order_date;''',['orders'],[['2026-01-01',100.0],['2026-01-02',115.0]],
  ['Group daily revenue before applying the window.','The first row has only itself in its frame.','The next row averages two revenue rows.'],'Two rows is not necessarily two calendar days if dates are missing.')
Q('First Login per Player','Grouping','Return each player’s first login date, sorted by player ID.',
  '''SELECT player_id, MIN(event_date) AS first_login
FROM activity GROUP BY player_id ORDER BY player_id;''',['activity'],[[1,'2026-01-01'],[2,'2026-01-01'],[3,'2026-01-05']],
  ['Group by player ID and take the earliest date.'],'The sample stores dates in ISO YYYY-MM-DD text; its lexical ordering matches calendar ordering.',priority='Tonight')
Q('Next-Day Retention','Dates','Return the fraction of players who log in on the day immediately after their first login, rounded to two decimals.',
  '''WITH first_login AS (
  SELECT player_id, MIN(event_date) AS first_day FROM activity GROUP BY player_id
)
SELECT ROUND(AVG(CASE WHEN EXISTS (
  SELECT 1 FROM activity a WHERE a.player_id = f.player_id
  AND a.event_date = date(f.first_day, '+1 day')
) THEN 1.0 ELSE 0.0 END),2) AS fraction FROM first_login f;''',['activity'],[[0.33]],
  ['Create one first-login row per player.','EXISTS tests next-calendar-day activity without multiplying the player row.','Average the one/zero indicators.'],'Joining all later activity can double count players. EXISTS preserves one vote per player.',
  pg='''WITH first_login AS (
 SELECT player_id, MIN(event_date::date) AS first_day FROM activity GROUP BY player_id
)
SELECT ROUND(AVG(CASE WHEN EXISTS (
 SELECT 1 FROM activity a WHERE a.player_id = f.player_id
 AND a.event_date::date = f.first_day + 1
) THEN 1.0 ELSE 0.0 END),2) AS fraction FROM first_login f;''')
Q('Product Sales Totals','Grouping','Return total quantity and revenue by product ID, sorted by product ID.',
  '''SELECT product_id, SUM(quantity) AS units, SUM(revenue) AS revenue
FROM sales GROUP BY product_id ORDER BY product_id;''',['sales'],[[101,5,50],[102,1,15]],
  ['Group repeated product sales into one row.','Aggregate quantity and revenue independently.'],'Do not SUM unit price when the contract asks for revenue.')
Q('Employees Above Department Average','CTEs','Return non-NULL-salary employees whose salary is above their department’s average, sorted by ID.',
  '''WITH averages AS (
  SELECT department_id, AVG(salary) AS mean_salary FROM employees GROUP BY department_id
)
SELECT e.id,e.name FROM employees e
JOIN averages a ON a.department_id = e.department_id
WHERE e.salary > a.mean_salary ORDER BY e.id;''',['employees'],[[1,'Ada'],[3,'Cara'],[4,'Dan'],[7,'Gia']],
  ['Calculate one average per department; AVG ignores NULL salaries.','Join each employee to their department statistic.','Keep only salaries strictly above it.'],'A correlated subquery or window AVG can express the same logic.')
Q('Find Redundant Email Records','Ranking','For non-NULL duplicate emails, keep the lowest ID and return the redundant IDs.',
  '''WITH numbered AS (
  SELECT id,email, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS position
  FROM contacts WHERE email IS NOT NULL
)
SELECT id,email FROM numbered WHERE position > 1 ORDER BY id;''',['contacts'],[[3,'a@example.com']],
  ['Exclude NULL emails because this contract treats missing emails independently.','ROW_NUMBER picks an unambiguous first record using ID.','Return later records without deleting anything.'],'Ranking is a read-only preview here. Real deletion would require a carefully scoped transaction.')
Q('UNION Versus UNION ALL','Set operations','Combine names from employees ID ≤ 2 and customers ID ≤ 3. Return each distinct name once, alphabetically.',
  '''SELECT name FROM employees WHERE id <= 2
UNION
SELECT name FROM customers WHERE id <= 3
ORDER BY name;''',['employees','customers'],[['Ada'],['Ben'],['Cara']],
  ['Each SELECT projects a compatible name column.','UNION removes duplicate complete result rows.','The final ORDER BY applies to the combined result.'],'UNION ALL preserves duplicates and often avoids deduplication work.',priority='Tonight')
Q('Consecutive Login Streaks','Dates','Return runs of at least two consecutive calendar login days per player. Deduplicate same-day logins first.',
  '''WITH days AS (
  SELECT DISTINCT player_id,event_date FROM activity
), numbered AS (
  SELECT player_id,event_date,
         julianday(event_date) - ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY event_date) AS island
  FROM days
)
SELECT player_id,MIN(event_date) AS start_day,MAX(event_date) AS end_day,COUNT(*) AS length
FROM numbered GROUP BY player_id,island HAVING COUNT(*) >= 2
ORDER BY player_id,start_day;''',['activity'],[[1,'2026-01-01','2026-01-02',2]],
  ['Remove repeated login dates before assigning row numbers.','For consecutive days, calendar ordinal minus row number stays constant.','Group that island key and retain qualifying runs.'],'Day ordinals are SQLite julianday here. PostgreSQL uses date arithmetic; the two versions are shown explicitly.',
  pg='''WITH days AS (SELECT DISTINCT player_id,event_date::date AS event_date FROM activity),
numbered AS (
 SELECT player_id,event_date,
 event_date - (ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY event_date))::integer AS island
 FROM days
)
SELECT player_id,MIN(event_date) AS start_day,MAX(event_date) AS end_day,COUNT(*) AS length
FROM numbered GROUP BY player_id,island HAVING COUNT(*) >= 2 ORDER BY player_id,start_day;''',priority='Stretch')

assert len(lessons)==25
stage_queries={
 'Customers Who Never Order':[('After LEFT JOIN · matched and unmatched customers', 'SELECT c.id,c.name,o.id AS order_id FROM customers c LEFT JOIN orders o ON c.id=o.customer_id ORDER BY c.id,o.id')],
 'Employees Earning More Than Managers':[('After self-join · the two salary roles','SELECT e.name AS employee,e.salary,m.name AS manager,m.salary AS manager_salary FROM employees e JOIN employees m ON e.manager_id=m.id ORDER BY e.id')],
 'Duplicate Emails':[('After grouping · counts before HAVING','SELECT email,COUNT(*) AS occurrences FROM contacts WHERE email IS NOT NULL GROUP BY email ORDER BY email')],
 'Second Highest Salary':[('After removing the highest distinct salary','SELECT DISTINCT salary FROM employees WHERE salary<(SELECT MAX(salary) FROM employees) ORDER BY salary DESC')],
 'Department Highest Salary':[('After department partitioning and dense ranking','SELECT department_id,name,salary,DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS position FROM employees WHERE salary IS NOT NULL ORDER BY department_id,salary DESC,id')],
 'Department Top Three Salaries':[('All ranks before the top-three filter','SELECT department_id,name,salary,DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS position FROM employees WHERE salary IS NOT NULL ORDER BY department_id,salary DESC,id')],
 'Rank Scores':[('Compare tie semantics · same input, three different rankings','SELECT student,score,ROW_NUMBER() OVER (ORDER BY score DESC,id) AS row_number,RANK() OVER (ORDER BY score DESC) AS rank_with_gaps,DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank FROM scores ORDER BY score DESC,id')],
 'Consecutive Numbers':[('Window state · every current and prior value','SELECT id,num,LAG(num,1) OVER (ORDER BY id) AS previous,LAG(num,2) OVER (ORDER BY id) AS two_back FROM logs ORDER BY id')],
 'Confirmation Rate':[('After LEFT JOIN · note the NULL row for signup 3','SELECT s.user_id,c.action FROM signups s LEFT JOIN confirmations c ON s.user_id=c.user_id ORDER BY s.user_id,c.action'),('After counting · numerator and denominator','SELECT s.user_id,SUM(CASE WHEN c.action=\'confirmed\' THEN 1 ELSE 0 END) AS confirmed,COUNT(c.action) AS attempts FROM signups s LEFT JOIN confirmations c ON s.user_id=c.user_id GROUP BY s.user_id ORDER BY s.user_id')],
 'Paid Revenue by Customer':[('After paid-only LEFT JOIN · zero-revenue customers remain','SELECT c.id,c.name,o.id AS paid_order_id,o.amount FROM customers c LEFT JOIN orders o ON o.customer_id=c.id AND o.status=\'paid\' ORDER BY c.id,o.id')],
 'Running Revenue':[('Daily CTE before applying the cumulative window','SELECT order_date,SUM(amount) AS revenue FROM orders WHERE status=\'paid\' GROUP BY order_date ORDER BY order_date')],
 'Rolling Two-Row Average':[('Daily rows before evaluating each two-row frame','SELECT order_date,SUM(amount) AS revenue FROM orders WHERE status=\'paid\' GROUP BY order_date ORDER BY order_date')],
 'Find Redundant Email Records':[('Every numbered non-NULL email record before filtering','SELECT id,email,ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS position FROM contacts WHERE email IS NOT NULL ORDER BY id')],
 'Employees Above Department Average':[('One average per department · NULL salaries excluded by AVG','SELECT department_id,AVG(salary) AS mean_salary FROM employees GROUP BY department_id ORDER BY department_id')],
}
for lesson in lessons:
    db=sqlite3.connect(':memory:');db.executescript(setup);lesson['stages']=[]
    for name,query in stage_queries.get(lesson['title'],[]):
        cursor=db.execute(query);lesson['stages'].append({'name':name,'columns':[c[0] for c in cursor.description],'values':[list(r) for r in cursor.fetchall()]})
    db.close()
foundations=[
 ['Logical query order','FROM/JOIN → WHERE → GROUP BY → HAVING → window calculations → SELECT → DISTINCT → ORDER BY → LIMIT. This is a reasoning model, not the physical execution plan.'],
 ['NULL and three-valued logic','= NULL is not a NULL check. Use IS NULL / IS NOT NULL. WHERE retains only True; False and Unknown are rejected. COUNT(column) ignores NULL; COUNT(*) counts rows.'],
 ['Anti-joins','NOT EXISTS avoids the NULL trap in NOT IN. If a NOT IN subquery returns NULL, otherwise-unmatched comparisons can become Unknown.'],
 ['Join multiplicity','One-to-many joins multiply rows. Aggregate each many-side first when joining multiple detail tables, or you can multiply sums. DISTINCT is not a universal fix.'],
 ['LEFT JOIN filters','A right-side filter in WHERE can discard unmatched rows. Put matching restrictions in ON when you must preserve every left-side row.'],
 ['Grouping','Every selected nonaggregate expression must be grouped or supported by the engine’s functional-dependency rules. Write explicit GROUP BY columns for portable clarity.'],
 ['Ranking','ROW_NUMBER numbers every row; include a deterministic tie-breaker. RANK leaves gaps after ties. DENSE_RANK has no gaps between distinct levels.'],
 ['Window frames','ROWS counts physical rows; RANGE groups peer values under ordering. Explicit ROWS frames avoid surprising cumulative totals on tied sort keys.'],
 ['Integer division and zero','Cast or multiply by 1.0 before dividing integer counts. Use NULLIF(denominator,0), then decide whether NULL or zero is the intended result.'],
 ['Date dialects','The verified sample queries use SQLite with ISO date text. PostgreSQL references use casts, date + integer or intervals. MySQL date functions differ; confirm the actual assessment dialect.'],
 ['CTEs and subqueries','CTEs name intermediate relations and improve readability. Do not assume they always materialise or always improve performance; inspect the plan.'],
 ['Indexes and EXPLAIN','Indexes can help filters/joins/order, but add write and storage cost. Composite-key order matters. Use EXPLAIN to inspect access strategy; PostgreSQL EXPLAIN ANALYZE executes the query.'],
 ['Transactions and constraints','BEGIN/COMMIT make a unit of work atomic; ROLLBACK undoes it. UNIQUE, PRIMARY KEY, FOREIGN KEY and CHECK express invariants. Isolation level determines allowed concurrent anomalies.'],
 ['Safe parameterisation','Pass values as bound parameters via your database driver. Do not interpolate untrusted input into SQL. Parameters represent values, not arbitrary identifiers.'],
]
Path('src/data/sql-lessons.json').write_text(json.dumps(dict(lessons=lessons,foundations=foundations,sources=[
 ['PostgreSQL window functions','https://www.postgresql.org/docs/current/tutorial-window.html'],
 ['PostgreSQL date functions','https://www.postgresql.org/docs/current/functions-datetime.html'],
 ['SQLite window functions','https://www.sqlite.org/windowfunctions.html']]),ensure_ascii=False,indent=2))
print('PASS: all 25 SQL reference queries produce their independently specified expected tables.')
