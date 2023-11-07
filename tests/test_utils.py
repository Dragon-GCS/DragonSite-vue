import unittest

from server.utils import join_path


class TestUtils(unittest.TestCase):
    def test_join_path(self):
        self.assertEqual(join_path("path1", "path2"), "/path1/path2")
        self.assertEqual(join_path("path1/", "/path2"), "/path1/path2")
        self.assertEqual(join_path("path1", "path2", "path3"), "/path1/path2/path3")
        self.assertEqual(join_path("path1", "", "path3"), "/path1/path3")
        self.assertEqual(join_path("", "path2"), "/path2")
        self.assertEqual(join_path("", ""), "/")
