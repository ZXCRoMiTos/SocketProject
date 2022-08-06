from subprocess import Popen, PIPE
from ipaddress import ip_address
from tabulate import tabulate
import threading
import chardet
import re


reachable = []
unreachable = []


def stdout_decode(stdout):
    return stdout.decode(chardet.detect(stdout)["encoding"])


def check_connection(address, table=False):
    ping = Popen(["ping", str(address)], stdout=PIPE)
    if table:
        ping.wait(), unreachable.append((str(address), )) if ping.poll() else reachable.append((str(address), ))
    else:
        ping.wait(), print(f"Узел {address} недоступен") if ping.poll() else print(f"Узел {address} доступен")


def check_ip(address, ip_range=0, table=False):
    ping = Popen(["ping", address], stdout=PIPE)
    answer = re.search("\d+.\d+.\d+.\d+", stdout_decode(ping.stdout.read()))
    if answer:
        for num in range(0, ip_range + 1):
            threading.Thread(target=check_connection, args=[ip_address(answer.group()) + num, table]).start()


def host_ping(addresses):
    for address in addresses:
        threading.Thread(target=check_ip, args=[address]).start()


def host_range_ping(addresses, ip_range):
    for address in addresses:
        threading.Thread(target=check_ip, args=[address, ip_range]).start()


def host_range_ping_tab(addresses, ip_range):
    for address in addresses:
        threading.Thread(target=check_ip, args=[address, ip_range, True]).start()
    while True:
        if len(unreachable) + len(reachable) == len(addresses) * ip_range + len(addresses):
            break
    print(tabulate(reachable, headers=['Reachable']))
    print(tabulate(unreachable, headers=['Unreachable']))


if __name__ == "__main__":
    host_ping(["google.com", "142.250.180.238", "youtube.com", "142.251.39.78",
               "facebook.com", "185.60.218.35", "twitter.com", "104.244.42.129",
               "instagram.com", "185.60.218.174", "baidu.com", "110.242.68.66",
               "wikipedia.org", "91.198.174.192", "yandex.ru", "77.88.55.50"])
    host_range_ping(["google.com", "142.250.180.238", "youtube.com"], 5)
    host_range_ping_tab(["google.com", "142.250.180.238", "youtube.com"], 5)
