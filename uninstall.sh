set -x -e
mkdir -p ~/.config/systemd/user/
sudo loginctl enable-linger $USER
cp *.service ~/.config/systemd/user/ -v
systemctl daemon-reload --user
for UNIT in *.service; do
    export SERVICE=`echo $UNIT |sed 's:.service::'`;
    systemctl --user stop $SERVICE
    systemctl --user disable $SERVICE
done
