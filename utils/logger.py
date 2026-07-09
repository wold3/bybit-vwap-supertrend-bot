import logging
import os



LOG_DIR = "logs"



if not os.path.exists(LOG_DIR):

    os.makedirs(LOG_DIR)






def create_logger(
        name,
        filename
):


    logger = logging.getLogger(name)


    logger.setLevel(
        logging.INFO
    )



    if not logger.handlers:


        handler = logging.FileHandler(

            os.path.join(
                LOG_DIR,
                filename
            ),

            encoding="utf-8"

        )



        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s"

        )


        handler.setFormatter(
            formatter
        )


        logger.addHandler(
            handler
        )



    return logger







bot_logger = create_logger(

    "bot",

    "bot.log"

)



order_logger = create_logger(

    "order",

    "order.log"

)



error_logger = create_logger(

    "error",

    "error.log"

)
