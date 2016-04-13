''' Script to check the correctness of the analysis. The analysis is done on raw data and all results are compared to a recorded analysis.
'''

import os
import unittest
import tables as tb
import numpy as np

from silab_utils import analysis_utils

# Get package path
testing_path = os.path.dirname(__file__)  # Get the absoulte path of the online_monitor installation

# Set the converter script path
tests_data_folder = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(testing_path)) + r'/testing/test_utils_data/'))


class TestUtils(unittest.TestCase):

    def test_1d_index_histograming(self):  # check compiled hist_2D_index function
        x = np.random.randint(0, 100, 100)
        shape = (100, )
        array_fast = analysis_utils.hist_1d_index(x, shape=shape)
        array = np.histogram(x, bins=shape[0], range=(0, shape[0]))[0]
        shape = (5, )  # shape that is too small for the indices to trigger exception
        exception_ok = False
        try:
            array_fast = analysis_utils.hist_1d_index(x, shape=shape)
        except IndexError:
            exception_ok = True
        except:  # other exception that should not occur
            pass
        self.assertTrue(exception_ok & np.all(array == array_fast))

    def test_2d_index_histograming(self):  # check compiled hist_2D_index function
        x, y = np.random.randint(0, 100, 100), np.random.randint(0, 100, 100)
        shape = (100, 100)
        array_fast = analysis_utils.hist_2d_index(x, y, shape=shape)
        array = np.histogram2d(x, y, bins=shape, range=[[0, shape[0]], [0, shape[1]]])[0]
        shape = (5, 200)  # shape that is too small for the indices to trigger exception
        exception_ok = False
        try:
            array_fast = analysis_utils.hist_2d_index(x, y, shape=shape)
        except IndexError:
            exception_ok = True
        except:  # other exception that should not occur
            pass
        self.assertTrue(exception_ok & np.all(array == array_fast))

    def test_3d_index_histograming(self):  # check compiled hist_3D_index function
        with tb.open_file(os.path.join(tests_data_folder + '/hist_data.h5'), mode="r") as in_file_h5:
            xyz = in_file_h5.root.HistDataXYZ[:]
            x, y, z = xyz[0], xyz[1], xyz[2]
            shape = (100, 100, 100)
            array_fast = analysis_utils.hist_3d_index(x, y, z, shape=shape)
            array = np.histogramdd(np.column_stack((x, y, z)), bins=shape, range=[[0, shape[0] - 1], [0, shape[1] - 1], [0, shape[2] - 1]])[0]
            shape = (50, 200, 200)  # shape that is too small for the indices to trigger exception
            exception_ok = False
            try:
                array_fast = analysis_utils.hist_3d_index(x, y, z, shape=shape)
            except IndexError:
                exception_ok = True
            except:  # other exception that should not occur
                pass
            self.assertTrue(exception_ok & np.all(array == array_fast))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TextTestRunner(verbosity=2).run(suite)
