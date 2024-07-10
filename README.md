# 鹿乃子乃子乃子虎视眈眈 字幕仓库

该仓库存放以`北宇治字幕组`名义制作的TV动画《鹿乃子乃子乃子虎视眈眈》 字幕。

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

### 手动合并

1. 克隆本仓库到本地
2. 使用[zhconvert.org](zhconvert.org)将**每个文件**均进行繁化。对于主文件，还需更改import语句中的文件名。将繁化后的文件命名为`*_tc.ass`
3. 修改对应样式为繁体样式，对应样式可以在_tc.ass的主文件中找到
4. 使用`The0x539's templater`将模板应用到`insert`文件夹中的文件并保存，注意该脚本与aegisub自带的auto4模板运行器不完全兼容
5. 依次打开各个主文件，使用`Merge Scripts`的`Import all external files`导入子文件；`Generate release candidate`生成发布文件

## 声明

![site image](https://zhconvert.org/build/assets/images/logo_h36.1306fa53.png)

本仓库字幕在繁体中文化流程中，使用了繁化姬（[zhconvert.org](https://zhconvert.org/)）提供的 API 服务。

繁化姬API仅供个人学习研究使用，商业用途请参考[繁化姬说明文件](https://docs.zhconvert.org/commercial/)