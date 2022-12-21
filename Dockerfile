FROM seatable/seatable-enterprise:latest

LABEL description="Seatable with custom config."

COPY templates/ /templates/
