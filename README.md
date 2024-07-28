# 鹿乃子乃子乃子虎视眈眈 字幕仓库

该仓库存放以`北宇治字幕组`名义制作的TV动画《鹿乃子乃子乃子虎视眈眈》 字幕。

![ShikaNoko](https://github.com/user-attachments/assets/c6d67091-5acd-471c-867a-de0b8e458e4c)

## 下载字幕

[![status badge main branch](https://github.com/Kitauji-Sub/subs-shikanoko/actions/workflows/build-subtitle.yml/badge.svg?branch=main)](https://github.com/Kitauji-Sub/subs-shikanoko/releases/latest) ![GitHub Release](https://img.shields.io/github/v/release/Kitauji-Sub/subs-shikanoko)


可前往 Releases 下载最新字幕文件：[Release](https://github.com/Kitauji-Sub/subs-shikanoko/releases/latest)

可在此处下载所使用的字体：[字体](https://github.com/Kitauji-Sub/subs-shikanoko/releases/tag/typeface)


<!-- |分支|说明|下载|
|-|-|:-:|
|`latest`|`main`持续集成的分支，拥有最新改动，部分显示可能会不正常|[点此下载](https://github.com/Kitauji-Sub/subs-shikanoko/releases/tag/latest)|
|`tv`|适配网络放送版TV播放源（例如CR）的稳定分支|[点此下载](https://github.com/Kitauji-Sub/subs-shikanoko/releases/tag/tv-1.0)| -->

## 开发

### 环境需求

+ Aegisub
  + [DependencyControl (optional)](https://github.com/TypesettingTools/DependencyControl)
  + [Merge Scripts](https://github.com/TypesettingTools/Myaamori-Aegisub-Scripts)
  + [The0x539's templater](https://github.com/The0x539/Aegisub-Scripts/blob/trunk/src/0x.KaraTemplater.moon)
+ Python 3.x
  + SubDigest
  + [assdiff3](https://github.com/TypesettingTools/assdiff3)

> [!CAUTION]
> 现有仓库中的Merge Scripts存在一个bug，会使导出的字幕文件中存在重复样式。
>
> 参见https://github.com/TypesettingTools/Myaamori-Aegisub-Scripts/issues/26

> [!NOTE]
> 安装完assdiff3后，还需将其设置为git的merge driver，详见仓库说明。

### 目录结构

对于每个单集的目录结构如下图所示：

```
epxx → 主目录
├── insert
│   ├── insert0x.ass
│   └── insert0x_tc.ass
├── screen
│   ├── screen.ass
│   └── screen_tc.ass
├── staff
│   ├── stf_kitauji.ass
│   └── stf_lolihouse.ass
├── epxx_sc.ass
└── epxx_tc.ass
```

> [!NOTE]  
> 由于现在由自动化流程自动生成繁体化文件，故_tc.ass已弃用。

`insert`下的文件应该仅包含插入曲部分，其它子文件也应各司其职。`epxx_sc.ass`为主文件，包含`import`语句。其它文件应使用 `Merge Scripts` 经由`import`语句导入到主文件中，最后导出发布文件。

### 修改字幕

应对每个分集下的各个子文件进行修改。在增删主文件对话行时，应注意保持特效栏文本为`kara`。

修改完成后，进行字幕文件的构建。

#### Github Actions构建

1. [Fork](https://github.com/Kitauji-Sub/subs-shikanoko/fork)本仓库
2. commit后提交到仓库
3. 在Actions选项卡下查看workflow run，在Artifacts中下载sino_subs_built

> [!NOTE]
> 如果在commit message中加入[PATCH]则会使版本号第三位增加，并把构建出的字幕文件发布到release。

#### 本地构建

1. 克隆本仓库到本地
2. 下载[Aegisub cli](https://github.com/scrpr/aegisub-cli/releases/download/disable_unique_path/aegisub-cli.zip)，解压到仓库根目录/aegisub-cli/下
3. 下载[字体](https://github.com/Kitauji-Sub/subs-shikanoko/releases/download/typeface/fonts.zip)，安装或使用FontLoader类工具临时加载
4. 安装依赖库
```
pip install --user git+https://github.com/FichteForks/Myaamori-Aegisub-Scripts.git@pr/fix-style-deduplication#subdirectory=scripts/sub-digest
pip install requests urllib3
```
5. 运行Python脚本
```
python build_scripts/build.py <path>/<to>/<work_dir>
```
6. 在`builds/output`下查看输出的字幕文件

## 声明

![site image](https://zhconvert.org/build/assets/images/logo_h36.1306fa53.png)

本仓库字幕在繁体中文化流程中，使用了繁化姬（[zhconvert.org](https://zhconvert.org/)）提供的 API 服务。

繁化姬API仅供个人学习研究使用，商业用途请参考[繁化姬说明文件](https://docs.zhconvert.org/commercial/)