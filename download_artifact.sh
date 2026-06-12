#!/usr/bin/env bash
set -euo pipefail

ARTIFACT_ID="7584177289"
REPO="bzlmodRio/allwpilib"
DEST="/tmp"
ZIPFILE="${DEST}/artifact_${ARTIFACT_ID}.zip"

if command -v gh &>/dev/null && gh auth status &>/dev/null 2>&1; then
    echo "Downloading artifact ${ARTIFACT_ID} via gh CLI..."
    gh api "repos/${REPO}/actions/artifacts/${ARTIFACT_ID}/zip" > "${ZIPFILE}"
elif [[ -n "${GITHUB_TOKEN:-}" ]]; then
    echo "Downloading artifact ${ARTIFACT_ID} via curl..."
    curl -fsSL \
        -H "Authorization: Bearer ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github+json" \
        -L "https://api.github.com/repos/${REPO}/actions/artifacts/${ARTIFACT_ID}/zip" \
        -o "${ZIPFILE}"
else
    echo "Error: neither 'gh' (authenticated) nor GITHUB_TOKEN is available." >&2
    exit 1
fi

echo "Extracting to ${DEST}..."
unzip -o "${ZIPFILE}" -d "${DEST}"
rm "${ZIPFILE}"
echo "Done."
