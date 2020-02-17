#!/usr/bin/env python3
import io
import subprocess
import control
proc = subprocess.Popen("adb logcat", shell=True, stdout=subprocess.PIPE)
for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
    if "com.google.android.apps.tachyon.action.ACTION_LIGHTWEIGHT_INCOMING_RING" in line:
        control.run("adb shell input swipe 344 1130 344 0 1500")