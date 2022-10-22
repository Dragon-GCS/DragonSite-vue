#!/usr/bin/python3
import server.cli as cli
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage users and database(TODO)")
    subparser = parser.add_subparsers()
    users = subparser.add_parser("user", help="Manage users")
    users.add_argument("action", choices=["add", "drop"], help="Action to perform")
    users.add_argument("username", help="Username")
    users.add_argument("password", help="Password")
    users.add_argument("--admin", action="store_true", help="Create admin user")
    args = parser.parse_args()
    if args.action == "add":
        cli.create_user(args.username, args.password, args.admin)
    if args.action == "remove":
        cli.remove_user(args.username, args.password)