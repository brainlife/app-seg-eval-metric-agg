import unittest
from aggregate import aggregate


def document(dice, **values):
    return {'raw': {'dice': dice, **values}, 'target_informed_neighbor_corrected': {'dice': min(1, dice + 0.1), **values}}


class AggregateTest(unittest.TestCase):
    def test_equal_weight_means_population_sd_and_both_groups(self):
        result = aggregate([document(0.2, tp=10), document(0.6, tp=1000)], 'Team', 'batch', ['a', 'b'])
        self.assertAlmostEqual(result['raw']['dice']['mean'], 0.4)
        self.assertAlmostEqual(result['raw']['dice']['std'], 0.2)
        self.assertEqual(result['raw']['tp']['mean'], 505)
        self.assertAlmostEqual(result['target_informed_neighbor_corrected']['dice']['mean'], 0.5)
        self.assertEqual(result['file_count'], 2)

    def test_zero_single_missing_and_all_null(self):
        result = aggregate([document(0, precision=None)], 'Team', 'batch', ['a'])
        self.assertEqual(result['raw']['dice'], {'mean': 0, 'std': 0, 'n': 1})
        self.assertEqual(result['raw']['precision'], {'mean': None, 'std': None, 'n': 0})
        mixed = aggregate([document(0, precision=0), document(1)], 'Team', 'batch', ['a', 'b'])
        self.assertEqual(mixed['raw']['precision'], {'mean': 0, 'std': 0, 'n': 1})

    def test_invalid_or_incomplete_inputs_fail(self):
        for docs, ids in [([], []), ([document(0)], []), ([document(0), document(1)], ['a', 'a']),
                          ([{'raw': {'dice': 0}}], ['a']), ([document(float('nan'))], ['a']),
                          ([document(0, tp=True)], ['a'])]:
            with self.assertRaises(ValueError):
                aggregate(docs, 'Team', 'batch', ids)


if __name__ == '__main__':
    unittest.main()
