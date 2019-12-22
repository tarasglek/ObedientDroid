from subprocess import check_output, call
# https://gist.github.com/me7/12ad7c823a1b5d1a061dceb4fcd72b87
# https://stackoverflow.com/questions/18924968/using-adb-to-access-a-particular-ui-control-on-the-screen
def run(cmd):
    return check_output(cmd, shell=True).decode("utf-8")

def ensure_screen_on():
    if "Display Power: state=OFF" in run("adb shell dumpsys power"):
        print("state=off")
        run("adb shell input keyevent 82;sleep 1;adb shell input keyevent 82;")
    # lines =  [line for line in run("adb shell dumpsys power").split("\n") if "mHoldingDisplaySuspendBlocker" in line]
    # print("locked")
    # print("\n".join(lines))
    # run("adb shell input keyevent 82")

def main():
    ensure_screen_on()
    run("adb shell am start -n com.termux/.app.TermuxActivity")

if __name__ == "__main__":
    main()