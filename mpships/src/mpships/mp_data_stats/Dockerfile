FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your package (code + data + output)
COPY mpds/ mpds/

# Ensure 'import mpds' works (parent of 'mpds' on sys.path)
# ENV PYTHONPATH=/app
WORKDIR /app/mpds

# Expose your app port (adjust if needed)
EXPOSE 8051

# Define the command to run when the container starts
CMD ["python", "MP_data_stats.py"]