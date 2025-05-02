#!/usr/bin/env python3

"""
FlowStitch v1.0.0
Developer: HxN0n3
"""

import pyshark
import re

def print_banner():
    print(r"""
███████╗██╗      ██████╗ ██╗    ██╗███████╗████████╗██╗████████╗ ██████╗██╗  ██╗
██╔════╝██║     ██╔═══██╗██║    ██║██╔════╝╚══██╔══╝██║╚══██╔══╝██╔════╝██║  ██║
█████╗  ██║     ██║   ██║██║ █╗ ██║███████╗   ██║   ██║   ██║   ██║     ███████║
██╔══╝  ██║     ██║   ██║██║███╗██║╚════██║   ██║   ██║   ██║   ██║     ██╔══██║
██║     ███████╗╚██████╔╝╚███╔███╔╝███████║   ██║   ██║   ██║   ╚██████╗██║  ██║
╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝   ╚═╝   ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝

                        FlowStitch v1.0.0 - Dev: HxN0n3
    """)
    print("=== FlowStitch: HTTP Fragment Reassembler ===\n")


def flowstitch(pcap_file, content_type, output_image):
    print(f"[+] Reading {pcap_file} for content-type '{content_type}'\n")

    try:
        cap = pyshark.FileCapture(pcap_file, display_filter='http')
    except Exception as e:
        print(f"[!] Error opening pcap file: {e}")
        return

    fragments = []

    for packet in cap:
        try:
            http = packet.http
            if (
                hasattr(http, 'content_range') and
                hasattr(http, 'request_in') and
                hasattr(http, 'content_type') and
                http.content_type == content_type and
                hasattr(http, 'file_data')
            ):
                match = re.search(r'bytes\s+(\d+)-(\d+)', http.content_range)
                if match:
                    start = int(match.group(1))
                    hex_data = http.file_data.replace(':', '')  # clean hex
                    fragments.append((start, hex_data))
        except AttributeError:
            continue

    if not fragments:
        print("[!] No matching HTTP fragments found.")
        return

    # Sort and merge
    fragments.sort(key=lambda x: x[0])
    merged_hex = ''.join([frag[1] for frag in fragments])

    # Write to binary image
    try:
        with open(output_image, "wb") as f:
            f.write(bytes.fromhex(merged_hex))
        print(f"[+] Image reconstructed successfully → {output_image}")
    except Exception as e:
        print(f"[!] Failed to write image: {e}")

if __name__ == "__main__":
    print_banner()
    pcap_file = input("Enter PCAP filename (e.g., forensic.pcap): ").strip()
    content_type = input("Enter HTTP Content-Type (e.g., image/jpeg): ").strip()
    output_file = input("Enter output image filename (e.g., final.jpeg): ").strip()
    flowstitch(pcap_file, content_type, output_file)
