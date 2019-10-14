# logcat-kernel-time-aligner
When you get logcat, which including kernel log from an Android device.
The timestamp of kernel is not match to the others - main/system/radio.
This program helps replace the kernel timestamp to align the previous log (main/system/radio).

## Usage
Make a logcat to have the "Kernel Time Fix"

    python KernelLogTimeAligner.py logcat.log > logcat_ktfix.log
