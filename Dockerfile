FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /tmp/uploaded_docs /tmp/chroma_db assets

EXPOSE 7860

CMD ["streamlit", "run", "app.py", \
     "--server.port=7860", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.maxUploadSize=200", \
     "--server.maxMessageSize=200", \
     "--browser.gatherUsageStats=false", \
     "--theme.base=dark", \
     "--theme.primaryColor=#6366f1", \
     "--theme.backgroundColor=#0a0a0f", \
     "--theme.secondaryBackgroundColor=#12121a", \
     "--theme.textColor=#f1f5f9"]
