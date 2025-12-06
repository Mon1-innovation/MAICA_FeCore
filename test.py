import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"新的客户端连接: {addr}")
    
    # 发送欢迎消息
    welcome = "欢迎！发送 'exit' 退出连接。\n"
    writer.write(welcome.encode())
    await writer.drain()
    
    try:
        while True:
            # 等待客户端消息
            data = await reader.read(1024)
            if not data:
                break
                
            message = data.decode().strip()
            print(f"来自 {addr} 的消息: {message}")
            
            if message.lower() == 'exit':
                response = "再见！\n"
            else:
                response = f"收到: {message}\n"
            
            # 发送回应
            writer.write(response.encode())
            await writer.drain()
            
            if message.lower() == 'exit':
                break
                
    except Exception as e:
        print(f"与 {addr} 通信时出错: {e}")
    finally:
        print(f"关闭连接: {addr}")
        writer.close()
        await writer.wait_closed()

async def main():
    """
    主函数，启动服务器
    """
    # 配置服务器参数
    host = '127.0.0.1'
    port = 8888
    
    try:
        # 启动服务器
        server = await asyncio.start_server(
            handle_client,  # 客户端处理函数
            host,           # 监听地址
            port            # 监听端口
        )
        
        # 获取服务器监听的地址和端口
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f"服务器启动，监听地址: {addrs}")
        print(f"使用 'telnet {host} {port}' 或 'nc {host} {port}' 进行测试")
        
        # 持续运行服务器
        async with server:
            await server.serve_forever()
            
    except OSError as e:
        print(f"无法启动服务器: {e}")
        print(f"请检查端口 {port} 是否已被占用")
    except KeyboardInterrupt:
        print("\n服务器正在关闭...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("服务器已停止")