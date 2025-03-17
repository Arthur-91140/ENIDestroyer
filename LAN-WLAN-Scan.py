import socket
import csv
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip_port_tuple):
    ip, port = ip_port_tuple
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return ip, port
    except socket.error:
        return None

def scan_ports(ip, ports):
    ip_port_tuples = [(ip, port) for port in ports]
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(scan_port, ip_port_tuples))
    
    open_ports = [port for result in results if result for ip, port in [result]]
    return open_ports

def main():
    subnet = "172.16.30.0/24"
    ports_to_scan = [20121, 20194]
    output_file = "ipv.csv"
    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'Open Ports']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        network = ipaddress.ip_network(subnet)
        for ip in network.hosts():
            ip_str = str(ip)
            print(f"Scanning IP: {ip_str}...")
            open_ports = scan_ports(ip_str, ports_to_scan)
            if open_ports:
                writer.writerow({'IP': ip_str, 'Open Ports': ', '.join(map(str, open_ports))})
                print(f"Found open ports {', '.join(map(str, open_ports))} on {ip_str}")

    print("Scan completed. Results saved in ipv.csv")

if __name__ == "__main__":
    main()
