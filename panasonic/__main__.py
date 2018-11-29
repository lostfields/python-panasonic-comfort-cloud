import argparse
import json
import panasonic

def main():
    """ Start Panasonic Comfort Cloud command line """

    parser = argparse.ArgumentParser(
        description='Read or change status of Panasonic Climate devices')

    parser.add_argument(
        'username',
        help='Username for Panasonic Comfort Cloud')

    parser.add_argument(
        'password',
        help='Password for Panasonic Comfort Cloud')

    parser.add_argument(
        '-t', '--token',
        help='File to store token in',
        default='~/.panasonic-token')

    args = parser.parse_args()

    session = panasonic.Session(args.username, args.password, args.cookie)
    session.login()
    try:
        print('Yes')
        # session.set_giid(session.installations[args.installation - 1]['giid'])

        # if args.command == COMMAND_INSTALLATIONS:
        #     print_result(session.installations)

        # if args.command == COMMAND_OVERVIEW:
        #     print_result(session.get_overview(), *args.filter)
    
    except panasonic.ResponseError as ex:
        print(ex.text)


# pylint: disable=C0103
if __name__ == "__main__":
    main()