
# See README.md

rut() {
  local -r TIDS=$(echo "$*" | sed "s/ / or /g")
  make run_unit_tests TIDS="-k ${TIDS}"
}

rst() {
  local -r TIDS=$(echo "$*" | sed "s/ / or /g")
  make run_system_tests TIDS="-k ${TIDS}";
}