# See README.md

rut() { testing run unit "$*"; }
eut() { testing exec unit "$*"; }
rst() { testing run system "$*"; }
est() { testing exec system "$*"; }

tid() { "$(scripts_dir)/print_test_id.sh"; }
demo() { "$(scripts_dir)/run_demo.sh"; }
hup() { "$(scripts_dir)/hup.sh"; }

testing()
{
  local -r command="${1}"; shift
  local -r scope="${1}"; shift
  TIDS="-k ${*// / or }" \
    "$(scripts_dir)/test/${scope}/covered_${command}.sh"
}

scripts_dir()
{
  # BASH_SOURCE is empty inside a 'sourced' script
  local -r repo_home=$(git rev-parse --show-toplevel)
  echo "${repo_home}/scripts"
}

