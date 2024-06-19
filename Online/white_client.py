from socket_client import HOST, PORT1
from relativistic_client import RelativisticClient

if __name__ == '__main__':
    print('White client started!')
    rc = RelativisticClient(host=HOST, port=PORT1)
    rc.connect()
    rc.time_buffering()
    rc.start()
    # input('Press any key to exit...')
    # rc.go = False
    rc.join()
    print('Main Good bye!')
