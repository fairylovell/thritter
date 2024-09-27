from thritter import Thritter
import asyncio
import signal

stop_signal = False

def handler(signum, frame):
    global stop_signal
    stop_signal = True

# signal.signal(signal.SIGINT, handler)

async def main():
    thritter = Thritter()
    await thritter.load_config()

    while stop_signal == False:
        await thritter.update()
        await asyncio.sleep(60)

    await thritter.close_gracefully()

if __name__ == "__main__":
    asyncio.run(main())
