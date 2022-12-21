ARG SEATABLE_VERSION=latest
FROM seatable/seatable-enterprise:${SEATABLE_VERSION}

LABEL description="Seatable with custom config."

COPY templates/ /templates/
