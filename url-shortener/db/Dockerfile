FROM postgres:14-alpine 
COPY schema.sql /docker-entrypoint-initdb.d/
EXPOSE ${DATABASE_PORT}