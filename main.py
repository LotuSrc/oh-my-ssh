import base64
import os
import fire
import pexpect
import subprocess
import json
from bullet import Bullet, Password, Input, VerticalPrompt, ScrollBar, SlidePrompt


class OmsCli(object):

    def upsert(self):
        cli = VerticalPrompt(
            [
                Input("Enter the server name or ip:",),
                Password("Enter the password:"),
            ],
            spacing=0
        )
        result = cli.launch()
        ret = subprocess.run(["vault", "kv", "patch", "-format=json", "-mount=secret", "test", "{}={}".format(result[0][1], result[1][1])], capture_output=True)
        print(
            f"Finsh upsert server: {result[0][1]}")

    def list(self):
        pass

    def ssh(self):
        ret = subprocess.run(["vault", "kv", "get", "-format=json", "-mount=secret", "test"], capture_output=True)
        data = json.loads(ret.stdout.decode('utf-8'))['data']['data']
        cli = Bullet(
            prompt="Choose from the servers below:",
            choices=list(data.keys())
        )
        result = cli.launch()
        child = pexpect.spawn(f"ssh {result}")
        i = child.expect([".*password.*", ".*continue.*?",
                          pexpect.EOF, pexpect.TIMEOUT])
        if i == 0:
            child.sendline("{}\n".format(data[result]))
            child.interact()
        elif i == 1:
            child.sendline("yes\n")
            child.sendline("{}\n".format(data[result]))
            child.interact()

    def scp(self):
        print("call scp func")


def main():
    fire.Fire(OmsCli)


if __name__ == '__main__':
    main()
