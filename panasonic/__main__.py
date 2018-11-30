import argparse
import json
import panasonic

def print_result(overview, *names):
    """ Print the result of a verisure request """
    if names:
        print(json.dumps(overview, indent=4, separators=(',', ': ')))
        # for name in names:
        #     toprint = overview
        #     for part in overview:
        #         toprint = toprint[part]
        #     print(json.dumps(toprint, indent=4, separators=(',', ': ')))
    else:
        print(json.dumps(overview, indent=4, separators=(',', ': ')))

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

    session = panasonic.Session(args.username, args.password, args.token)
    session.login()
    try:
        print_result(session.get_devices())

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