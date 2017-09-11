import asyncio
import command
import namespace


ENCODING = 'utf8'
READ_CHUNK = 4096
EXIT = 'exit'


async def handle_echo(reader, writer):

    namespaces = namespace.NamespaceManager()

    should_loop = True
    while should_loop:

        writer.write('not-redis> '.encode(ENCODING))

        data = await reader.read(READ_CHUNK)
        message = data.decode()

        if message.strip() == EXIT:
            should_loop = False
        else:
            result = command.exec_command(message, namespaces)
            writer.write(result.encode(ENCODING))
            writer.write('\n'.encode(ENCODING))
        await writer.drain()

    print("Close the client socket")
    writer.close()


def main():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    main()
