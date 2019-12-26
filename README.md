A cheap android device can provide internet, video-calling, etc for IoT type projects. ObedientDroid provides a api to use raspberrypi + cheap android phones to automate tethering, ssh endpoint, video-calling, etc. This doesn't require hotspot or root on the phone.  303  ./duo.sh 
  381  adb shell input keyevent 82
  382  adb shell input text "cp /sdcard/authorized_keys .ssh"
  383  adb shell input text "'cp /sdcard/authorized_keys .ssh'"
  384  adb shell input keyevent 82; sleep 1; adb shell input keyevent 82
  385  adb shell input text "'cp /sdcard/authorized_keys .ssh'"
  386  adb push ~/.ssh/id_rsa.pub /sdcard/authorized_keys
  387  adb shell input keyevent 82; sleep 1; adb shell input keyevent 82
  388  adb shell input keyevent ENTER
  389  adb shell input text "'termux-setup-storge'"
  390  adb shell input keyevent ENTER
  391  adb shell input text "'termux-setup-storage'"
  392  adb shell input keyevent ENTER
  393  adb shell input keyevent TAB
  394  adb shell input keyevent ENTER
  395  ifconfig 
  396  top
  397  ls
  398  history |tail -n 100
  399  history |tail -n 100 > README.md 
  400  vi README.md 
  401  git checkout README.md
  402  history |tail -n 100 >> README.md 
