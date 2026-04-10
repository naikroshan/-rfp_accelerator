import unittest

from backend.app.domain import (
    classify_question,
    compliance_mapping,
    generate_answer,
    parse_questions_csv,
    process_question,
)


class DomainTests(unittest.TestCase):
    def test_classification_keywords(self):
        self.assertEqual(classify_question("Need SBOM generation support"), "SBOM")
        self.assertEqual(classify_question("Do you provide SAST scans?"), "SAST")
        self.assertEqual(classify_question("How do you run DAST tests?"), "DAST")
        self.assertEqual(classify_question("How do you track dependency vulnerabilities?"), "SCA")

    def test_unknown_classification(self):
        self.assertEqual(classify_question("Do you support IAM federation?"), "Unknown")

    def test_unknown_fallback_text(self):
        answer, confidence = generate_answer("Unknown")
        self.assertEqual(answer, "This capability is not explicitly documented")
        self.assertEqual(confidence, 60)

    def test_compliance_mapping_unknown(self):
        mapping = compliance_mapping("Unknown")
        self.assertEqual(mapping["RBI"], "This capability is not explicitly documented")

    def test_process_question_shape(self):
        result = process_question("Do you support DAST testing?")
        self.assertEqual(result["category"], "DAST")
        self.assertIn("compliance", result)
        self.assertIn("confidence", result)

    def test_parse_questions_csv(self):
        decoded = "question\nDo you provide SAST capabilities?\nDo you support SBOM generation?\n"
        questions = parse_questions_csv(decoded)
        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0], "Do you provide SAST capabilities?")

    def test_parse_questions_csv_missing_column(self):
        decoded = "prompt\nDo you provide SAST capabilities?\n"
        questions = parse_questions_csv(decoded)
        self.assertEqual(questions, [])


if __name__ == "__main__":
    unittest.main()
