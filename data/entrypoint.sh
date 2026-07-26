#!/bin/bash
set -euo pipefail

# Entrypoint for Plone container (run as the 'plone' user).
# - Ensure a venv with pinned buildout tooling exists (created in the mounted /opt/instance).
# - Run buildout if RUN_BUILDOUT=1 or if parts is missing/empty.
# - Exec the container command (e.g. /opt/instance/bin/instance fg).
#
# Requirements:
# - The host-mounted ./data (or whatever is mounted to /opt/instance) must be writable
#   by this user (commonly chown -R 1000:1000 ./data ./src on the host).

PLONE_HOME="/opt/instance"
VENV_DIR="${PLONE_HOME}/venv"
BUILDOUT_BIN="${VENV_DIR}/bin/buildout"
BUILDOUT_CFG="${PLONE_HOME}/buildout.cfg"
PARTS_DIR="${PLONE_HOME}/parts"

cd "${PLONE_HOME}"

# Create virtualenv + install pinned buildout tooling if missing
if [ ! -x "${BUILDOUT_BIN}" ]; then
  echo "Virtualenv or buildout binary not found; creating venv and installing buildout tooling..."
  python3 -m venv "${VENV_DIR}"
  "${VENV_DIR}/bin/pip" install --upgrade pip
  "${VENV_DIR}/bin/pip" install --no-cache-dir "setuptools==65.7.0" "wheel==0.38.4" "zc.buildout==3.0.1"
fi

# Decide whether to run buildout:
# - If RUN_BUILDOUT is explicitly set to "1", run it
# - Or run it if parts dir is absent or empty
if [ "${RUN_BUILDOUT:-0}" = "1" ] || [ ! -d "${PARTS_DIR}" ] || [ -z "$(ls -A "${PARTS_DIR}" 2>/dev/null || true)" ]; then
  echo "Running buildout (RUN_BUILDOUT=${RUN_BUILDOUT:-0})..."
  # Fail loudly on buildout error
  "${BUILDOUT_BIN}" -c "${BUILDOUT_CFG}"
else
  echo "Skipping buildout (parts exists and RUN_BUILDOUT != 1)"
fi

# Execute the container's CMD (e.g. /opt/instance/bin/instance fg)
exec "$@"
