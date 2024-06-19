from socket_client import HOST, PORT1
from relativistic_client import RelativisticClient, Display

if __name__ == '__main__':
    print('White client started!')
    rc = RelativisticClient(host=HOST, port=PORT1)
    d = Display(rc, player_name='White')
    rc.connect()
    rc.time_buffering()
    rc.start()
    d.main()
    rc.go = False
    rc.join()
    print('Main Good bye!')
