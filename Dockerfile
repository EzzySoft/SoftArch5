FROM postgres:13

ENV POSTGRES_DB=softarch5
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword

COPY init.sql /docker-entrypoint-initdb.d/