from bandapi import config


if __name__ == "__main__":
    print('''
    Hi! this is a initial setup for this api wrapper.
    ''')

    if not config.ACCESS_TOKEN:
        print('''
        It seems that you did not put your Access Token for Band API.
        Please make sure you put your Access Token in ./bandapi/config.py.
        ''')
        return

    print('''
    Setup complete!
    ''')
