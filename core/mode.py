from config import MODE

class Mode:

    def is_paper(self):
        return MODE == "PAPER"

    def is_live(self):
        return MODE == "LIVE"

mode = Mode()
