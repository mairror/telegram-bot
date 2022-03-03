FROM python:3.9-slim

# Maintainer of the Dockerfile
LABEL maintainer="Mairror Team"

# Input data
ARG NON_ROOT_USER=nroot
ARG ID=1000

# Hadolint DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Switch to root user to make administrative tasks
# hadolint ignore=DL3002
USER root

# Change directory to /tmp to do administrative tasks
WORKDIR /tmp

# Create a non-root user group
RUN addgroup ${NON_ROOT_USER} --gid ${ID} && \
    adduser \
      --disabled-password \
      --uid ${ID} --gid ${ID} \
      --shell /bin/bash \
      --gecos "" \
      ${NON_ROOT_USER}

# Upgrade OS && install all OS dependencies
RUN apt-get update && \
    # APT and /tmp cleanup
    apt-get clean && apt-get autoremove -y && \
        rm -rf /var/lib/{apt,dpkg,cache,log}/ && \
        rm -rf -- *

WORKDIR /app

# Change the ownership of /app to the non-root user
RUN chown -R ${NON_ROOT_USER}:${NON_ROOT_USER} /app

# Use non-root user
USER ${NON_ROOT_USER}

# Install python libraries
COPY requirements.txt /app

RUN pip install --upgrade pip==21.3.1 --no-cache-dir && \
    pip install -r /app/requirements.txt --no-cache-dir


# Add local files as late as possible to avoid cache busting
COPY --chown=${NON_ROOT_USER}:${ID} src/ /app

CMD ["python", "main.py"]
