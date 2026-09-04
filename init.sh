#!/bin/bash
set -e

# =============================================================================
# EU-27 Sovereign Data Centers — initialize from scratch
# =============================================================================
# Idempotent: safe to re-run at any time.

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info()    { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error()   { echo -e "${RED}❌ $1${NC}"; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# The date stamped into generated files, kept in one place so init/run/test agree.
# Pinned so regeneration is byte-reproducible: a diff then shows real changes rather
# than today's date in 27 files.
export SOURCE_DATE_EPOCH="$(cat "$ROOT/.build-epoch")"

echo -e "${GREEN}🇪🇺 EU-27 Sovereign Data Centers${NC}"
echo -e "${GREEN}Initializing...${NC}"
echo

# --- Prerequisites -----------------------------------------------------------
print_info "Checking prerequisites..."

version_at_least() {
    # $1 = minimum, $2 = actual. Uses sort -V, matching the workspace templates.
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$1" ]
}

if ! command -v python3 &> /dev/null; then
    print_error "python3 is not installed. The capacity model needs Python 3.11+."
    exit 1
fi
PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')
if ! version_at_least "3.11.0" "$PY_VERSION"; then
    print_error "Python 3.11+ required. Found $PY_VERSION"
    exit 1
fi
print_success "Python $PY_VERSION (stdlib only — nothing to install)"

if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Install Node 20+ from https://nodejs.org/"
    exit 1
fi
NODE_VERSION=$(node -v | cut -d'v' -f2)
if ! version_at_least "20.0.0" "$NODE_VERSION"; then
    print_error "Node.js 20+ required. Found v$NODE_VERSION"
    exit 1
fi
print_success "Node.js v$NODE_VERSION"

if ! command -v npm &> /dev/null; then
    print_error "npm is not installed."
    exit 1
fi
print_success "npm $(npm -v)"

# --- Optional tools ----------------------------------------------------------
# Chrome is needed for PDF/poster export and for the end-to-end tests. Note the
# local install is at Chrome.app, not the conventional "Google Chrome.app".
CHROME_CANDIDATES=(
    "/Applications/Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
)
CHROME=""
for candidate in "${CHROME_CANDIDATES[@]}"; do
    if [ -x "$candidate" ]; then CHROME="$candidate"; break; fi
done
if [ -n "$CHROME" ]; then
    print_success "Browser for export/E2E: $(basename "$(dirname "$(dirname "$(dirname "$CHROME")")")" .app)"
else
    print_warning "No Chromium-family browser found — './run.sh export' and E2E tests will not run"
fi

# Typst is only needed for the paper book, so a missing install is a warning.
if command -v typst &> /dev/null; then
    print_success "typst $(typst --version | awk '{print $2}')"
else
    print_warning "typst not installed — './run.sh book' will not run"
    echo -e "         Install with: ${GREEN}brew install typst${NC}"
fi

# --- Web dependencies --------------------------------------------------------
echo
print_info "Installing web dependencies..."
cd "$ROOT/web"
# Playwright drives the Chrome already on this machine (channel: 'chrome'), so its
# ~400 MB Chromium download is skipped deliberately.
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
if [ -f package-lock.json ]; then
    npm ci --no-audit --no-fund
else
    npm install --no-audit --no-fund
fi
print_success "$(python3 -c "import json;d=json.load(open('package.json'));print(len(d.get('dependencies',{}))+len(d.get('devDependencies',{})))") direct dependencies installed, all exactly pinned"
cd "$ROOT"

# --- Data --------------------------------------------------------------------
echo
print_info "Generating the data bundle..."
python3 model/export_json.py
print_success "web/public/data/eu27.json ready"

# --- Done --------------------------------------------------------------------
echo
print_success "Initialization complete"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo -e "${BLUE}Next steps:${NC}"
echo -e "  ${GREEN}./run.sh${NC}          Start the dev server on http://localhost:5173"
echo -e "  ${GREEN}./test.sh${NC}         Run the full test gate"
echo -e "  ${GREEN}./run.sh help${NC}     List every command"
echo
