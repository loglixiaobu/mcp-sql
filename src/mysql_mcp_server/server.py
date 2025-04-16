import asyncio
import logging
import os
from mysql.connector import connect, Error
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
from pydantic import AnyUrl

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mysql_mcp_server")

def get_db_config():
    """
    从环境变量中获取数据库配置。
    如果缺少必要的配置（用户、密码或数据库名），将抛出异常。
    """
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE")
    }
    
    if not all([config["user"], config["password"], config["database"]]):
        logger.error("缺少必要的数据库配置。请检查环境变量：")
        logger.error("MYSQL_USER, MYSQL_PASSWORD 和 MYSQL_DATABASE 是必需的")
        raise ValueError("缺少必要的数据库配置")
    
    return config

# 初始化 MCP 服务器
app = Server("mysql_mcp_server")

@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    列出 MySQL 数据库中的表作为资源。
    每个表被表示为一个 Resource 对象。
    """
    config = get_db_config()
    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                logger.info(f"找到的表：{tables}")
                
                resources = []
                for table in tables:
                    resources.append(
                        Resource(
                            uri=f"mysql://{table[0]}/data",
                            name=f"表: {table[0]}",
                            mimeType="text/plain",
                            description=f"表中的数据: {table[0]}"
                        )
                    )
                return resources
    except Error as e:
        logger.error(f"列出资源失败：{str(e)}")
        return []

@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """
    读取指定表的内容。
    参数:
        uri: 表的 URI，例如 mysql://table_name/data
    返回:
        表的内容，格式为 CSV。
    """
    config = get_db_config()
    uri_str = str(uri)
    logger.info(f"读取资源：{uri_str}")
    
    if not uri_str.startswith("mysql://"):
        raise ValueError(f"无效的 URI 协议：{uri_str}")
        
    parts = uri_str[8:].split('/')
    table = parts[0]
    
    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table} LIMIT 100")
                columns = [desc[0] for desc in cursor.description]  # 获取列名
                rows = cursor.fetchall()  # 获取行数据
                result = [",".join(map(str, row)) for row in rows]
                return "\n".join([",".join(columns)] + result)  # 返回 CSV 格式的内容
                
    except Error as e:
        logger.error(f"读取资源 {uri} 时发生数据库错误：{str(e)}")
        raise RuntimeError(f"数据库错误：{str(e)}")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    列出可用的工具。
    当前仅支持执行 SQL 查询的工具。
    """
    logger.info("列出工具...")
    return [
        Tool(
            name="execute_sql",
            description="在 MySQL 服务器上执行 SQL 查询",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "要执行的 SQL 查询"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    执行指定的工具。
    参数:
        name: 工具名称，目前仅支持 "execute_sql"。
        arguments: 工具的参数，例如 SQL 查询。
    返回:
        执行结果，格式为 TextContent。
    """
    config = get_db_config()
    logger.info(f"调用工具：{name}，参数：{arguments}")
    
    if name != "execute_sql":
        raise ValueError(f"未知工具：{name}")
    
    query = arguments.get("query")
    if not query:
        raise ValueError("查询语句是必需的")
    
    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                
                # 特殊处理 SHOW TABLES 查询
                if query.strip().upper().startswith("SHOW TABLES"):
                    tables = cursor.fetchall()
                    result = ["Tables_in_" + config["database"]]  # 表头
                    result.extend([table[0] for table in tables])
                    return [TextContent(type="text", text="\n".join(result))]
                
                # 处理 SELECT 查询
                elif query.strip().upper().startswith("SELECT"):
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    result = [",".join(map(str, row)) for row in rows]
                    return [TextContent(type="text", text="\n".join([",".join(columns)] + result))]
                
                # 处理非 SELECT 查询
                else:
                    conn.commit()
                    return [TextContent(type="text", text=f"查询成功执行。受影响的行数：{cursor.rowcount}")]
                
    except Error as e:
        logger.error(f"执行 SQL '{query}' 时发生错误：{e}")
        return [TextContent(type="text", text=f"执行查询时发生错误：{str(e)}")]

async def main():
    """
    MCP 服务器的主入口。
    初始化并运行服务器。
    """
    from mcp.server.stdio import stdio_server
    
    logger.info("启动 MySQL MCP 服务器...")
    config = get_db_config()
    logger.info(f"数据库配置：{config['host']}/{config['database']}，用户：{config['user']}")
    
    async with stdio_server() as (read_stream, write_stream):
        try:
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
        except Exception as e:
            logger.error(f"服务器错误：{str(e)}", exc_info=True)
            raise

if __name__ == "__main__":
    # 启动异步主函数
    asyncio.run(main())