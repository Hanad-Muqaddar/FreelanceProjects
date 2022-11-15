from getpass import getpass


class PasswordPrompt():
    def prompt(self):
        while True:
            self._password = getpass("Your Facebook password: ")

            if len(self._password) >= 6:
                break

        return self._password
