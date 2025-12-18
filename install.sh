#!/bin/sh
# SignalPilot CLI Installer
# Usage: curl -sSf https://get.signalpilot.dev | sh
#
# This script:
# 1. Installs uv if not present
# 2. Creates isolated venv at ~/.signalpilot/venv
# 3. Installs signalpilot-cli package
# 4. Creates wrapper script at ~/.signalpilot/bin/sp
# 5. Adds ~/.signalpilot/bin to PATH

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# SignalPilot directories
SIGNALPILOT_DIR="${HOME}/.signalpilot"
VENV_DIR="${SIGNALPILOT_DIR}/venv"
BIN_DIR="${SIGNALPILOT_DIR}/bin"

print_banner() {
    printf "\n"
    printf "${PURPLE}╭─────────────────────────────────────────────────────────────╮${NC}\n"
    printf "${PURPLE}│${NC}                                                             ${PURPLE}│${NC}\n"
    printf "${PURPLE}│${NC}   ${PURPLE}SignalPilot${NC}                                               ${PURPLE}│${NC}\n"
    printf "${PURPLE}│${NC}   Your Trusted CoPilot for Data Analysis                    ${PURPLE}│${NC}\n"
    printf "${PURPLE}│${NC}                                                             ${PURPLE}│${NC}\n"
    printf "${PURPLE}╰─────────────────────────────────────────────────────────────╯${NC}\n"
    printf "\n"
}

success() {
    printf "${GREEN}✓${NC} %s\n" "$1"
}

info() {
    printf "${BLUE}→${NC} %s\n" "$1"
}

error() {
    printf "${RED}✗${NC} %s\n" "$1"
}

# Check OS compatibility
check_os() {
    case "$(uname -s)" in
        Linux*)     OS=Linux;;
        Darwin*)    OS=macOS;;
        CYGWIN*|MINGW*|MSYS*) OS=Windows;;
        *)          OS="Unknown";;
    esac

    if [ "$OS" = "Unknown" ]; then
        error "Unsupported operating system"
        exit 1
    fi

    if [ "$OS" = "Windows" ]; then
        info "Detected Windows/WSL environment"
    fi
}

# Check for required tools
check_requirements() {
    if ! command -v curl > /dev/null 2>&1; then
        error "curl is required but not installed"
        exit 1
    fi
}

# Install uv if not present
install_uv() {
    if command -v uv > /dev/null 2>&1; then
        success "uv is already installed ($(uv --version))"
        return 0
    fi

    # Check common locations
    if [ -x "${HOME}/.local/bin/uv" ]; then
        success "uv found at ~/.local/bin/uv"
        return 0
    fi

    if [ -x "${HOME}/.cargo/bin/uv" ]; then
        success "uv found at ~/.cargo/bin/uv"
        return 0
    fi

    info "Installing uv (Python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Source the env to get uv in PATH for this session
    if [ -f "${HOME}/.local/bin/env" ]; then
        . "${HOME}/.local/bin/env"
    elif [ -f "${HOME}/.cargo/env" ]; then
        . "${HOME}/.cargo/env"
    fi

    success "uv installed"
}

# Get uv path
get_uv() {
    if command -v uv > /dev/null 2>&1; then
        echo "uv"
        return
    fi

    if [ -x "${HOME}/.local/bin/uv" ]; then
        echo "${HOME}/.local/bin/uv"
        return
    fi

    if [ -x "${HOME}/.cargo/bin/uv" ]; then
        echo "${HOME}/.cargo/bin/uv"
        return
    fi

    echo "uv"
}

# Create SignalPilot CLI venv
create_venv() {
    info "Creating SignalPilot CLI environment..."
    mkdir -p "${SIGNALPILOT_DIR}"

    UV=$(get_uv)
    "${UV}" venv "${VENV_DIR}" --python 3.12 --quiet

    success "CLI environment created"
}

# Install signalpilot-cli package
install_cli() {
    info "Installing SignalPilot CLI..."

    UV=$(get_uv)

    # Install from PyPI (or local path for development)
    if [ -n "${SIGNALPILOT_DEV_PATH:-}" ]; then
        "${UV}" pip install --python "${VENV_DIR}" -e "${SIGNALPILOT_DEV_PATH}" --quiet
    else
        "${UV}" pip install --python "${VENV_DIR}" signalpilot-cli --quiet
    fi

    success "SignalPilot CLI installed"
}

# Create wrapper script
create_wrapper() {
    info "Creating sp command..."
    mkdir -p "${BIN_DIR}"

    cat > "${BIN_DIR}/sp" << 'WRAPPER'
#!/bin/sh
exec "${HOME}/.signalpilot/venv/bin/sp" "$@"
WRAPPER

    chmod +x "${BIN_DIR}/sp"
    success "sp command created"
}

# Add to PATH in shell configs
add_to_path() {
    PATH_LINE='export PATH="${HOME}/.signalpilot/bin:${PATH}"'

    # Add to .bashrc
    if [ -f "${HOME}/.bashrc" ]; then
        if ! grep -q ".signalpilot/bin" "${HOME}/.bashrc" 2>/dev/null; then
            printf "\n# SignalPilot CLI\n%s\n" "${PATH_LINE}" >> "${HOME}/.bashrc"
        fi
    fi

    # Add to .zshrc
    if [ -f "${HOME}/.zshrc" ]; then
        if ! grep -q ".signalpilot/bin" "${HOME}/.zshrc" 2>/dev/null; then
            printf "\n# SignalPilot CLI\n%s\n" "${PATH_LINE}" >> "${HOME}/.zshrc"
        fi
    fi

    # Add to .profile for other shells
    if [ -f "${HOME}/.profile" ]; then
        if ! grep -q ".signalpilot/bin" "${HOME}/.profile" 2>/dev/null; then
            printf "\n# SignalPilot CLI\n%s\n" "${PATH_LINE}" >> "${HOME}/.profile"
        fi
    fi
}

# Print success message
print_success() {
    printf "\n"
    success "SignalPilot installed!"
    printf "\n"
    printf "  Restart your terminal, or run:\n"
    printf "    ${YELLOW}export PATH=\"\${HOME}/.signalpilot/bin:\${PATH}\"${NC}\n"
    printf "\n"
    printf "  Then run:\n"
    printf "    ${YELLOW}sp init${NC}\n"
    printf "\n"
}

# Main installation flow
main() {
    print_banner
    check_os
    check_requirements
    install_uv
    create_venv
    install_cli
    create_wrapper
    add_to_path
    print_success
}

main "$@"
