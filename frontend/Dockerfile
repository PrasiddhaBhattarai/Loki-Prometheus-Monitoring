# Stage 1
FROM python:3.13 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
COPY . .


#Stage 2
FROM python:3.13-slim

RUN groupadd -g 1001 appgroup \
&& useradd -r -u 1001 -g appgroup -m -d /home/appuser appuser

WORKDIR /app

# appuser can read and execute the packages in /usr/local (world-readable by default), but can’t  write in runtime
# thats why no need to change owner
COPY --from=builder /install /usr/local

# COPY --from=builder /app /app
# RUN chown -R appuser:appgroup /app

# Instead of above two commands, Copy with ownership in a single layer — no separate chown RUN needed
COPY --chown=appuser:appgroup --from=builder /app .

# above commands/instructions run as root user
USER appuser:appgroup

EXPOSE 5000

# This runs as appuser user
CMD ["python","app.py"]