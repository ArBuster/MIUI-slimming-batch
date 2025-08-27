注意：  
•卸载系统组件有可能造成系统崩溃/无法正常开机进入系统卓面，操作之前先备份数据，出问题了进recovery模式恢复出厂设置。
•不同系统版本可卸载/停用的包不一样，不可通用。
•以下包通过红米note12T pro miui14测试。

参考：
https://zhuanlan.zhihu.com/p/648185138
https://www.bilibili.com/opus/898292534556491811
https://www.cnblogs.com/ray365/p/18690901
https://gist.github.com/mcxiaoke/ade05718f590bcd574b807c4706a00b1
https://gist.github.com/mcxiaoke/0a4c639d04e94c45eb6c787c0f98940a
https://archive.ph/R3T2S


常用命令：
检测设备连接：adb devices
列出用户：adb shell pm list users
列出用户的包名：adb shell pm list packages --user [user id]  (使用-f列出包路径，-d列出被禁用的包，-e列出启用的包)
停用用户的应用命令：adb shell pm disable-user --user [user id] [包名]
启用用户的应用命令：adb shell pm enable --user [user id] [包名]
卸载用户的应用命令：adb uninstall --user [user id] [包名]
恢复用户的已卸载系统应用：adb shell cmd package install-existing --user [user id] [包名]


可代替的软件包：
搜狗输入法小米版（用gboard代替）：com.sohu.inputmethod.sogou.xiaomi
使用谷歌play的mi player（com.miui.player）代替预装的QQ音乐。


停用的系统包（可能偶尔需要使用的）：
录音机：com.android.soundrecorder
指南针：com.miui.compass


部分包其它机型其它系统卸载后可能存在问题：
miui安全组件（内置腾讯天御库，会上传应用列表）：com.miui.guardprovider
系统服务组件（儿童空间，游戏加速）：com.miui.securityadd


卸载的系统包（可能有恶劣行为的）：
自带浏览器（广告，用firefox代替）：com.android.browser
快应用服务框架（广告）：com.miui.hybrid
小米广告分析：com.miui.analytics
智能服务（系统广告推送，自带应用管理器找不到）：com.miui.systemAdSolution
录音助手（通话录音）：com.miui.audiomonitor
云控：com.xiaomi.joyose
小爱同学：com.miui.voiceassist
小爱同学关联包：com.miui.voiceassistoverlay
小爱翻译：com.xiaomi.aiasst.vision
小爱建议：com.xiaomi.aireco
小爱通话：com.xiaomi.aiasst.service
语音唤醒：com.miui.voicetrigger
小米无障碍（小米闻声）：com.miui.accessibility
小米安全键盘：com.miui.securityinputmethod
小米云服务sdk：com.xiaomi.micloud.sdk
小米云备份：com.miui.cloudbackup
小米云服务：com.miui.cloudservice
MICloudSync（云同步）：com.miui.micloudsync
通话录音机（mtk平台）：com.mediatek.callrecorder
语音控制（mtk平台）：com.mediatek.voicecommand
（语音解锁，mtk平台）：com.mediatek.voiceunlock
百度输入法小米版：com.baidu.input_mi


没用的东西：
米币支付：com.xiaomi.payment
mi ai引擎：com.xiaomi.aicr
传送门：com.miui.contentextension
生活黄页：com.miui.yellowpage
CarWith：com.miui.carlink
智能助理（负一屏）：com.miui.personalassistant
主题商店：com.miui.themestore
小米视频：com.miui.video
小米商城：com.xiaomi.shop
游戏中心：com.xiaomi.gamecenter
游戏加速：com.miui.vpnsdkmanager
游戏服务：com.xiaomi.gamecenter.sdk.service
游戏高能时刻：com.xiaomi.migameservice
自动连招：com.xiaomi.macro
米家：com.xiaomi.smarthome
计算器：com.miui.calculator
屏幕录制：com.miui.screenrecorder
内容中心：com.miui.newhome
小米互联通信服务：com.xiaomi.mi_connect_service
MIUI+ Beta（跨屏协调服务）：com.xiaomi.mirror
小米SIM卡激活服务：com.xiaomi.simactivate.service
维修模式：com.miui.maintenancemode
常用语：com.miui.phrase
（miui定制金山词霸翻译）：com.miui.translation.kingsoft
（小米云翻译服务）：com.miui.translation.xmcloud
（miui翻译服务）：com.miui.translationservice
全球上网：com.miui.virtualsim
MConnService（MIUI虚拟SIM服务）：com.miui.vsimcore
WMService（MIUI无线管理服务）：com.miui.wmsvc
textaction（MIUI编辑器，用于编辑图片或视频）：com.miuix.editor
SystemHelper：com.mobiletools.systemhelper
家人守护：com.miui.greenguard
搜索：com.android.quicksearchbox
急救信息：com.android.emergency
小米画报：com.mfashiongallery.emag
小米文档查看强（wps，用NMM代替）：cn.wps.moffice_eng.xiaomi.lite
银联可信服务安全组件：com.unionpay.tsmservice.mi
Android无障碍套件：com.google.android.marvin.talkback
SoterService（腾讯指纹认证服务）：com.tencent.soter.soterserver
喜马拉雅：com.ximalaya.ting.android
多看：com.duokan.reader
