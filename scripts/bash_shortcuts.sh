
# See README.md

rut()
{
  # shellcheck disable=SC2116
  local -r TIDS=$(echo "${*// / or /}")
  make run_unit_tests TIDS="-k ${TIDS}"
}

eut()
{
  # shellcheck disable=SC2116
  local -r TIDS=$(echo "${*// / or /}")
  make exec_unit_tests TIDS="-k ${TIDS}"
}

rst()
{
  # shellcheck disable=SC2116
  local -r TIDS=$(echo "${*// / or /}")
  make run_system_tests TIDS="-k ${TIDS}";
}

# Note: replacing
#    local -r TIDS=$(echo "${*// / or /}")
# with
#    local -r TIDS="$(*// / or /)"
# causes warning
#    rut:N: permission denied: __pycache__//
