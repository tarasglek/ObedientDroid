from subprocess import check_output, call
import json
import sys
# https://gist.github.com/me7/12ad7c823a1b5d1a061dceb4fcd72b87
# https://stackoverflow.com/questions/18924968/using-adb-to-access-a-particular-ui-control-on-the-screen
def run(cmd):
    print(cmd, file=sys.stderr)
    return check_output(cmd, shell=True).decode("utf-8")

def ensure_screen_on():
    if "Display Power: state=OFF" in run("adb shell dumpsys power"):
        print("state=off")
        run("adb shell input keyevent 82;sleep 1;adb shell input keyevent 82;")
    # lines =  [line for line in run("adb shell dumpsys power").split("\n") if "mHoldingDisplaySuspendBlocker" in line]
    # print("locked")
    # print("\n".join(lines))
    # run("adb shell input keyevent 82")

def termux():
    ensure_screen_on()
    run("adb shell am start -n com.termux/.app.TermuxActivity")

def main():
    run("adb forward tcp:8022 tcp:8022")
    termux()
    # figure out local addresses to exclude from sshuttle
    # TODO: wonder how ip route output looks like when there is no outside routing
    output = run("ip route get 1.1.1.1").split("\n")[0].split(' ')
    wwan = output[4]
    # get extended details for wwan interface
    wwan_details = [
        interface
            for interface in json.loads(run("ip -j -p  addr show " + wwan))
                if interface.get('ifname', None) == wwan]
    # only do ipv4
    addr_info = [details for details in wwan_details[0]['addr_info'] if details['family'] == 'inet'][0]
    # get netmask and local ip
    ip = addr_info['local']
    netmask = addr_info['prefixlen']
    run(f"sshuttle -v -x {ip}/{netmask}  --python python2 -r localhost:8022 0/0")

if __name__ == "__main__":
    main()