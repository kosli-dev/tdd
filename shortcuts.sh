# See README.md

# shellcheck disable=SC2116
# Replacing
#    local -r TIDS=$(echo "${*// / or /}")
# with
#    local -r TIDS="$(*// / or /)"
# causes warning
#    rut:N: permission denied: __pycache__//

rut() {
  TIDS="-k $(echo "${*// / or /}")" "$(scripts_dir)/run_unit_tests_with_coverage.sh"
}

eut() {
  TIDS="-k $(echo "${*// / or /}")" "$(scripts_dir)/exec_unit_tests_with_coverage.sh"
}

rst() {
  TIDS="-k $(echo "${*// / or /}")" "$(scripts_dir)/run_system_tests_with_coverage.sh"
}

est() {
  TIDS="-k $(echo "${*// / or /}")" "$(scripts_dir)/exec_system_tests_with_coverage.sh"
}

tid() {
  "$(scripts_dir)/print_test_id.sh"
}

demo() {
  "$(scripts_dir)/run_demo.sh"
}

scripts_dir() {
  cd "$(dirname "${BASH_SOURCE[0]}")/scripts" && pwd
}
