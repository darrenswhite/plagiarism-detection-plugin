from server.server import Server

server = Server()


def main():
    """
    Start the server
    """
    try:
        server.run()
    except KeyboardInterrupt:
        pass
