FROM python:3.10-slim

WORKDIR /app

# Install curl, PostgreSQL client, and other dependencies
RUN apt-get update && apt-get install -y curl postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN apt-get update && apt-get install -y poppler-utils
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create user_data directory
RUN mkdir -p /app/user_data && chmod 777 /app/user_data

# Create entrypoint script
RUN echo '#!/bin/sh\n\
echo "Starting Streamlit app..."\n\
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0\n' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["/app/entrypoint.sh"] 