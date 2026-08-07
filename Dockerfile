FROM python:3.8-slim

ENV PLONE_HOME=/opt/instance
ENV PATH=$PLONE_HOME/venv/bin:$PLONE_HOME/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install system dependencies required by Plone and common eggs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ git wget ca-certificates \
    libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev libssl-dev libffi-dev \
    locales netcat-openbsd && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8

# Create plone user and instance dirs
RUN useradd -m -d /home/plone -s /bin/bash plone && \
    mkdir -p ${PLONE_HOME} ${PLONE_HOME}/src ${PLONE_HOME}/var ${PLONE_HOME}/parts ${PLONE_HOME}/eggs ${PLONE_HOME}/downloads && \
    chown -R plone:plone ${PLONE_HOME}

WORKDIR ${PLONE_HOME}

# Copy buildout config and entrypoint (ownership set to plone)
# buildout.cfg will be overridden by the bind-mounted file at runtime.
COPY --chown=plone:plone buildout.cfg ${PLONE_HOME}/buildout.cfg
COPY --chown=plone:plone entrypoint.sh ${PLONE_HOME}/entrypoint.sh
RUN chmod +x ${PLONE_HOME}/entrypoint.sh

USER plone

# Create virtualenv and install pinned buildout tooling only.
# Do NOT run buildout at image build time — buildout writes into mounted volumes and
# can produce unpredictable results in images.
RUN python3 -m venv ./venv && \
    ./venv/bin/pip install --upgrade pip && \
    ./venv/bin/pip install --no-cache-dir "setuptools==65.7.0" "wheel==0.38.4" "zc.buildout==3.0.1"

EXPOSE 8080

ENTRYPOINT ["/opt/instance/entrypoint.sh"]
CMD ["/opt/instance/bin/instance", "fg"]
