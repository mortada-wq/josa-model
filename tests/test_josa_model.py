import unittest

from josa_model import JosaModel


class TestJosaModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = JosaModel()

    def test_batchim_word_uses_first_option(self) -> None:
        result = self.model.predict("집", ["은", "는"])
        self.assertEqual(result.selected_josa, "은")
        self.assertEqual(result.combined_text, "집은")

    def test_non_batchim_word_uses_second_option(self) -> None:
        result = self.model.predict("바나나", ["은", "는"])
        self.assertEqual(result.selected_josa, "는")
        self.assertEqual(result.combined_text, "바나나는")

    def test_invalid_empty_word(self) -> None:
        with self.assertRaises(ValueError):
            self.model.predict("   ")


if __name__ == "__main__":
    unittest.main()
