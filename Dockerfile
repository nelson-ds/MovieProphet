FROM python:3.9-slim

WORKDIR /movieprophet/website/

# Upgrade pip
RUN pip install --no-cache-dir -U pip

# Copy and install requirements
COPY website/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application files
COPY website/ /movieprophet/website/

# Expose Flask port
EXPOSE 5000

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "main:app"]
