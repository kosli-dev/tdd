
tid:
	@./scripts/print_test_id.sh

run_unit_tests:
	@./scripts/run_unit_tests_with_coverage.sh "${TIDS}"

exec_unit_tests:
	@./scripts/exec_unit_tests_with_coverage.sh "${TIDS}"

run_system_tests:
	@./scripts/run_system_tests_with_coverage.sh "${TIDS}"

demo:
	@./scripts/run_demo.sh
