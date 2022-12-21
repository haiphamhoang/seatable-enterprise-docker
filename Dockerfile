ARG SEATABLE_VERSION=latest
FROM seatable/seatable-enterprise:${SEATABLE_VERSION}

LABEL description="Seatable with some custom config."

COPY templates/ /templates/
