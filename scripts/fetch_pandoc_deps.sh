#!/bin/bash
# Download pandoc hackage dependencies for offline build.
# Fetch phase — requires network access.
#
# Usage: ./scripts/fetch_pandoc_deps.sh [DEPS_FILE] [OUTPUT_DIR]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${SCRIPT_DIR}/.."

DEPS_FILE="${1:-${PROJECT_DIR}/pandoc-deps.txt}"
HACKAGE_DIR="${2:-${PROJECT_DIR}/hackage-packages}"

if [[ ! -f "${DEPS_FILE}" ]]; then
    echo "Error: ${DEPS_FILE} not found" >&2
    exit 1
fi

mkdir -p "${HACKAGE_DIR}"

TOTAL=$(grep -c "^https://" "${DEPS_FILE}" || echo 0)
COUNT=0

while read -r url; do
    [[ "$url" =~ ^#.*$ ]] && continue
    [[ -z "$url" ]] && continue

    COUNT=$((COUNT + 1))
    FILENAME=$(basename "$url")

    if [[ -f "${HACKAGE_DIR}/${FILENAME}" ]]; then
        echo "[${COUNT}/${TOTAL}] ${FILENAME} (exists)"
        continue
    fi

    echo "[${COUNT}/${TOTAL}] ${FILENAME}"
    curl -sL "$url" -o "${HACKAGE_DIR}/${FILENAME}" || {
        echo "  WARNING: Failed to download ${url}" >&2
    }
done < "${DEPS_FILE}"

DOWNLOADED=$(find "${HACKAGE_DIR}" -name '*.tar.gz' | wc -l)
echo "Packages: ${DOWNLOADED}/${TOTAL}"
