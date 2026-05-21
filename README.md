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

### 部署
1. 安装必要依赖：Python、Ffmpeg
2. 从release中下载最新版本`RM_Live_Capture.tar.gz`并解压
3. 进入backend目录，执行`pip install -r requirements.txt`安装后端依赖
4. 编辑`config.py`修改相关配置（特别注意修改HTTP Basic Security的账号密码）
5. 如修改了默认路径，请创建`config.py`中对应的两个存储路径；默认路径会使用`backend/out/data`和`backend/out/mp4`
6. 运行`main.py`启动程序

### 编译部署（不推荐）
1. 安装必要依赖：NodeJs、Yarn、Python、Ffmpeg
2. Clone项目到本地并进入项目文件夹
3. 进入web目录，执行`yarn && yarn build`构建前端项目
4. 将`web/dist`目录中的所有文件拷贝到`backend/static`目录
5. 进入backend目录，执行`pip install -r requirements.txt`安装后端依赖
6. 编辑`config.py`修改相关配置（特别注意修改HTTP Basic Security的账号密码）
7. 运行`main.py`启动程序
* 可选：执行`backend/video.py`可以将历史`.m3u8`文件批量封装为`.mp4`（该过程不会重新编解码，速度很快，不占用CPU）
