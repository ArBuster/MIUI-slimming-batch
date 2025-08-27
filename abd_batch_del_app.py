import subprocess
import re

disable_apps = ("com.android.soundrecorder", "com.miui.compass")
uninstall_apps = ("com.miui.guardprovider", "com.miui.securityadd", "com.android.browser",
                  "com.miui.hybrid", "com.miui.analytics", "com.miui.systemAdSolution",
                  "com.miui.audiomonitor", "com.xiaomi.joyose", "com.miui.voiceassist",
                  "com.miui.voiceassistoverlay", "com.xiaomi.aiasst.vision", "com.xiaomi.aireco",
                  "com.xiaomi.aiasst.service", "com.miui.voicetrigger", "com.miui.accessibility",
                  "com.miui.securityinputmethod", "com.xiaomi.micloud.sdk", "com.miui.cloudbackup",
                  "com.miui.cloudservice", "com.miui.micloudsync", "com.mediatek.callrecorder",
                  "com.mediatek.voicecommand", "com.mediatek.voiceunlock", "com.baidu.input_mi",
                  "com.xiaomi.payment", "com.xiaomi.aicr", "com.miui.contentextension",
                  "com.miui.yellowpage", "com.miui.carlink", "com.miui.personalassistant",
                  "com.miui.themestore", "com.miui.video", "com.xiaomi.shop",
                  "com.xiaomi.gamecenter", "com.miui.vpnsdkmanager", "com.xiaomi.gamecenter.sdk.service",
                  "com.xiaomi.migameservice", "com.xiaomi.macro", "com.xiaomi.smarthome",
                  "com.miui.newhome", "com.xiaomi.mi_connect_service", "com.xiaomi.mirror",
                  "com.xiaomi.simactivate.service", "com.miui.maintenancemode", "com.miui.phrase",
                  "com.miui.translation.kingsoft", "com.miui.translation.xmcloud", "com.miui.translationservice",
                  "com.miui.virtualsim", "com.miui.vsimcore", "com.miui.wmsvc", "com.miuix.editor",
                  "com.mobiletools.systemhelper", "com.miui.greenguard", "com.android.quicksearchbox",
                  "com.android.emergency", "com.mfashiongallery.emag", "cn.wps.moffice_eng.xiaomi.lite",
                  "com.unionpay.tsmservice.mi", "com.google.android.marvin.talkback", "com.tencent.soter.soterserver",
                  "com.ximalaya.ting.android", "com.duokan.reader", "com.miui.calculator",
                  "com.miui.screenrecorder")

def adb_list_users() -> tuple:
    cmd = R"adb shell pm list users"
    ps_ret = subprocess.run(
        cmd.split(' '), stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, encoding="utf8")
    print("执行命令: %s, 返回值: %d" % (cmd , ps_ret.returncode))
    print(ps_ret.stdout)

    user_ids = list()
    if ps_ret.returncode == 0:
        for line in ps_ret.stdout.split('\n'):
            match = re.search(R"UserInfo{(\d+):", line)
            if match:
                user_ids.append(match.group(1))

    return tuple(user_ids)


def adb_list_packages(user_id:str) -> tuple:
    cmd = R"adb shell pm list packages --user %s" % user_id
    ps_ret = subprocess.run(
        cmd.split(' '), stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, encoding="utf8")
    print("执行命令: %s, 返回值: %d" % (cmd , ps_ret.returncode))

    if ps_ret.stdout:
        package_list = ps_ret.stdout.split('\n')
        for i in range(0, len(package_list)):
            package_list[i] = package_list[i][8:]
    else:
        package_list = list()

    print("user %s 已安装的包共 %d 个\n" % (user_id, len(package_list)))
    return tuple(package_list)


def adb_disable_package(user_id:str, installed_apps:tuple[str]):
    print("正在执行adb disable-user --user %s 操作\n" % user_id)
    apps_not_installed = list()
    success, failed = 0, 0
    for app in disable_apps:
        if app not in installed_apps:
            apps_not_installed.append(app)
            continue
        cmd = R"adb shell pm disable-user --user %s %s" % (user_id, app)
        ps_ret = subprocess.run(
            cmd.split(' '), stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, encoding="utf8")
        if ps_ret.returncode == 0:
            success+=1
        else:
            failed+=1
            print("error 执行命令: %s, 返回值: %d" % (cmd, ps_ret.returncode))
            print(ps_ret.stdout)

    print("停用 %d 个软件包, 成功: %d, 失败: %d, 有 %d 个软件包未安装:" %
          (len(disable_apps), success, failed, len(apps_not_installed)))
    for app in apps_not_installed:
        print(app)
    print('\n')


def adb_uninstall_package(user_id:str, installed_apps:tuple[str]):
    print("正在执行adb uninstall --user %s 操作\n" % user_id)
    apps_not_installed = list()
    success, failed = 0, 0
    for app in uninstall_apps:
        if app not in installed_apps:
            apps_not_installed.append(app)
            continue
        cmd = R"adb uninstall --user %s %s" % (user_id, app)
        ps_ret = subprocess.run(
            cmd.split(' '), stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, encoding="utf8")

        if ps_ret.returncode == 0:
            success+=1
        else:
            failed+=1
            print("error 执行命令: %s, 返回值: %d" % (cmd, ps_ret.returncode))
            print(ps_ret.stdout)

    print("卸载 %d 个软件包, 成功: %d, 失败: %d, 有 %d 个软件包未安装:" %
          (len(uninstall_apps), success, failed, len(apps_not_installed)))
    for app in apps_not_installed:
        print(app)


if __name__ == "__main__":
    user_ids = adb_list_users()
    if user_ids:
        id = input("请输入要操作的user id: ")
        if id in user_ids:
            installed_apps = adb_list_packages(id)
            print("正在执行user id: %s 的adb批处理操作\n" % id)
            adb_disable_package(id, installed_apps)
            adb_uninstall_package(id, installed_apps)
        else:
            print("不存在user id: %s\n" % id)

    print("\nadb批处理操作执行结束\n")
