from socket_client import HOST, PORT0
from relativistic_client import RelativisticClient

if __name__ == '__main__':
    print('Black client started!')
    rc = RelativisticClient(host=HOST, port=PORT0)
    rc.connect()
    rc.time_buffering()
    rc.start()
    input('Press any key to exit...')
    rc.go = False
    rc.join()
    print('Main Good bye!')
