from portfolio.bybit_wallet import wallet


class PositionManager:


    def __init__(self):

        self.position = None


        print(
            "[POSITION MANAGER READY]"
        )



    def update(self):

        try:

            data = wallet.get_position()

            self.position = data


            return data


        except Exception as e:

            print(
                "[POSITION ERROR]",
                e
            )

            return None



    def has_position(self):


        if not self.position:

            return False



        try:

            size = float(
                self.position.get(
                    "size",
                    0
                )
            )


            return size != 0


        except:


            return False



    def side(self):

        if not self.position:

            return None


        return self.position.get(
            "side"
        )



position_manager = PositionManager()
