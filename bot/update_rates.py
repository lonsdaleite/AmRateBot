import asyncio
import aioschedule
import bot.common
from add_rates import add_all_rates


async def update_rates():
    add_all_rates(bot.common.all_rates)


async def scheduler(bot):
    aioschedule.every(20).minute.do(update_rates)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def run(dp):
    asyncio.create_task(scheduler(dp.bot))
