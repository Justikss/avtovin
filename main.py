import asyncio

from loader import *
import handlers





if __name__ == "__main__":
    # dp.startup.register(set_main_menu)

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(start_bot())


