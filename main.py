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
                Input("Enter the description:"),
            ],
            spacing=0
        )
        result = cli.launch()
        ret = subprocess.run(["vault", "kv", "patch", "-format=json", "-mount=secret", "oms/{}".format(result[0][1]), "password={}".format(result[1][1]), "description={}".format(result[2][1])], capture_output=True)
        if not ret.stdout.decode('utf-8'):
            # 数据库为空，需要先put一次
            ret = subprocess.run(["vault", "kv", "put", "-format=json", "-mount=secret", "oms/{}".format(result[0][1]), "password={}".format(result[1][1]), "description={}".format(result[2][1])], capture_output=True) 
        console.print("[green]Finish upsert server: [/green][sky_blue3]{}[/sky_blue3]".format(result[0][1]))

    def list(self):
        ret = subprocess.run(["vault", "kv", "list", "-format=json", "secret/oms"], capture_output=True)
        data = json.loads(ret.stdout.decode('utf-8'))

        console.print("[bold medium_purple]All servers are listed:[/bold medium_purple]")
        for k in data:
            ret = subprocess.run(["vault", "kv", "get", "-format=json", "-field=description", "-mount=secret", "oms/{}".format(k)], capture_output=True)
            console.print("[sky_blue3]{}[/sky_blue3]\t{}".format(k, json.loads(ret.stdout.decode('utf-8'))))

    def ssh(self):
        ret = subprocess.run(["vault", "kv", "list", "-format=json", "secret/oms"], capture_output=True)
        data = json.loads(ret.stdout.decode('utf-8'))
        cli = Bullet(
            prompt="Choose from the servers below:",
            choices=data
        )
        result = cli.launch()
        child = pexpect.spawn("ssh", [result], timeout=10, maxread=1)
        i = child.expect(["(?i)(?:password:)|(?:passphrase for key)", "(?i)are you sure you want to continue connecting", "Welcome",
                          pexpect.EOF, pexpect.TIMEOUT])
        if i == 0 or i == 1:
            ret = subprocess.run(["vault", "kv", "get", "-format=json", "-mount=secret", "oms/{}".format(result)], capture_output=True)
            data = json.loads(ret.stdout.decode('utf-8'))['data']['data']
            if i == 0:
                child.sendline("{}\n".format(data['password']))
                child.interact()
            else:
                child.sendline("yes\n")
                child.sendline("{}\n".format(data['password']))
                child.interact()
        elif i == 2:
            # 处理秘钥登录的情况
            print(child.after.decode(), end="")
            child.interact()

    def scp(self):
        print("call scp func")


def main():
    fire.Fire(OmsCli)


if __name__ == '__main__':
    main()
