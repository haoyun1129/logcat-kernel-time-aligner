from unittest import TestCase
from KernelLogTimeAligner import KernelLogTimeAligner


class TestKernelLogTimeAligner(TestCase):

    def setUp(self):
        self.aligner = KernelLogTimeAligner()

    def test_parse_time(self):
        a = KernelLogTimeAligner.parse_time("10-09 01:44:16.507111   628  9271 E QCamera : <MCI><ERROR> mm_stream_cancel_buf: 4847: Error Trying to extract a frame already sent to HAL(idx=40) count=1");
        b = KernelLogTimeAligner.parse_time("10-09 01:44:16.507111   628  9271 E QCamera : <MCI><ERROR> mm_stream_cancel_buf: 4847: Error Trying to extract a frame already sent to HAL(idx=40) count=1");
        self.assertEqual(a, b)

    def test_parse_time2(self):
        a = KernelLogTimeAligner.parse_time("10-09 01:44:16.507111   628  9271 E QCamera : <MCI><ERROR> mm_stream_cancel_buf: 4847: Error Trying to extract a frame already sent to HAL(idx=40) count=1");
        b = KernelLogTimeAligner.parse_time("10-09 01:44:16.507112   628  9271 E QCamera : <MCI><ERROR> mm_stream_cancel_buf: 4847: Error Trying to extract a frame already sent to HAL(idx=40) count=1");
        self.assertEqual(a, b)

    def test_parse_time_ms(self):
        a = KernelLogTimeAligner.parse_time("10-09 01:44:16.530 31757  9012 I mm-camera: <CPP   >< INFO> 364: cpp_hardware_set_clock: Set clock 200000000 BW avg 328924800 BW inst 328924800");
        b = KernelLogTimeAligner.parse_time("10-09 01:44:16.530    31757  9012 I mm-camera: <CPP   >< INFO> 364: cpp_hardware_set_clock: Set clock 200000000 BW avg 328924800 BW inst 328924800");
        self.assertEqual(a, b)

    def test_parse_time_ms2(self):
        a = KernelLogTimeAligner.parse_time("10-09 01:44:16.507 628  9271 E QCamera : <MCI><ERROR> mm_stream_cancel_buf: 4847: Error Trying to extract a frame already sent to HAL(idx=40) count=1");
        b = KernelLogTimeAligner.parse_time("10-09 01:44:16.508    628  9271 E QCamera : <MCI><ERROR> mm_stream_cancel_buf: 4847: Error Trying to extract a frame already sent to HAL(idx=40) count=1");
        self.assertNotEqual(a, b)

    def test_to_time_string(self):
        pass

    def test_determine_time_string_length(self):
        self.assertEqual(KernelLogTimeAligner.determine_time_string_length("10-09 01:44:16.508   628  9271 E QCamera :"), 18)
        self.assertEqual(KernelLogTimeAligner.determine_time_string_length("01-01 16:03:32.056     0     0 I Reserved memory"), 18)
        self.assertEqual(KernelLogTimeAligner.determine_time_string_length("10-09 01:44:16.508123   628  9271 E QCamera :"), 21)
        self.assertEqual(KernelLogTimeAligner.determine_time_string_length("01-01 16:03:32.056380     0     0 I Reserved memory"), 21)

