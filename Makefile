
tid:
	@./scripts/print_test_id.sh

test_unit:
	@./scripts/run_unit_tests_with_coverage.sh "${TIDS}"

test_system:
	@./scripts/run_system_tests_with_coverage.sh "${TIDS}"

demo:
	@./scripts/run_demo.sh
