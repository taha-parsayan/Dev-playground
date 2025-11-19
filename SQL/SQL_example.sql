-- ---------- Basic skills -----------

-- select all
SELECT *
FROM employee_demographics;

-- unique
SELECT DISTINCT gender
FROM employee_demographics;

-- where
Select *
FROM employee_demographics
WHERE age > 30;

Select *
FROM employee_demographics
WHERE first_name = 'Tom';

-- AND, OR, NOT
Select *
FROM employee_demographics
WHERE age > 30 AND gender = 'Male'; 

-- LIKE, _
Select *
FROM employee_demographics
WHERE first_name LIKE '%jer%';

Select *
FROM employee_demographics
WHERE first_name LIKE 'a__';

Select *
FROM employee_demographics
WHERE first_name LIKE 'a_%';

-- GROUP BY
SELECT *
FROM employee_salary;

SELECT occupation, AVG(salary), MIN(salary), MAX(salary), COUNT(occupation)
FROM employee_salary
GROUP BY occupation;

-- ORDER BY
Select *
FROM employee_demographics
ORDER BY age ASC;

Select *
FROM employee_demographics
ORDER BY age DESC;

Select *
FROM employee_demographics
ORDER BY gender, age DESC;

-- HAVING vs WHERE
SELECT 
  occupation, 
  AVG(salary), 
  MIN(salary), 
  MAX(salary), 
  COUNT(occupation)
FROM employee_salary
WHERE occupation LIKE 'city%'
GROUP BY occupation
HAVING AVG(salary) > 30000;

-- LIMIT
Select *
FROM employee_demographics
LIMIT 5;

Select *
FROM employee_demographics
ORDER BY age DESC
LIMIT 5;

-- ALIASING
SELECT 
	occupation, 
    AVG(salary) as avg_sal
FROM employee_salary
WHERE occupation like 'city%'
GROUP BY occupation
HAVING avg_sal > 30000;

-- JOINT
SELECT *
FROM employee_demographics AS dem
JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;

SELECT dem.employee_id, dem.gender, sal.salary
FROM employee_demographics AS dem
JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;

SELECT dem.employee_id, dem.gender, sal.salary, department_name
FROM employee_demographics AS dem
JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id
JOIN parks_departments as dep
	ON sal.dept_id = dep.department_id;

-- UNION
SELECT age, gender
FROM employee_demographics
UNION ALL
SELECT first_name, last_name
FROM employee_salary;

SELECT age, gender
FROM employee_demographics
UNION DISTINCT
SELECT first_name, last_name
FROM employee_salary;

SELECT first_name, last_name, 'old male' AS 'label'
FROM employee_demographics
WHERE age > 40 AND gender like 'Male'
UNION
SELECT first_name, last_name, 'old femail' AS 'label'
FROM employee_demographics
WHERE age > 40 AND gender like 'Female'
UNION
SELECT first_name, last_name, 'High paid' AS 'label'
FROM employee_salary
WHERE salary > 70000
ORDER BY first_name;

-- String functions
SELECT LENGTH('Taha Parsayan');

SELECT first_name, LENGTH(first_name)
FROM employee_demographics;

SELECT UPPER('Taha');
SELECT LOWER('Taha');

SELECT TRIM('        Taha     ');
SELECT LTRIM('        Taha     ');
SELECT RTRIM('        Taha     ');

SELECT LEFT("ghorme sabzi ba berenj", 5);
SELECT RIGHT("ghorme sabzi ba berenj", 5);
SELECT SUBSTRING("ghorme sabzi ba berenj", 1, 5);
SELECT SUBSTRING("ghorme sabzi ba berenj", 5, 3);
SELECT SUBSTRING("ghorme sabzi ba berenj", 5, -3);
SELECT SUBSTRING("1995-01-16", 6, 2) AS 'month';

SELECT REPLACE('Taha', 'T', 'R');

SELECT LOCATE('s', 'Parsayan');

SELECT first_name, LOCATE('An', first_name)
FROM employee_demographics;

SELECT first_name, last_name, CONCAT(first_name,' ', last_name) AS full_name
FROM employee_demographics;

-- Case statement
SELECT first_name, last_name,
CASE
	WHEN age < 30 THEN 'Young'
    WHEN age BETWEEN 30 AND 50 THEN 'OLD'
    WHEN age > 50 THEN 'Retired'
END AS age_label
FROM employee_demographics;

-- Subquery
SELECT *
FROM employee_demographics
WHERE employee_id IN (
	SELECT employee_ID
    FROM employee_salary
    WHERE dept_id = 1
);

SELECT first_name, last_name, salary,
(
SELECT AVG(salary)
FROM employee_salary
) AS average_salary
FROM employee_salary;

-- Window functions
Select gender, AVG(salary) AS avg_salary
FROM employee_demographics AS dem
JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id
GROUP BY gender;

Select gender, AVG(salary) OVER(PARTITION BY gender)
FROM employee_demographics AS dem
JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;

Select dem.first_name, dem.last_name, gender, salary, AVG(salary) OVER(PARTITION BY gender)
FROM employee_demographics AS dem
JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;
    
Select dem.first_name, dem.last_name, gender, SUM(salary) OVER(PARTITION BY gender ORDER BY dem.employee_id) AS rolling_table
FROM employee_demographics AS dem
JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;
    
Select dem.first_name, dem.last_name, gender, salary,
ROW_NUMBER() OVER()
FROM employee_demographics AS dem
JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;
    
Select dem.first_name, dem.last_name, gender, salary,
ROW_NUMBER() OVER(PARTITION BY gender ORDER BY salary DESC) AS row_num,
RANK() OVER(PARTITION BY gender ORDER BY salary DESC) AS rank_num,
DENSE_RANK() OVER(PARTITION BY gender ORDER BY salary DESC) AS dense_rank_num
FROM employee_demographics AS dem
JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;
    
-- ---------- ADVANCED ------------

-- CTE: Common Table Expression
WITH CTE_example AS
(
SELECT occupation, AVG(salary), MIN(salary), MAX(salary), COUNT(occupation)
FROM employee_salary
GROUP BY occupation
)
SELECT *
FROM CTE_example;

WITH CTE_example AS
(
SELECT employee_id, gender, birth_date
FROM employee_demographics
WHERE birth_date > '1985-01-01'
),
CTE_example2 AS
(
SELECT employee_id, salary
FROM employee_salary
WHERE salary > 50000
)
SELECT *
FROM CTE_example AS CTE_1
JOIN CTE_example2 AS CTE_2
	ON CTE_1.employee_id = CTE_2.employee_id;
    
-- Temporary tables
#method 1
CREATE TEMPORARY TABLE table1
(
first_name varchar(50),
last_name varchar(50),
age INT
);

INSERT INTO table1
VALUES ('Taha', 'Parsayan', 30);

SELECT * 
FROM table1;

# method 2
CREATE TEMPORARY TABLE table2
SELECT *
FROM employee_salary
WHERE salary >= 50000;

SELECT *
FROM table2;

# method 3 -> CTE (not a temporary table)
WITH table3 AS (
SELECT *
FROM employee_salary
WHERE salary >= 50000
)
SELECT *
FROM table3;

-- Stored procedures
CREATE PROCEDURE large_salaries()
SELECT *
FROM employee_salary
WHERE salary >= 50000;

CALL large_salaries();

# if we need to have several queries inside it, we need to change the delimiter ; to somehting else. It can be anything such as //, or $$.
# therefore ; is no longer the end of a procedure, but only the end of a query.
DELIMITER $$
CREATE PROCEDURE large_salaries2()
BEGIN
	SELECT *
	FROM employee_salary
	WHERE salary >= 50000;
	SELECT *
	FROM employee_salary
	WHERE salary >= 10000;
END $$
DELIMITER ;

CALL large_salaries2()

# You can also right click on Stored Procedures on the left pannel to create a new one

DELIMITER $$
CREATE PROCEDURE large_salaries3(id INT)
BEGIN
	SELECT *
	FROM employee_salary
	WHERE employee_id = id;
END $$
DELIMITER ;

CALL large_salaries3(1)

-- Trigers
# we want if data is updated in one table, it also be updated in anohter related table.

DELIMITER $$
CREATE TRIGGER employee_insert
	AFTER INSERT ON employee_salary
    FOR EACH ROW
BEGIN
	INSERT INTO employee_demographics (employee_id, first_name, last_name)
    VALUES (NEW.employee_id, NEW.first_name, NEW.last_name);
END $$employee_insert
DELIMITER ;

INSERT INTO employee_salary (employee_id, first_name, last_name, occupation, salary, dept_id)
VALUES (13, 'Taha', 'Parsayan', 'Data Engineer', 55000, NULL);

SELECT *
FROM employee_salary;

SELECT *
FROM employee_demographics;

-- Events
DELIMITER $$
CREATE EVENT delete_retirees
ON SCHEDULE EVERY 30 SECOND
DO
BEGIN
	DELETE
    FROM employee_demographics
    WHERE age >= 60;
END $$
DELIMITER ;

SELECT *
FROM employee_demographics;

-- Data Cleaning

# Go to settings -> SQL editor -> uncheck safe updates
# Create a new database called world_layoffs
# On the left side in the databse right click on table and upload the .csv file

SELECT *
FROM layoffs;

-- 1. Remove duplicates

# make an empty table with the same cols
CREATE TABLE layoffs_staging
LIKE layoffs;

SELECT *
FROM layoffs_staging;

# transfer the data
INSERT layoffs_staging
SELECT *
FROM layoffs;

SELECT *
FROM layoffs_staging;

# add a new col to find the duplicates
WITH duplicate_cte AS
(
SELECT *,
ROW_NUMBER() OVER(
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, `date`, stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging
)
DELETE
FROM duplicate_cte
WHERE row_num > 1;
# it says you cannot delete from this table.
# so we create a new table and insert the col row_num as well
# this is stupid

CREATE TABLE `layoffs_staging2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_num` INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO layoffs_staging2
SELECT *,
ROW_NUMBER() OVER(
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, `date`, stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging;

SELECT *
FROM layoffs_staging2;

# now we can delete

DELETE
FROM layoffs_staging2
WHERE row_num > 1;

# I would not do it! I would do:
WITH duplicate_clean AS
(
SELECT *,
ROW_NUMBER() OVER(
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, `date`, stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging
)
SELECT *
FROM duplicate_clean
WHERE row_num = 1;

-- 2. Standardize
SELECT *
FROM layoffs_staging2;

SELECT DISTINCT(company)
FROM layoffs_staging2;

UPDATE layoffs_staging2
SET company = TRIM(company);

SELECT DISTINCT(industry)
FROM layoffs_staging2
ORDER BY 1;

UPDATE layoffs_staging2
SET industry = 'Crypto'
WHERE industry LIKE 'Crypto%';

UPDATE layoffs_staging2
SET country = TRIM(TRAILING '.' FROM country)
WHERE country LIKE 'United States';

# fix date format
UPDATE layoffs_staging2
SET `date` = STR_TO_DATE(`date`, '%m/%d/%Y');
# convert text to date
ALTER TABLE layoffs_staging2
MODIFY COLUMN `date` DATE;

-- 3. No values or blank values
SELECT *
FROM layoffs_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

-- 4. Remove unnecessary cols
