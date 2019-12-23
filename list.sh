
# Remove whitespace
function remWS {
    if [ -z "${1}" ]; then
        cat | tr -d '[:space:]'
    else
        echo "${1}" | tr -d '[:space:]'
    fi
}

for pkg in $(adb shell pm list packages -3 | cut -d':' -f2); do
    apk_loc="$(adb shell pm path $(remWS $pkg) | cut -d':' -f2 | remWS)"
    apk_name="$(adb shell aapt dump badging $apk_loc | pcregrep -o1 $'application-label:\'(.+)\'' | remWS)"
    apk_info="$(adb shell aapt dump badging $apk_loc | pcregrep -o1 '\b(package: .+)')"

    echo "$apk_name v$(echo $apk_info | pcregrep -io1 -e $'\\bversionName=\'(.+?)\'')"
done
