import base64
import os
import fire
import pexpect
import subprocess
import json
from rich.console import Console
from bullet import Bullet, Password, Input, VerticalPrompt, ScrollBar, SlidePrompt


console = Console()

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
        if not ret.stdout.decode('utf-8'):
            # 数据库为空，需要先put一次
            ret = subprocess.run(["vault", "kv", "put", "-format=json", "-mount=secret", "test", "{}={}".format(result[0][1], result[1][1])], capture_output=True) 
        console.print("[green]Finish upsert server: [/green][sky_blue3]{}[/sky_blue3]".format(result[0][1]))

    def list(self):
        ret = subprocess.run(["vault", "kv", "get", "-format=json", "-mount=secret", "test"], capture_output=True)
        data = json.loads(ret.stdout.decode('utf-8'))['data']['data']
        console.print("[bold medium_purple]All servers are listed:[/bold medium_purple]")
        for k in data.keys():
            console.print("[sky_blue3]{}[/sky_blue3]".format(k))

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
