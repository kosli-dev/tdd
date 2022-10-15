
# See README.md

mtu() {
  local -r TIDS=$(echo "$*" | sed "s/ / or /g")
  make test_unit TIDS="-k ${TIDS}"
}

mts() {
  local -r TIDS=$(echo "$*" | sed "s/ / or /g")
  make test_system TIDS="-k ${TIDS}";
}