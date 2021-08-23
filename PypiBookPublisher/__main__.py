import argparse
import sys
from . import __version__
from . import *

def main():
    parser = argparse.ArgumentParser(prog="PypiBookPublisher", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version", action="version", version=f"PYBP version: {__version__}")
    parser.set_defaults(func=lambda x: parser.print_help())
    subparsers = parser.add_subparsers()
    
    pub_parser = subparsers.add_parser("publish", help="publish book")
    pub_parser.add_argument("dir", help="dir")
    pub_parser.set_defaults(func=publish)
    
    config_parser = subparsers.add_parser("config", help="configure token")
    config_parser.add_argument("token", help="token")
    config_parser.set_defaults(func=config)
    
    args = parser.parse_args()
    args.func(args)
    
if __name__ == '__main__': main()