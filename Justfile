## Eotel blog: maintenance recipes
##
## Quick start:
##   just dev      # build + index + serve with hot reload
##   just         # list available recipes

set shell := ["bash", "-uc"]

dev_dir   := ".claude/temp/public-dev"
dev_port  := "18080"
prod_dir  := "public"

# List available recipes
default:
    @just --list

# Production build into ./public (matches CI baseURL behavior when run in CI)
build:
    hugo --gc

# Generate the Pagefind search index for ./public
index:
    npx -y pagefind@latest --site {{prod_dir}}

# Build into the dev directory with a localhost baseURL
build-dev:
    rm -rf {{dev_dir}}
    hugo --gc --baseURL "http://localhost:{{dev_port}}/" --destination {{dev_dir}}

# Generate the Pagefind index for the dev build directory
index-dev:
    npx -y pagefind@latest --site {{dev_dir}}

# Build + index + serve with hot reload
dev: build-dev index-dev serve

# Hot-reload dev server (port 18080, livereload, content/layout watch)
# Pagefind index in {{dev_dir}}/pagefind is preserved across Hugo rebuilds.
# Re-run `just index-dev` after content edits if you want search to reflect them.
serve:
    hugo server \
        --baseURL "http://localhost:{{dev_port}}/" \
        --destination {{dev_dir}} \
        --watch \
        --port {{dev_port}} \
        --bind 127.0.0.1 \
        --noHTTPCache

# Stop any running hugo server
stop:
    @pkill -f "hugo server" 2>/dev/null && echo "stopped hugo server" || echo "no hugo server running"

# Remove all build artifacts
clean:
    rm -rf {{prod_dir}} {{dev_dir}} public-test public-ci .hugo_build.lock

# Open the dev server in the default browser (assumes `just serve` is running)
open:
    open "http://localhost:{{dev_port}}/"

# Refresh the Pagefind index in the dev build (useful while `just serve` is running)
reindex: index-dev
