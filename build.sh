#!/usr/bin/env bash
set -euo pipefail

# Build script for generating executable binaries
# Supports Windows and Linux platforms

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="Agro5-SCADA"
ICON_FILE="icono2-app.ico"
MAIN_FILE="main.py"
OUTPUT_DIR="dist"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

detect_os() {
  case "$(uname -s)" in
    Linux*)
      echo "linux"
      ;;
    Darwin*)
      echo "macos"
      ;;
    MINGW*|MSYS*|CYGWIN*)
      echo "windows"
      ;;
    *)
      echo "unknown"
      ;;
  esac
}

check_dependencies() {
  log_info "Checking dependencies..."
  
  if ! command -v python3 &> /dev/null; then
    log_error "Python3 is not installed or not in PATH"
    exit 1
  fi
  
  if ! python3 -c "import PyInstaller" 2>/dev/null; then
    log_error "PyInstaller is not installed"
    log_info "Install it with: pip3 install pyinstaller"
    exit 1
  fi
  
  if [[ ! -f "${SCRIPT_DIR}/${MAIN_FILE}" ]]; then
    log_error "Main file '${MAIN_FILE}' not found"
    exit 1
  fi
  
  log_info "All dependencies satisfied"
}

build_windows() {
  log_info "Building executable for Windows..."
  
  local current_os="$(detect_os)"
  if [[ "${current_os}" != "windows" ]]; then
    log_warn "You are running on ${current_os}, but trying to build for Windows"
    log_warn "PyInstaller can only build native executables for the current OS"
    log_warn "The output will be a ${current_os} executable, not a Windows .exe"
    log_info "To build for Windows, run this script on a Windows machine"
    echo ""
  fi
  
  local icon_arg=""
  if [[ -f "${SCRIPT_DIR}/${ICON_FILE}" ]]; then
    icon_arg="--icon=${ICON_FILE}"
    log_info "Using icon: ${ICON_FILE}"
  else
    log_warn "Icon file '${ICON_FILE}' not found, building without icon"
  fi
  
  cd "${SCRIPT_DIR}"
  
  python3 -m PyInstaller \
    --noconsole \
    --onefile \
    --clean \
    ${icon_arg} \
    --name="${APP_NAME}" \
    "${MAIN_FILE}"
  
  local current_os="$(detect_os)"
  local output_file="${OUTPUT_DIR}/${APP_NAME}"
  if [[ "${current_os}" == "windows" ]]; then
    output_file="${output_file}.exe"
  fi
  
  log_info "Executable built successfully"
  log_info "Output: ${output_file}"
}

build_linux() {
  log_info "Building executable for Linux..."
  
  local current_os="$(detect_os)"
  if [[ "${current_os}" != "linux" ]]; then
    log_warn "You are running on ${current_os}, but trying to build for Linux"
    log_warn "PyInstaller can only build native executables for the current OS"
    log_warn "The output will be a ${current_os} executable, not a Linux binary"
    log_info "To build for Linux, run this script on a Linux machine"
    echo ""
  fi
  
  cd "${SCRIPT_DIR}"
  
  python3 -m PyInstaller \
    --noconsole \
    --onefile \
    --clean \
    --name="${APP_NAME}" \
    "${MAIN_FILE}"
  
  local current_os="$(detect_os)"
  local output_file="${OUTPUT_DIR}/${APP_NAME}"
  if [[ "${current_os}" == "windows" ]]; then
    output_file="${output_file}.exe"
  fi
  
  log_info "Executable built successfully"
  log_info "Output: ${output_file}"
}

show_usage() {
  cat << EOF
Usage: $0 [OPTION]

Build executable binary for SCADA Supervision System.

Options:
  windows     Build for Windows (with icon support)
  linux       Build for Linux
  both        Build for both platforms
  help        Show this help message

Examples:
  $0 windows
  $0 linux
  $0 both

EOF
}

cleanup_build_artifacts() {
  log_info "Cleaning up build artifacts..."
  rm -rf build/ *.spec
  log_info "Cleanup completed"
}

main() {
  local platform="${1:-}"
  
  if [[ -z "${platform}" ]]; then
    log_error "No platform specified"
    show_usage
    exit 1
  fi
  
  case "${platform}" in
    windows)
      check_dependencies
      build_windows
      cleanup_build_artifacts
      ;;
    linux)
      check_dependencies
      build_linux
      cleanup_build_artifacts
      ;;
    both)
      check_dependencies
      build_windows
      log_info ""
      build_linux
      cleanup_build_artifacts
      ;;
    help|--help|-h)
      show_usage
      exit 0
      ;;
    *)
      log_error "Unknown platform: ${platform}"
      show_usage
      exit 1
      ;;
  esac
  
  log_info "Build process completed successfully!"
  log_info "Executable(s) can be found in: ${OUTPUT_DIR}/"
}

# Error handling
trap 'log_error "Build failed on line $LINENO"; exit 1' ERR

main "$@"
