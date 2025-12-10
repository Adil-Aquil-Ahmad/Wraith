import os
import json
import socket

class ServerManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.servers_dir = os.path.join(base_dir, "tor", "servers")
        self.status_file = os.path.join(base_dir, "server_status.json")
        os.makedirs(self.servers_dir, exist_ok=True)
    
    def get_server_dir(self, server_num):
        return os.path.join(self.servers_dir, f"server_{server_num}")
    
    def is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0
    
    def is_server_running(self, server_num):
        port = 8000 + server_num
        return self.is_port_in_use(port)
    
    def get_server_port(self, server_num):
        return 8000 + server_num
    
    def get_onion_address(self, server_num):
        server_dir = self.get_server_dir(server_num)
        hostname_file = os.path.join(server_dir, "hostname")
        
        if os.path.exists(hostname_file):
            with open(hostname_file, 'r') as f:
                return f.read().strip()
        return None
    
    def load_status(self):
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_status(self, status):
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
