# but we aren't using it, we'll directly use docker-compose
FROM postgres:14

# Set environment variables
ENV POSTGRES_USER=root
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_DB=devops

# Copy initialization SQL script
COPY init.sql /docker-entrypoint-initdb.d/init.sql

# Expose default port
EXPOSE 5432