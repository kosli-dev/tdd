
# See README.md

# shellcheck disable=SC2116
# Replacing
#    local -r TIDS=$(echo "${*// / or /}")
# with
#    local -r TIDS="$(*// / or /)"
# causes warning
#    rut:N: permission denied: __pycache__//

rut()
{
  local -r TIDS=$(echo "${*// / or /}")
  make run_unit_tests TIDS="-k ${TIDS}"
}

eut()
{
  local -r TIDS=$(echo "${*// / or /}")
  make exec_unit_tests TIDS="-k ${TIDS}"
}

rst()
{
  local -r TIDS=$(echo "${*// / or /}")
  make run_system_tests TIDS="-k ${TIDS}";
}

est()
{
  local -r TIDS=$(echo "${*// / or /}")
  make exec_system_tests TIDS="-k ${TIDS}";
}
