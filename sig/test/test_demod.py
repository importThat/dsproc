import unittest
import numpy as np
import dsproc


class TestDemod(unittest.TestCase):

    def test_normalise_pwr(self):
        message = dsproc.utils.create_message(10000, 4)
        s = dsproc.Mod(fs=10000, message=message, sps=2)
        s.ASK()
        # Randomly change the amplitude
        amps = np.random.randint(1, 100, size=len(s.samples))
        s.samples *= amps

        # demod
        d = dsproc.Demod(fs=10000)
        d.samples = s.samples.copy()
        d.normalise_pwr()

        self.assertTrue(np.all(d.samples >= -1.1))
        self.assertTrue(np.all(d.samples <= 1.1))

    def test_QAM_demod(self):
        for M in range(2, 8):
            message = dsproc.utils.create_message(200, M)
            s = dsproc.Mod(fs=10000, message=message, sps=1)
            s.QAM(type="square")
            s.baseband()

            d = dsproc.Demod(fs=10000)
            d.samples = s.samples
            c = d.detect_clusters(M, iter=100)
            out = d.QAM(c=c)

            original_pattern = dsproc.utils.markify(message)
            demod_pattern = dsproc.utils.markify(out)

            self.assertTrue(np.all(original_pattern==demod_pattern), msg=f"QAM demod failed on M={M}")

    def test_demod_ask(self):

        for M in range(2, 8):
            message = dsproc.utils.create_message(200, M)

            s = dsproc.Mod(fs=10000, sps=1, message=message)
            s.ASK()
            d = dsproc.Demod(fs=10000)
            d.samples = s.samples.copy()
            out = d.demod_ASK(M, iterations=200)
            demod_pattern = dsproc.utils.markify(out)
            original_pattern = dsproc.utils.markify(message)

            self.assertTrue(np.all(original_pattern == demod_pattern), msg=f"ASK demod failed on M={M}")

    def test_demod_fsk(self):
        sps = 50
        for M in range(2, 8):
            message = dsproc.utils.create_message(200, M)

            s = dsproc.Mod(fs=10000, sps=sps, message=message)
            s.FSK()
            d = dsproc.Demod(fs=10000)
            d.samples = s.samples.copy()
            out = d.demod_FSK(M, sps=sps, iterations=200)
            demod_pattern = dsproc.utils.markify(out)
            original_pattern = dsproc.utils.markify(message)

            self.assertTrue(np.all(original_pattern == demod_pattern), msg=f"ASK demod failed on M={M}")



if __name__ == "__main__":
    unittest.main(verbosity=1)