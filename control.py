#!/usr/bin/env python3
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
        run("adb shell input keyevent 82;sleep 1;adb shell input keyevent 82;")
    # lines =  [line for line in run("adb shell dumpsys power").split("\n") if "mHoldingDisplaySuspendBlocker" in line]
    # print("locked")
    # print("\n".join(lines))
    # run("adb shell input keyevent 82")

def termux():
    ensure_screen_on()
    run("adb shell am start -n com.termux/.app.TermuxActivity")

def vpn(endpoint):
    run("adb kill-server")
    run("adb forward tcp:8022 tcp:8022")
    #ensure forward worked
    print(run("adb forward --list |  grep tcp:8022"))
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
    # dont do interactive prompts
    ssh_opts = " -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o      ServerAliveInterval=60"
    ssh = f"""ssh -C -R 6666:localhost:22 {ssh_opts} -o ProxyCommand="ssh -W %h:%p localhost -p 8022 {ssh_opts}" """
    # --python python2
    run(f"""sshuttle --dns -e '{ssh}' -x {ip}/{netmask} -r {endpoint} 0/0""")
    sys.exit(1)

# per https://vic.demuzere.be/articles/using-systemd-user-units/
def enable_startup(endpoint):
    run("mkdir -p ~/.config/systemd/user/ && cp android-tether.service ~/.config/systemd/user/")
    run(f"sed -i s':SSH_ENDPOINT:{endpoint}:' ~/.config/systemd/user/android-tether.service")
    run("systemctl --user daemon-reload")
    run("sudo loginctl enable-linger $USER")
    run("systemctl --user enable android-tether")

def main(mode, arg):
    if mode == "vpn":
        vpn(arg)
    elif mode == "enable-startup":
        enable_startup(arg)

if __name__ == "__main__":
    main(*sys.argv[1:])
