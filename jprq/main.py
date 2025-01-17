import argparse
import asyncio
from getpass import getuser
from .username import randomize
from .tunnel import open_tunnel
from . import __version__


def main():
    parser = argparse.ArgumentParser(description='Live And HTTPS Localhost')
    parser.add_argument('port', type=int, help='Port number of the local server')
    parser.add_argument('--host', type=str, help='Host of the remote server', default='cloudberry.live')
    parser.add_argument('-s', '--subdomain', type=str, help='Sub-domain')
    parser.add_argument('-v', '--version', action="version",version=__version__, help='Version number of jprq')

    args = parser.parse_args()

    
    if not args.port:
        print("Please specify -p/--port argument and port.")
        return
        
    username = args.subdomain or randomize(getuser())

    loop = asyncio.get_event_loop()

    print(f"\n {__version__}{'Press Ctrl+C to quit.':>60}\n")

    try:
        loop.run_until_complete(
            open_tunnel(
                ws_uri=f'wss://{args.host}/_ws/?username={username}&port={args.port}&version={__version__}',
                http_uri=f'http://127.0.0.1:{args.port}',
            )
        )
    except KeyboardInterrupt:
        print("\njprq tunnel closed")
