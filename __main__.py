# from uniland import UniLand
from pyrogram import Client


if __name__ == "__main__":
    plugins = dict(
        root='uniland.plugins',
        include=[
            'jozve.jozve_handler',
            'start.start_handler',
            'back.back_handler',
            'help.help_handler',
            'ostad.ostad_handler',
            'apply.apply_handler',
            'reserve.reserve_handler',

            ]
        )
    Client(
        "uniland",
        plugins = plugins,
    ).run()
