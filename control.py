#!/usr/bin/env python3
from subprocess import check_output, call
import json
import sys
import os.path
# https://gist.github.com/me7/12ad7c823a1b5d1a061dceb4fcd72b87
# https://stackoverflow.com/questions/18924968/using-adb-to-access-a-particular-ui-control-on-the-screen
def run(cmd):
    print(cmd, file=sys.stderr)
    return check_output(cmd, shell=True).decode("utf-8")

def ensure_screen_on():
    if "Display Power: state=OFF" in run("adb shell dumpsys power"):
        run("adb shell input keyevent 82;sleep 1;adb shell input keyevent 82;")
    # lines =  [line for line in run("adb shell dumpsys power").split("\n") if "mHoldingDisplaySuspendBlocker" in line]
    # print("locked")
    # print("\n".join(lines))
    # run("adb shell input keyevent 82")

def termux():
    ensure_screen_on()
    run("adb shell am start -n com.termux/.app.TermuxActivity")

def vpn(endpoint):
    # run("adb kill-server")
    run("adb forward tcp:8022 tcp:8022")
    #ensure forward worked
    print(run("adb forward --list |  grep tcp:8022"))
    termux()
    # figure out local addresses to exclude from sshuttle
    # TODO: wonder how ip route output looks like when there is no outside routing
    output = run("ip route get 1.1.1.1").split("\n")[0].split(' ')
    wwan = output[4]
    # get extended details for local interfaces
    exclude_ls = []
    for iface in json.loads(run("ip -j -p  addr show ")):
        for info in iface['addr_info']:
            if info['family'] == 'inet':
                exclude_ls.append("-x {}/{}".format(info['local'],info['prefixlen']))
    exclude_str = (" ".join(exclude_ls))
    # dont do interactive prompts
    ssh_opts = " -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o      ServerAliveInterval=60"
    ssh = f"""ssh -C -R 6666:localhost:22 {ssh_opts} -o ProxyCommand="ssh -W %h:%p localhost -p 8022 {ssh_opts}" """
    # --python python2
    run(f"""sshuttle --dns -e '{ssh}' {exclude_str} -r {endpoint} 0/0""")
    sys.exit(1)

def main(mode):
    if mode == "vpn":
        prefix = os.path.dirname(__file__)
        if prefix == "":
            prefix = "."
        config = json.load(open(prefix + "/config.json"))
        vpn(config["ssh"])

if __name__ == "__main__":
    main(*sys.argv[1:])
