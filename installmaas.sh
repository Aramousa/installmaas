#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <maas_dbuser> <maas_dbpass> <maas_dbname>"
    exit 1
fi

# Set MAAS configuration parameters
MAAS_DBUSER="$1"
MAAS_DBPASS="$2"
MAAS_DBNAME="$3"

# Update package list
sudo apt update -y

# Install MAAS by snap
sudo snap install maas

# Disable local NTP Client
sudo systemctl disable --now systemd-timesyncd

# Install PostgreSQL
sudo apt install -y postgresql-14

#Install ufw 
sudo apt install ufw -y
sudo apt update -y


# Create a PostgreSQL user
sudo -i -u postgres psql -c "CREATE USER \"$MAAS_DBUSER\" WITH ENCRYPTED PASSWORD '$MAAS_DBPASS';"

# Create the MAAS database
sudo -i -u postgres createdb -O "$MAAS_DBUSER" "$MAAS_DBNAME"

# Add parameters to the end of pg_hba.conf
echo "host    $MAAS_DBNAME             $MAAS_DBUSER             0/0            md5" | sudo tee -a /etc/postgresql/14/main/pg_hba.conf

# Inint the MAAS
sudo maas init region+rack --database-uri "postgres://$MAAS_DBUSER:$MAAS_DBPASS@$HOSTNAME/$MAAS_DBNAME"

#
# Restart PostgreSQL to apply changes
sudo systemctl restart postgresql

echo "MAAS installation completed successfully."

# ufw configuration
sudo ufw allow ssh, http, https, 5240/tcp, 5240/udp
sudo ufw enable
sudo ufw status
