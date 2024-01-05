## 使用 `pyinstaller --onefile --windowed --icon=logo.ico main.py` 构建.exe文件

在vscode中ctrl+shift+p打开命令面板，输入shell command:create environment，选择Python 3.8 (64-bit) - venv，创建环境

### 命令解释

--onefile:创建一个单一的可执行文件
--windowed:创建一个没有控制台的窗口化可执行文件

--icon=logo.ico:指定图标文件的位置

main.py:指定要打包的Python脚本文件

### 注意事项

