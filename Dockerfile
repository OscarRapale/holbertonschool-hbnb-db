FROM python:3.12.3-slim


WORKDIR /app


COPY requirements.txt /app/

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc-dev libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . /app

# Environment variables
ENV PORT=5000
ENV DATABASE_URL=sqlite:///hbnb_dev.db

# Expose the port
EXPOSE $PORT

# Command to run the application
CMD ["gunicorn", "hbnb:app", "-w", "2", "-b", "0.0.0.0:5000"]
