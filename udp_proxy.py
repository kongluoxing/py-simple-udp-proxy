#! /usr/bin/env python
#coding: utf-8

import argparse
import socket


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--bind-address',
                        help='The address to bind, use 0.0.0.0 for all ip address.',
                        type=str)
    parser.add_argument('--port',
                        help='The port to listen, eg. 623.',
                        type=int)
    parser.add_argument('--dest-ip',
                        help='Destination host ip, eg. 192.168.3.101.',
                        type=str)
    parser.add_argument('--dest-port',
                        help='Destination host port, eg. 623.',
                        type=int)
    parser.add_argument('--src-ip',
                        help='Only allowed packages from src-ip.',
                        type=str)

    return parser.parse_args()

namespace = parse_args()


def recv():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_addr = (namespace.bind_address, namespace.port)
    send_addr = (namespace.dest_ip, namespace.dest_port)
    s.bind(recv_addr)

    while True:
        data, addr = s.recvfrom(65565)
        if not data:
            print('an error occured')
            break
        print('received: {0} from {1}'.format(data, addr))
        s.sendto(data, send_addr)
        print('send message: {0} to {1}'.format(data, send_addr))

    s.close()


if __name__ == '__main__':
    parse_args()
    try:
        recv()
    except KeyboardInterrupt:
        exit(0)
