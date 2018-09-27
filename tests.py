from unittest import TestCase
import numpy as np

from distribution import Distribution, parse_string
from gen_test_data import generate_text

class DistributionTest(TestCase):
    def test_parsing(self):
        """Test parsing functionality"""
        nodetext = 'node_1 10\nnode_2 100'
        parsed = parse_string(nodetext)
        self.assertEqual(parsed[0], ('node_1', 10))
        self.assertEqual(parsed[1], ('node_2', 100))
        longtext = generate_text(100, 'nodes', upper=100, lower=10)
        parsed = parse_string(longtext)
        nnames, sizes = list(zip(*parsed))
        sizes = np.array(sizes)
        # Check text generator
        self.assertTrue((sizes >= 10).all())
        self.assertTrue((sizes <= 100).all())
        self.assertTrue(all([name.startswith('nodes') for name in nnames]))

    def test_simple(self):
        """Test simple cases"""
        # One file one node
        nodes = [('node', 100)]
        files = [('file', 100)]
        dist = Distribution(nodes, files)
        self.assertTrue(len(dist.placed_files), 1)
        self.assertEqual(dist.placed_files[0][0], ('file', 100))
        # One node two files that fit perfectly
        nodes = [('node', 100)]
        files = [('file_1', 25), ('file_2', 75)]
        dist = Distribution(nodes, files)
        self.assertIn(('file_1', 25), dist.placed_files[0])
        self.assertIn(('file_2', 75), dist.placed_files[0])
        # One node two files one of which doesn't fit
        nodes = [('node', 100)]
        files = [('file_1', 26), ('file_2', 75)]
        dist = Distribution(nodes, files)
        self.assertIn(('file_1', 26), dist.null_files)
        self.assertIn(('file_2', 75), dist.placed_files[0])

    def test_large(self):
        """Test some big cases to get an idea of scaling"""
        bigfiles = generate_text(1000000, 'files', upper=100)
        bignodes = generate_text(1000, 'nodes')
        # Takes around 1 min now
        dist = Distribution.from_strings(bignodes, bigfiles)
