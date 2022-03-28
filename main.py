import base64
import os
import configparser
import fire
import pexpect
from config import *
from bullet import Bullet, Password, Input, VerticalPrompt, ScrollBar, SlidePrompt


class OmsCli(object):

    def upsert(self):
        config = configparser.ConfigParser()
        config.read(OH_MY_SSH_PATH)
        cli = VerticalPrompt(
            [
                Input("Enter the server name or ip:",),
                Password("Enter the password:"),
            ],
            spacing=0
        )
        result = cli.launch()
        config[result[0][1]] = {"psw": result[1][1]}
        with open(OH_MY_SSH_PATH, 'w') as f:
            config.write(f)
        print(
            f"Finsh upsert server: {result[0][1]}")

    def list(self):
        pass

    def ssh(self):
        config = configparser.ConfigParser()
        config.read(OH_MY_SSH_PATH)
        print(OH_MY_SSH_PATH)
        cli = Bullet(
            prompt="Choose from the servers below:",
            choices=config.sections()
        )
        result = cli.launch()
        child = pexpect.spawn(f"ssh {result}")
        i = child.expect([".*password.*", ".*continue.*?",
                          pexpect.EOF, pexpect.TIMEOUT])
        if i == 0:
            child.sendline(f"{config.get(result, 'psw')}\n")
            child.interact()
        elif i == 1:
            child.sendline("yes\n")
            child.sendline(f"{config.get(result, 'psw')}\n")
            child.interact()

    def scp(self):
        print("call scp func")


def main():
    fire.Fire(OmsCli)


if __name__ == '__main__':
    main()
