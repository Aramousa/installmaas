
import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode(), error.decode(), process.returncode

def install_maas(maas_dbuser, maas_dbpass, maas_dbname):
    # Update the package list
    _, _, return_code = run_command("sudo apt update -y")
    if return_code != 0:
        print("Error updating package list. Exiting.")
        return

    # Install MAAS by snap
    _, _, return_code = run_command("sudo snap install maas")
    if return_code != 0:
        print("Error installing MAAS. Exiting.")
        return
    # Disable local NTP Client
    _, _, return_code = run_command("sudo systemctl disable --now systemd-timesyncd")
    if return_code != 0:
        print("Error Disabling NTP client. Exiting.")
        return

    # Initialise MAAS for production
    _, _, return_code = run_command("sudo apt update -y")
    if return_code != 0:
        print("Error Updating system, please check network connectivity. Exiting.")
        return


    # Initialise MAAS for production
    _, _, return_code = run_command("sudo apt install -y postgresql-14 ")
    if return_code != 0:
        print("Error installing postgresql 14. Exiting.")
        return
    MAAS_DBUSER= sys.argv[1]
    MAAS_DBPASS= sys.argv[2]
    MAAS_DBNAME= sys.argv[31]
    HOSTNAME= 'localhost'

    # Create a suitable PostgreSQL user
    _, _, return_code = run_command("sudo -i -u postgres psql -c 'CREATE USER \"$MAAS_DBUSER\" WITH ENCRYPTED PASSWORD '$MAAS_DBPASS''")
    if return_code != 0:
        print("Error create user for postgresql. Exiting.")
        return

    # Create the MAAS database
    _, _, return_code = run_command("sudo -i -u postgres createdb -O '$MAAS_DBUSER' '$MAAS_DBNAME' ")
    if return_code != 0:
        print("Error create user for postgresql. Exiting.")
        return

if __name__ == "__main__":
    install_maas()

