from config import MODE


class ModeManager:

    def is_live(self):
        return MODE == "LIVE"

    def is_paper(self):
        return MODE == "PAPER"


mode_manager = ModeManager()
