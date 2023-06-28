#### 第一步：打开谷歌浏览器所在的目录：

![1687953730392](C:\Users\Lenovo\AppData\Local\Temp\1687953730392.png)

在上面红色框中输入 cmd，进入命令行窗口。

#### 第二步：输入命令

```
chrome.exe --remote-debugging-port=9527 --user-data-dir="D:\大三下课程笔记和PPT\项目实训\chrome"
```

该命令用于创建一个新的谷歌浏览器，其中端口9527不用改，改了也没事，但是改了之后得在程序中做相应的修改。 --user-data-dir的值是只要是一个合理的文件夹目录即可。如图：

![1687954024589](C:\Users\Lenovo\AppData\Local\Temp\1687954024589.png)

#### 第三步：在新创建出来的谷歌浏览器中登录chatGPT,这样就可以避免用程序模拟登录被检测的问题。

![1687954298940](C:\Users\Lenovo\AppData\Local\Temp\1687954298940.png)

#### 第四步：

由于我没有将prompt写入程序，所以第一个prompt需要自己手动复制到chatGPT中。

#### 第五步：启动脚本程序，自动执行。