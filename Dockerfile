FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/app

# Dependencies are installed first so docker can cache them to make future docker builds faster.
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add all files to the working directory
ADD ./ ./

# Collect static files
RUN python manage.py collectstatic --noinput

# dos2unix ensures the script is not tampered by Windows line endings
RUN apt-get update && apt-get install dos2unix
RUN dos2unix ./run-prod.sh

# Make the script executable
RUN chmod +x ./run-prod.sh

EXPOSE 8000

CMD ["/bin/bash", "./run-prod.sh"]