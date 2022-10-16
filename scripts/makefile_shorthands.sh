
# See README.md

rut() {
  local -r TIDS=$(echo "${*// / or /}")
  make run_unit_tests TIDS="-k ${TIDS}"
}

eut() {
  local -r TIDS=$(echo "${*// / or /}")
  make exec_unit_tests TIDS="-k ${TIDS}"
}

rst() {
  local -r TIDS=$(echo "${*// / or /}")
  make run_system_tests TIDS="-k ${TIDS}";
}
