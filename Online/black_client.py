from socket_client import HOST, PORT0
from relativistic_client import RelativisticClient, Display

if __name__ == '__main__':
    print('Black client started!')
    rc = RelativisticClient(host=HOST, port=PORT0)
    d = Display(rc, player_name='Black')
    rc.connect()
    rc.time_buffering()
    rc.start()
    d.main()
    rc.go = False
    rc.join()
    print('Main Good bye!')
