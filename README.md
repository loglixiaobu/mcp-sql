# MCP Server for MySQL

 

#  

# **1.** ***\*安装vscode和mysql\****

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps1.jpg) 

可以上网查阅资料，这里不展开

[VSCode安装配置使用教程（最新版超详细保姆级含插件）一文就够了_vscode使用教程-CSDN博客](https://blog.csdn.net/msdcp/article/details/127033151)

[Windows环境下MySQL安装与配置（超详细、超细致）_mysql在windows系统下-CSDN博客](https://blog.csdn.net/weixin_45896437/article/details/132030152)

 

下面是我的实验数据库：

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps2.jpg) 

# ***\*2.在vscode中安装cline插件\****

## **1.找到左边的拓展**

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps3.jpg) 

 

## 2. **搜索cline，并安装，有中文版和英文版的，我们安装** **英文版的**

[VSCode神级AI插件Cline：从安装到实战【创建微信小程序扫雷】_cline编程助手 创建漂亮html-CSDN博客](https://blog.csdn.net/2401_84380512/article/details/145955009)

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps4.jpg) 

 

***\*安装好后，重启vscode，注册并配置cline：\****

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps5.jpg) 

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps6.jpg) 

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps7.jpg) 

 

***\*这里可以选择DeepSeek，但是DeepSeek API调用要钱，所以我还是选择cursor：\****

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps8.jpg) 

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps9.jpg) 

 

***\*我们的MCP-SERVER就可以在这里配置了，具体配置见三：\****

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps10.jpg) 

 

 

# ***\*3.项目重点，MCP-Server的配置\****

## **第一种方法：可以自己开发，具体参考：**

[Spring AI MCP Server + Cline 快速搭建一个数据库 ChatBi 助手_mysql  mcp server-CSDN博客](https://blog.csdn.net/qq_43692950/article/details/146770666)

jdk版本17及以上，具体可以参考下列博客：

[jdk21下载、安装（Windows、Linux、macOS）-CSDN博客](https://blog.csdn.net/weixin_68416970/article/details/145854183)

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps11.jpg) 

Spring-boot版本 3以上：

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps12.jpg) 

 

## **第二种方法：直接在****Smithery****中配置即可**

[GitHub - designcomputer/mysql_mcp_server：支持与 MySQL 数据库安全交互的模型上下文协议 （MCP） 服务器](https://github.com/designcomputer/mysql_mcp_server)

简单来说，Smithery就像是一个"AI服务超市"，开发者可以在这里：

· 快速找到现成的智能服务

· 一键部署到自己的项目中

· 加速AI应用开发流程

 

注册登录Smithery:

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps13.jpg) 

Search输入：npx -y @smithery/cli@latest inspect @f4ww4z/mcp-mysql-server

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps14.jpg) 

 

选择这个：

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps15.jpg) 

 

然后在install页面选择cline:

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps16.jpg) 

 

终端运行命令：>npx -y @smithery/cli@latest install @f4ww4z/mcp-mysql-server --client cline --key 89a9f140-aa68-42cc-8b0d-77449e67533c（根据自己的来）

报错的话，大概率是因为你没有配置Node.js环境，问一下大模型就行

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps17.jpg) 

 

安装成功后：打开vscode，打开左侧的cline，会出现一个json文件：

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps18.jpg) 

 

修改为：

{  

 "mcpServers": {  

  "mcp - mysql - server": {  

   "command": "cmd",  

   "args": [  

​    "/c",  

​    "npx",  

​    "-y",  

​    "@smithery/cli@latest",  

​    "run",  

​    "@f4ww4z/mcp - mysql - server",  

​    "--key",  

​    "89a9f140 - aa68 - 42cc - 8b0d - 77449e67533c" 

   ],  

   "env": {  

​    "MYSQL_HOST": "localhost",  

​    "MYSQL_USER": "你的用户名",  

​    "MYSQL_PASSWORD": "你的密码",  

​    "MYSQL_DATABASE": "数据库名称" 

   }  

  }  

 }  

}  

 

 

## **配置完成后：重启cline，就可以实现自然语言查询数据库啦！！下面进行一些测试：**

 

## **测试1：查询数据库：**

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps19.jpg) 

 

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps20.jpg) 

***\*大模型自动在终端调用命令查询：\****

 

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps21.jpg) 

 

 

## **测试2：查询test的表结构,成功查询到我的实验表t1**

## ![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps22.jpg) 

## ![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps23.jpg) 

 

## **测试3：查询t1的内容**

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps24.jpg) 

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps25.jpg) 

 

 

## **测试4：上面是查询，下面进行内容的修改，成功插入**

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps26.jpg) 

 

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps27.jpg) 

 

## **测试5：测试删除：成功删除**

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps28.jpg) 

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps29.jpg) 

 

## **测试6：最后一个测试，输出按pass逆向输出：**

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps30.jpg) 

![img](file:///C:\Users\xiaobu\AppData\Local\Temp\ksohtml3968\wps31.jpg) 

 
