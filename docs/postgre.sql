sudo -u postgres psql
CREATE DATABASE djangoproject;
CREATE USER djangouser WITH PASSWORD '1234';
ALTER ROLE djangouser SET client_encoding TO 'utf8';
ALTER ROLE djangouser SET default_transaction_isolation TO 'read committed';
ALTER ROLE djangouser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE djangoproject TO djangouser;
ALTER DATABASE djangoproject OWNER TO djangouser;
\q