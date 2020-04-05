#!/bin/bash
set +e
# Set defaults if not provided by environment
CHECK_DELAY=${CHECK_DELAY:-5}
CHECK_IP=${CHECK_IP:-8.8.8.8}
PRIMARY_IF=${PRIMARY_IF:-wlan0}
PRIMARY_GW=${PRIMARY_GW:-192.168.1.1}
BACKUP_IF=${BACKUP_IF:-ppp0}
BACKUP_GW=${BACKUP_GW:-10.64.64.64}

# Compare arg with current default gateway interface for route to healthcheck IP
gateway_if() {
  [[ "$1" = "$(ip r g "$CHECK_IP" | sed -rn 's/^.*dev ([^ ]*).*$/\1/p')" ]]
}

# Cycle healthcheck continuously with specified delay
while sleep "$CHECK_DELAY"
do
  # If healthcheck succeeds from primary interface
  if ping -I "$PRIMARY_IF" -c1 "$CHECK_IP" &>/dev/null
  then
    # Are we using the backup?
    if gateway_if "$BACKUP_IF"
    then # Switch to primary
      echo switching to wifi-primary
      ip r d default via "$BACKUP_GW" dev "$BACKUP_IF"
      ip r a default via "$PRIMARY_GW" dev "$PRIMARY_IF"
    fi
  else
    # Are we using the primary?
    if gateway_if "$PRIMARY_IF"
    then # Switch to backup
      echo switching to lte
      ip r d default via "$PRIMARY_GW" dev "$PRIMARY_IF"
      ip r a default via "$BACKUP_GW" dev "$BACKUP_IF"
    fi
  fi
done
