import argparse
import sys
from . import __version__
from . import *

def main():
    parser = argparse.ArgumentParser(prog="BookerPubTool", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version", action="version", version=f"PYBP version: {__version__}")
    parser.set_defaults(func=lambda x: parser.print_help())
    subparsers = parser.add_subparsers()
    
    pypi_pub_parser = subparsers.add_parser("pub-pypi", help="publish book to pypi")
    pypi_pub_parser.add_argument("dir", help="dir")
    pypi_pub_parser.set_defaults(func=publish_pypi)
    
    pypi_config_parser = subparsers.add_parser("conf-pypi", help="configure pypi token")
    pypi_config_parser.add_argument("token", help="token")
    pypi_config_parser.set_defaults(func=config_pypi)
    
    args = parser.parse_args()
    args.func(args)
    
if __name__ == '__main__': main()