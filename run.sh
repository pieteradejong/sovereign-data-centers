#!/bin/bash
set -e

# =============================================================================
# EU-27 Sovereign Data Centers — development runner
# =============================================================================

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

check_deps() {
    if [ ! -d "$ROOT/web/node_modules" ]; then
        print_error "Dependencies not installed. Run ./init.sh first."
        exit 1
    fi
}

show_help() {
    echo -e "${GREEN}EU-27 Sovereign Data Centers${NC}"
    echo
    echo "Usage: ./run.sh [command]"
    echo
    echo -e "${GREEN}Develop${NC}"
    echo "  dev, start       Start the dev server (default)"
    echo "  build            Production build"
    echo "  preview          Serve the production build"
    echo
    echo -e "${GREEN}Quality${NC}"
    echo "  test             Full test gate (delegates to ./test.sh)"
    echo "  test:watch       Vitest in watch mode"
    echo "  lint             ESLint"
    echo "  lint:fix         ESLint with auto-fix"
    echo "  format           Prettier write"
    echo "  format:check     Prettier check"
    echo "  type-check       tsc --noEmit"
    echo
    echo -e "${GREEN}Data and artefacts${NC}"
    echo "  data             Regenerate country CSVs, briefs and the JSON bundle"
    echo "  artefacts        Re-render the tracked posters and briefing PDFs (needs Chrome)"
    echo "  export           Standalone per-country PDF briefs (book/build/briefs/)"
    echo "  book             Typeset the paper book"
    echo "  sources          Verification-ledger coverage report"
    echo
    echo -e "${GREEN}Housekeeping${NC}"
    echo "  clean            Remove build artefacts"
    echo "  health           Versions, data freshness, tool availability"
    echo "  help             This message"
}

regen_data() {
    print_info "Regenerating model outputs..."
    python3 model/generate_countries.py > /dev/null
    python3 model/export_json.py
    print_success "Country files, briefs and bundle regenerated"
}

case "${1:-dev}" in
    dev|start)
        check_deps
        print_info "Starting dev server on http://localhost:5173"
        cd web && npm run dev
        ;;
    build)
        check_deps
        regen_data
        (cd web && npm run build)
        # Briefs go into dist/, never into web/public/ — public/ is committed and these
        # are regenerable binaries. Skipped rather than fatal when typst is absent.
        if command -v typst &> /dev/null; then
            python3 book/build.py --briefs -o web/dist/briefs > /dev/null
            print_success "Built to web/dist/ (with 27 briefs at /briefs/<ISO>.pdf)"
        else
            print_warning "typst missing — built without the per-country PDFs"
            print_success "Built to web/dist/"
        fi
        ;;
    preview)
        check_deps
        cd web && npm run preview
        ;;
    test)
        exec "$ROOT/test.sh" "${@:2}"
        ;;
    test:watch)
        check_deps
        cd web && npm run test:watch
        ;;
    lint)         check_deps; cd web && npm run lint ;;
    lint:fix)     check_deps; cd web && npm run lint:fix ;;
    format)       check_deps; cd web && npm run format ;;
    format:check) check_deps; cd web && npm run format:check ;;
    type-check)   check_deps; cd web && npm run type-check ;;
    data)
        regen_data
        ;;
    artefacts)
        # The tracked countries/<ISO>/ poster and briefing PDF (#24, #51). Distinct from
        # `export`, which typesets standalone A4 briefs into the gitignored book/build/.
        check_deps
        python3 model/export_artifacts.py "${@:2}"
        ;;
    export)
        check_deps
        python3 book/build.py --briefs "${@:2}"
        ;;
    sources)
        python3 model/sources.py "${@:2}"
        ;;
    book)
        if ! command -v typst &> /dev/null; then
            print_error "typst is not installed. Install with: brew install typst"
            exit 1
        fi
        print_info "Typesetting the book..."
        python3 book/build.py "${@:2}"
        ;;
    clean)
        print_info "Cleaning build artefacts..."
        rm -rf web/dist web/coverage web/test-results web/playwright-report
        find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
        print_success "Clean"
        ;;
    health)
        echo -e "${GREEN}Environment${NC}"
        echo "  python3   $(python3 --version 2>&1 | awk '{print $2}')"
        echo "  node      $(node -v 2>/dev/null || echo 'missing')"
        echo "  npm       $(npm -v 2>/dev/null || echo 'missing')"
        echo "  typst     $(typst --version 2>/dev/null | awk '{print $2}' || echo 'missing (book only)')"
        echo
        echo -e "${GREEN}Data${NC}"
        if git diff --quiet -- countries model web/public/data 2>/dev/null; then
            print_success "No uncommitted changes under countries/, model/ or the bundle"
        else
            # Not necessarily stale: re-rendered artefacts and work in progress look
            # the same here. ./test.sh distinguishes them by regenerating and seeing
            # whether anything moves.
            print_warning "Uncommitted changes present — ./test.sh says whether they are stale"
        fi
        echo "  countries $(find countries -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')"
        echo "  bundle    $(du -h web/public/data/eu27.json 2>/dev/null | cut -f1 || echo 'missing')"
        echo
        echo -e "${GREEN}Verification${NC} (the gate on indexing, the domain and the book)"
        python3 model/sources.py 2>/dev/null | tail -1 | sed 's/^/  /' 
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo
        show_help
        exit 1
        ;;
esac
