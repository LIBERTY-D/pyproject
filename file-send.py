import socket
import socketserver
import os
import argparse
import binascii
import random
server_address = "127.0.0.1"


class RequestHandlerClass(socketserver.BaseRequestHandler):
    def handle(self):
        count = random.randint(0, 1000)
        # receive data
        # may extension  3

        data = self.request.recv(8).decode("utf-8")
        print(data)
        ext = data.split(":")[1]
        if (ext == "htm"):
            ext = "html"
        if (data.startswith('SEND:')):
            print("RECEIVING:")

            with open(f'file{count}.{ext}', "wb") as f:
                while data:
                    data = bytearray(self.request.recv(512))
                    f.write(data)


def startServer(args):
    try:

        server = socketserver.TCPServer((
            server_address, args.port), RequestHandlerClass)
        print("[*]LISTENING..")
        server.serve_forever()
    except Exception as err:
        print("exited")


def startClient(args):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((args.IpAddress, args.port))
        print("[*]CONNECTED...")
        path, fle = os.path.split(args.file)
        ext = fle.split(".")[1]
        data = b'SEND:'+bytes(ext, "utf-8")
        # actuall data
        client.send(data)
        if (args.file):
            with open(f"{args.file}", "rb") as f:
                data = f.read(512)
                while data:
                    client.sendall(data)
                    data = f.read(512)
        print("FILE SEND: "+args.file)
        client.close()

    except Exception as err:
        print(err)


def main(args):
    if (args.client):
        startClient(args)
    elif (args.server):
        startServer(args)


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--client", action="store",
                        type=str, nargs="?", default=False, const=True, help="to specify client side runtime")
    parser.add_argument("-s", "--server", action="store",
                        type=str, nargs="?", default=False, const=True)
    parser.add_argument("-ip", "--IpAddress", action="store",
                        type=str, help="to specify server address")
    parser.add_argument("-p", "--port", action="store", type=int,
                        nargs="?", help="to specify server port")
    parser.add_argument("-f", "--file", action="store",
                        help="file to send", type=str)
    args = parser.parse_args()

    print(args)
    if (not args.client and not args.server):
        parser.print_help()
        print("Specify -s for server or -c or client")
        parser.exit()
    main(args)
