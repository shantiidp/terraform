from agentic_ai.iac_generator.validator import ValidationResult


def test_validation_result_no_errors():
    result = ValidationResult(valid=True, errors=[], warnings=["No tags found"])
    assert result.valid is True
    assert len(result.warnings) == 1


def test_validation_result_with_errors():
    result = ValidationResult(valid=False, errors=["Missing provider block"], warnings=[])
    assert result.valid is False
    assert len(result.errors) == 1
