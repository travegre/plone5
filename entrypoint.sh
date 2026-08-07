#!/bin/bash
set -euo pipefail

# Entrypoint for Plone container (run as the 'plone' user).
# - Ensure a venv with pinned buildout tooling exists.
# - Run buildout if RUN_BUILDOUT=1 or if parts is missing/empty.
# - Exec the container command (e.g. /opt/instance/bin/instance fg).
#
# Requirements:
# - Host-mounted volumes (./data/*) must be writable by UID 1000 (plone user).
#   Run: chown -R 1000:1000 ./data ./src   on the host before first start.

PLONE_HOME="/opt/instance"
VENV_DIR="${PLONE_HOME}/venv"
BUILDOUT_BIN="${VENV_DIR}/bin/buildout"
BUILDOUT_CFG="${PLONE_HOME}/buildout.cfg"
PARTS_DIR="${PLONE_HOME}/parts"
EGGS_DIR="${PLONE_HOME}/eggs"

cd "${PLONE_HOME}"

# ---------------------------------------------------------------------------
# 1. Create virtualenv + install pinned buildout tooling if missing
# ---------------------------------------------------------------------------
if [ ! -x "${BUILDOUT_BIN}" ]; then
  echo "Virtualenv or buildout binary not found; creating venv and installing buildout tooling..."
  python3 -m venv "${VENV_DIR}"
  "${VENV_DIR}/bin/pip" install "pip==23.2.1"
  "${VENV_DIR}/bin/pip" install --no-cache-dir \
      "setuptools==65.7.0" \
      "wheel==0.38.4" \
      "zc.buildout==3.0.1" \
      "collective.recipe.environment"
fi

# ---------------------------------------------------------------------------
# 2. Decide whether to run buildout
# ---------------------------------------------------------------------------
if [ "${RUN_BUILDOUT:-0}" = "1" ] || [ ! -d "${PARTS_DIR}" ] || [ -z "$(ls -A "${PARTS_DIR}" 2>/dev/null || true)" ]; then
  echo "Running buildout (RUN_BUILDOUT=${RUN_BUILDOUT:-0})..."

  # Remove any partial/stale egg directories left by a previously interrupted
  # buildout run. zc.buildout uses os.rename() which fails with ENOTEMPTY
  # when the destination already exists (even if incomplete).
  if [ -d "${EGGS_DIR}" ]; then
    echo "Cleaning stale temporary egg directories in ${EGGS_DIR}..."
    find "${EGGS_DIR}" -maxdepth 1 -name 'tmp*' -type d -exec rm -rf {} + 2>/dev/null || true
  fi

  # Fail loudly on buildout error
  "${BUILDOUT_BIN}" -c "${BUILDOUT_CFG}"
else
  echo "Skipping buildout (parts exists and RUN_BUILDOUT != 1)"
fi

# ---------------------------------------------------------------------------
# 3. Execute the container CMD (e.g. /opt/instance/bin/instance fg)
# ---------------------------------------------------------------------------
exec "$@"
