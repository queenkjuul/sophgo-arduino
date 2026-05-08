#!/usr/bin/env python3
import sys
import urllib.request
import os
import hashlib


def upload():
    if len(sys.argv) < 3:
        sys.exit(1)

    ip = sys.argv[1]
    file_path = sys.argv[2]
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    file_size = os.path.getsize(file_path)

    url_host = f"[{ip}]" if ":" in ip else ip
    url = f"http://{url_host}:65000/"


    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_hash = hashlib.md5(file_data).hexdigest()

            req = urllib.request.Request(url, data=file_data, method='POST')
            req.add_header('Content-Length', str(file_size))
            req.add_header('Content-Type', 'application/octet-stream')
            req.add_header('X-Binary-Hash', file_hash)

            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    print("OK")
                else:
                    print(f"Upload failed with status: {response.status}")
                    sys.exit(1)
    except Exception as e:
        print(f"Network Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    upload()
