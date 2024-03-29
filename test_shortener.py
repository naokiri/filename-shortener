from unittest import TestCase

from filename_shortener import *


class Tests(TestCase):
    def test_replace_spaces(self):
        result = replace_spaces("foo　hoge　bar")
        self.assertEqual("foo hoge bar", result)

    def test_remove_paren_in_bracket(self):
        result = remove_paren_in_bracket("[foo bar (hoge)] abc")
        self.assertEqual("[foo bar] abc", result)
        result = remove_paren_in_bracket("[ほげ　(補足)]　書名.epub")
        self.assertEqual("[ほげ]　書名.epub", result)

    def test_remove_paren_appended(self):
        result = remove_paren_appended("hogehoge (rescanned).pdf")
        self.assertEqual("hogehoge.pdf", result)
        result = remove_paren_appended("(piyo) [hoge] Foo bar baz (foo bar baz).pdf")
        self.assertEqual("(piyo) [hoge] Foo bar baz.pdf", result)

    def test_remove_bracket_appended(self):
        result = remove_bracket_appended("An important paper about fugafuga [2015-10-11].pdf")
        self.assertEqual("An important paper about fugafuga.pdf", result)
        result = remove_paren_appended("(piyo) [hoge fuga] Foo bar baz [foo bar baz].pdf")
        self.assertEqual("(piyo) [hoge fuga] Foo bar baz [foo bar baz].pdf", result)


    def test_remove_words(self):
        func = remove_words_func({"絶版"})
        result = func("(電子透かし済) hoge")
        self.assertEqual("hoge", result)
        result = func("【絶版】 fuu.pdf")
        self.assertEqual("fuu.pdf", result)

    def test_remove_date_6num_tag(self):
        result = remove_date_6num_tag("[170127] hogehoge")
        self.assertEqual("hogehoge", result)
        result = remove_date_6num_tag("foo 11 ways to do.zip")
        self.assertEqual("foo 11 ways to do.zip", result)

    def test_apply_all(self):
        result = apply_all("")
        self.assertEqual("", result)
