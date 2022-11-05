import paramiko
import argparse
import sys
import textwrap
import re
from colorama import Fore, Style, init
import random
init(autoreset=True)
def style():
    global success, output, info, fail
    output, info, fail = Fore.GREEN + Style.BRIGHT, Fore.WHITE, Fore.YELLOW + \
        Style.BRIGHT, Fore.RED + Style.BRIGHT


def banner():
    init(autoreset=True)
    styles = [Fore.LIGHTCYAN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX,Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTRED_EX, Fore.MAGENTA, Fore.CYAN, Fore.YELLOW, Fore.GREEN, Fore.RED]
    random_index = random.randint(0, len(styles)-1)

    print(styles[random_index] + "") 
    random_index = random.randint(0, len(styles)-1)
    print(Fore.CYAN +           '                _                   _             _ _           '+ Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + '               (_)                 | |           | | |          '+ Style.RESET_ALL)
    print(Fore.LIGHTMAGENTA_EX +'   ___ _____  ___    ___ ___  _ __ | |_ _ __ ___ | | | ___ _ __ '+ Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX +  '  / _ / __\ \/ | |  / __/ _ \|  _ \| __|  __/ _ \| | |/ _ | __| '+ Style.RESET_ALL)
    print(Fore.LIGHTRED_EX +    ' |  __\__ \>  <| | | (_| (_) | | | | |_| | | (_) | | |  __| |   '+ Style.RESET_ALL)
    print(Fore.CYAN +           '  \___|___/_/\_|_|  \___\___/|_| |_|\__|_|  \___/|_|_|\___|_|   \n' + Style.RESET_ALL)

def options():
    opt_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
        '''python3 esxicontroller.py -m
'''))
    opt_parser.add_argument(
        '-s', '--start', help='Starts the listed VM')
    opt_parser.add_argument(
        '-r', '--restart', help='Restarts the listed VM')
    opt_parser.add_argument(
        '-st', '--stop', help='Stops the listed VM')
    opt_parser.add_argument(
        '-l', '--list', help='Lists all VMs', action='store_true')
    opt_parser.add_argument('-g', '--getstate', help='Prints the power state of the listed VM')
    opt_parser.add_argument('-i', '--ip', help='ESXi IP', required=True)
    opt_parser.add_argument('-u', '--user', help='ESXi Username', required=True)
    opt_parser.add_argument('-pw', '--password', help='ESXi Password', required=False)
    opt_parser.add_argument('-p', '--port', help='ESXi Port', required=False)
    opt_parser.add_argument('-k', '--key', help='Utilize id_rsa public key authentication.', required=False)


    global args
    args = opt_parser.parse_args()
    if len(sys.argv) == 1:
        opt_parser.print_help()
        opt_parser.exit()
def ssh_command(ip, port, user, password):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=password, key_filename=args.key)
    print('Connected to ESXi server at ' + ip + '\n')

    try:
                
        if args.start:
            vm_id = args.start
            command = f'vim-cmd vmsvc/power.on {vm_id}'
            _, stdout, stderr = client.exec_command(command)
            output = stdout.readlines() + stderr.readlines()     
            for line in output:
                valid = re.search('Powering on VM:', line)
                if valid:
                    print(f'{line.strip()} {vm_id}')
                    break
        if args.stop:
            vm_id = args.stop
            command = f'vim-cmd vmsvc/power.off {vm_id}'
            _, stdout, stderr = client.exec_command(command)
            output = stdout.readlines() + stderr.readlines()     
            for line in output:
                valid = re.search('Powering off VM:', line)
                if valid:
                    print(f'{line.strip()} {vm_id}')
                    break
        if args.restart:
            vm_id = args.restart
            command = f'vim-cmd vmsvc/power.reboot {vm_id}'
            _, stdout, stderr = client.exec_command(command)
            output = stdout.readlines() + stderr.readlines()     
            for line in output:
                print(line.strip())
                break
        if args.list:        
            command = 'vim-cmd vmsvc/getallvms'
            _, stdout, stderr = client.exec_command(command)
            output = stdout.readlines() + stderr.readlines()       
            for line in output:
                print(line.strip())
                #quit()
        if args.getstate:        
            command = f'vim-cmd vmsvc/power.getstate {args.getstate}'
            _, stdout, stderr = client.exec_command(command)
            output = stdout.readlines() + stderr.readlines()      
            for line in output:
                print(line.strip())
                #quit()
    except Exception as e:
        quit()

if __name__ == '__main__':
    try:
        init()
        banner()
        options()
        user = args.user
        password = args.password
        ip = args.ip
        keyfile = args.key
        if keyfile is None:
            pass
        port = args.port
        if port is None:
            port = 22
        ssh_command(ip, port, user, password)
    except IndexError:
        print('Check parameters and try again')
