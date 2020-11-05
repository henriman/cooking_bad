import unittest
import api

class TestAuthentication(unittest.TestCase):
    def test_slow_equals(self):
        s1 = b"abc"
        s2 = b"abc"
        self.assertTrue(
            api.Account.Authentication.slow_equals(s1, s2),
            "Equal strings should result in True."
        )

        s1 = b"abc"
        s2 = b"abd"
        self.assertFalse(
            api.Account.Authentication.slow_equals(s1, s2),
            "Different strings should result in False."
        )

        s1 = b"abc"
        s2 = b"ab"
        self.assertFalse(
            api.Account.Authentication.slow_equals(s1, s2),
            "Different strings (of different length) should result in False."
        )

    def test_authenticate(self):
        acc = api.Account.Authentication("1234")
        self.assertTrue(
            acc.authenticate("1234"),
            "Correct password should result in True."
        )
        self.assertFalse(
            acc.authenticate("password"),
            "Incorrect password should result in False."
        )


if __name__ == "__main__":
    unittest.main()
