ARG SEATABLE_VERSION=latest
FROM seatable/seatable-enterprise:${SEATABLE_VERSION}

# Maintainer
LABEL maintainer="HaiPhamHoang" \
      version="1.0.0" \
      description="Seatable with some custom config." \
      url="https://github.com/haiphamhoang/seatable-enterprise-docker"


COPY templates/ /templates/
