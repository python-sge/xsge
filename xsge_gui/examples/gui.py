#!/usr/bin/env python3

# GUI Example
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.


import sge
import xsge_gui


class Game(sge.dsp.Game):

    def event_game_start(self):
        sge.keyboard.set_repeat(interval=10, delay=500)

    def event_close(self):
        self.end()


class Room(sge.dsp.Room):

    def event_room_start(self):
        self.handler = xsge_gui.Handler.create()

        window = xsge_gui.Window(self.handler, 8, 8, 240, 240,
                                 title="Test window 1")
        button = xsge_gui.Button(window, 8, 8, 0, "My button")
        xsge_gui.Label(window, 8, 32, 0, "My label")
        xsge_gui.Label(window, 8, 64, 0, "my label " * 50, width=224)
        button2 = xsge_gui.Button(window, 16, 100, 5, "Another button",
                                  width=150)

        def event_press(handler=self.handler):
            xsge_gui.show_message(parent=handler,
                                  message="You just pressed my buttons!")

        button.event_press = event_press

        def event_press(handler=self.handler):
            name = xsge_gui.get_text_entry(parent=handler,
                                           message="Who are you?!")
            if name:
                m = "{}? That's a suspicious name!".format(name)
            else:
                m = "Won't talk, eh? I've got my eye on you!"

            xsge_gui.show_message(parent=handler, message=m)

        button2.event_press = event_press

        window.show()

        window2 = xsge_gui.Window(self.handler, 480, 200, 320, 320,
                                  title="Test window 2")
        xsge_gui.CheckBox(window2, 16, 16, 0)
        xsge_gui.RadioButton(window2, 16, 48, 0)
        xsge_gui.RadioButton(window2, 16, 80, 0)
        xsge_gui.RadioButton(window2, 16, 112, 0)
        xsge_gui.ProgressBar(window2, 16, 144, 0, 288, progress=0.5)
        xsge_gui.TextBox(window2, 16, 176, 0, width=288, text="mytext")
        window2.show()


def main():
    Game(width=800, height=600)
    xsge_gui.init()
    sge.game.start_room = Room()
    sge.game.start()


if __name__ == '__main__':
    main()
