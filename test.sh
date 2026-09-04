#!/bin/bash
set -e

# =============================================================================
# EU-27 Sovereign Data Centers — full test gate
# =============================================================================
# Runs everything and stops at the first failure, cheapest checks first so a
# problem surfaces in seconds rather than minutes.
#
#   ./test.sh              everything
#   ./test.sh --no-e2e     skip the browser stage (no Chrome, or CI without one)
#
# Exit 0 = safe to publish. Anything else = do not.

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

SKIP_E2E=false
for arg in "$@"; do
    case "$arg" in
        --no-e2e) SKIP_E2E=true ;;
        --help|-h)
            sed -n '3,14p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $arg${NC}"
            exit 1
            ;;
    esac
done

STEP=0
step() {
    STEP=$((STEP + 1))
    echo
    echo -e "${BLUE}[$STEP] $1${NC}"
}
ok() { echo -e "${GREEN}    ✅ $1${NC}"; }

# The date stamped into generated files, kept in one place so init/run/test agree.
# Pinned so regeneration is byte-reproducible: a diff then shows real changes rather
# than today's date in 27 files.
export SOURCE_DATE_EPOCH="$(cat "$ROOT/.build-epoch")"

echo -e "${GREEN}Running the full test gate${NC}"

# -----------------------------------------------------------------------------
step "Python model and data integrity"
python3 -m unittest discover -s tests -q
ok "model, CSV integrity, referential integrity, determinism"

# -----------------------------------------------------------------------------
step "Generated files are current"
# Regenerate with the date pinned; anything that moves is a real change that was
# not committed, which would make the published site disagree with the model.
python3 model/generate_countries.py > /dev/null
python3 model/export_json.py > /dev/null
if ! git diff --quiet -- countries model web/public/data; then
    echo -e "${RED}    ❌ Generated files are stale. Run ./run.sh data and commit.${NC}"
    git diff --stat -- countries model web/public/data
    exit 1
fi
ok "briefs, CSVs and bundle match the model"

# -----------------------------------------------------------------------------
if [ ! -d "web/node_modules" ]; then
    echo -e "${RED}❌ web/node_modules missing. Run ./init.sh first.${NC}"
    exit 1
fi
cd web

step "TypeScript types"
npm run --silent type-check
ok "tsc --noEmit clean"

step "Lint"
npm run --silent lint
ok "eslint clean"

step "Formatting"
npm run --silent format:check
ok "prettier clean"

step "Unit tests and TS/Python parity"
npm run --silent test
ok "capacity.ts reproduces the Python model for all 27 countries"

step "Production build"
npm run --silent build
ok "build succeeded"

cd "$ROOT"

# -----------------------------------------------------------------------------
if [ "$SKIP_E2E" = true ]; then
    echo
    echo -e "${YELLOW}⚠️  Skipping browser stage (--no-e2e)${NC}"
else
    step "End-to-end, accessibility and rendered-data assertions"
    cd web
    npx playwright test
    ok "routes render real data; no accessibility violations"
    cd "$ROOT"
fi

# -----------------------------------------------------------------------------
echo
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ All checks passed${NC}"
echo
echo -e "${YELLOW}Note:${NC} passing does not mean the data is verified. The legal and"
echo "regulatory entries are still unverified research — see DECISIONS.md #25"
echo "for the gate that must pass before publishing to a custom domain or print."
