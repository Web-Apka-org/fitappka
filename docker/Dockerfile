FROM python:3.11-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev
COPY requriements.txt .
RUN pip install --no-cache-dir -r requriements.txt
WORKDIR app

EXPOSE 8000
