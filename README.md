## RoboMaster Live Capture
#### RM录播姬

### 功能
* 录制官方流，支持分辨率选择
* 自动切片、自动启动与停止录制
* 基于网页的管理面板
* 在线播放已经完成的录制
* 录制结束后自动封装为`.mp4`

### 工作原理
* 通过直接拉取官方直播间HLS流实现录制，直接保存`.ts`数据并拼接`.m3u8`索引
* 录制结束后调用ffmpeg将`.m3u8`无重编码封装为`.mp4`
* 通过拉取赛事流程JSON实现自动切片与自动启动和停止

### 通过压缩包部署
1. 安装Python。推荐使用Python 3.9或更高版本。
2. 从GitHub Release下载最新版本压缩包并解压。
   * 可以下载项目提供的`RM_Live_Capture.tar.gz`
   * 也可以下载GitHub自动生成的`Source code (zip)`
3. 打开终端，进入解压后的项目目录。
4. 创建Python虚拟环境。

Windows PowerShell：
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD：
```bat
python -m venv .venv
.\.venv\Scripts\activate.bat
```

macOS / Linux：
```bash
python3 -m venv .venv
source .venv/bin/activate
```

5. 进入`backend`目录并安装依赖。

Windows：
```powershell
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS / Linux：
```bash
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

6. 运行程序。

```bash
python main.py
```

程序启动后会自动打开Chrome浏览器，并访问：

```text
http://127.0.0.1:10398
```

如果浏览器没有自动打开，也可以手动输入上面的地址访问。

默认配置已关闭HTTP Basic Security，直接访问即可，无需用户名和密码。录制文件默认保存到：

```text
backend/out/data   # .ts 和 .m3u8
backend/out/mp4    # 自动封装后的 .mp4
```

系统已安装Ffmpeg时会优先使用系统Ffmpeg；未安装时会尝试使用Python依赖提供的Ffmpeg。暂停录制后，程序会自动将缺少MP4的录制补转换为`.mp4`。

### 编译部署（不推荐）
1. 安装必要依赖：NodeJs、Yarn、Python（系统已安装Ffmpeg时会优先使用；未安装时会尝试使用Python依赖提供的Ffmpeg）
2. Clone项目到本地并进入项目文件夹
3. 进入web目录，执行`yarn && yarn build`构建前端项目
4. 将`web/dist`目录中的所有文件拷贝到`backend/static`目录
5. 进入backend目录，执行`pip install -r requirements.txt`安装后端依赖
6. 编辑`config.py`修改相关配置（当前版本默认已关闭HTTP Basic Security，直接访问即可，无需密码）
7. 运行`main.py`启动程序
* 可选：执行`backend/video.py`可以将历史`.m3u8`文件批量封装为`.mp4`（该过程不会重新编解码，速度很快，不占用CPU）
