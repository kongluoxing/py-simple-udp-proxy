#! /usr/bin/env python
# coding: utf-8

import argparse
import socket
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--bind-address',
                        help='The address to bind, use 0.0.0.0 for all ip address.',
                        type=str)
    parser.add_argument('--port',
                        help='The port to listen, eg. 623.',
                        type=int)
    parser.add_argument('--dst-ip',
                        help='Destination host ip, eg. 192.168.3.101.',
                        type=str)
    parser.add_argument('--dst-port',
                        help='Destination host port, eg. 623.',
                        type=int)

    return parser.parse_args()

namespace = parse_args()


def recv():
    sock_src = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_dst = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_addr = (namespace.bind_address, namespace.port)
    dst_addr = (namespace.dst_ip, namespace.dst_port)
    sock_src.bind(recv_addr)

    while True:
        data, addr = sock_src.recvfrom(65565)
        if not data:
            print('an error occured')
            break
        logger.debug('received: {0!r} from {1}'.format(data, addr))
        sock_dst.sendto(data, dst_addr)
        data, paddr = sock_dst.recvfrom(65565)
        sock_src.sendto(data, addr)

    sock_src.close()
    sock_dst.close()


if __name__ == '__main__':
    parse_args()
    try:
        recv()
    except KeyboardInterrupt:
        exit(0)
