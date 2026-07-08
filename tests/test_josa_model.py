import unittest

from josa import append_josa
from josa_model import attach_josa, has_batchim, pick_josa, select_josa


class TestJosaFunctions(unittest.TestCase):
    def test_select_standard_pairs(self) -> None:
        self.assertEqual(pick_josa("사과", "은/는"), "는")
        self.assertEqual(select_josa("집", "은/는"), "은")
        self.assertEqual(pick_josa("고양이", ("이", "가")), "가")
        self.assertEqual(pick_josa("책", ("이", "가")), "이")

    def test_handles_rieul_exception_for_ro_pair(self) -> None:
        self.assertEqual(append_josa("길", "으로/로"), "길로")
        self.assertEqual(append_josa("집", "으로/로"), "집으로")
        self.assertEqual(append_josa("바다", "으로/로"), "바다로")
        self.assertEqual(attach_josa("길", "으로/로"), "길로")

    def test_ignores_trailing_whitespace_and_punctuation(self) -> None:
        self.assertEqual(pick_josa("달!", "은/는"), "은")
        self.assertEqual(pick_josa("사과  ", "은/는"), "는")

    def test_non_hangul_defaults_to_vowel_form(self) -> None:
        self.assertFalse(has_batchim("AI"))
        self.assertEqual(pick_josa("AI", "은/는"), "는")

    def test_rejects_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            pick_josa("", "은/는")

        with self.assertRaises(ValueError):
            pick_josa("사과", "에게")


if __name__ == "__main__":
    unittest.main()
