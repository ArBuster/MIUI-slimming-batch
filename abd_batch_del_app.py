import subprocess
import re
import unicodedata

device_model = {
    # ro.product.model
    "23054RA19C": {
        "path": "23054RA19C",
        # ro.system.build.version.incremental
        "rom_version": {
            # rom_version: package_path
            "V14.0.10.0.TLHCNXM": "V14.0.10.0.TLHCNXM"
        }
    }
}


def normalize_cmd_output(cmd_output:str) -> str:
    return unicodedata.normalize("NFKC", cmd_output)


def adb_get_device_info() -> str:
    cmd = R"adb shell getprop"
    ps_ret = subprocess.run(
        cmd.split(' '), stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, encoding="utf8")
    print("执行命令: %s, 返回值: %d" % (cmd , ps_ret.returncode))
    packages_path = None
    if ps_ret.returncode == 0:
        cmd_output = normalize_cmd_output(ps_ret.stdout).lower()
        match = re.search(R"\[ro.product.model\]:\s*\[([\d\w]+)\]", cmd_output)
        if match:
            model = match.group(1).upper()
            if model in device_model:
                match = re.search(R"\[ro.system.build.version.incremental\]:\s*\[([\d\w\.]+)\]", cmd_output)
                if match:
                    rom_version = match.group(1).upper()
                    if rom_version in device_model[model]["rom_version"]:
                        packages_path = "./trim/" + device_model[model]["path"] + "/" + device_model[model]["rom_version"][rom_version] + "/"
                        print("设备型号: %s\nrom 版本: %s\n" % (model, rom_version))
                    else:
                        print("此设备的rom版本缺少要裁减的软件包列表. rom版本: %s" % rom_version)
            else:
                print("此设备型号缺少要裁减的软件包列表. 型号: %s" % model)
    else:
        print(ps_ret.stdout)

    return packages_path


def load_package_list(package_path:str) -> tuple:
    disable_apps, uninstall_apps = tuple(), tuple()
    with open(package_path + "disable", "r") as f:
        disable_apps = tuple(line[:-1].lower() for line in f.readlines() if line[:-1])

    with open(package_path + "uninstall", "r") as f:
        uninstall_apps = tuple(line[:-1].lower() for line in f.readlines() if line[:-1])

    return disable_apps, uninstall_apps


def adb_list_users() -> tuple:
    cmd = R"adb shell pm list users"
    ps_ret = subprocess.run(
        cmd.split(' '), stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, encoding="utf8")
    print("执行命令: %s, 返回值: %d" % (cmd , ps_ret.returncode))
    print(ps_ret.stdout)

    user_ids = list()
    if ps_ret.returncode == 0:
        cmd_out = normalize_cmd_output(ps_ret.stdout)
        for line in cmd_out.split('\n'):
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
        package_list = normalize_cmd_output(ps_ret.stdout).lower().split('\n')
        for i in range(0, len(package_list)):
            package_list[i] = package_list[i][8:]
    else:
        package_list = list()

    print("user %s 已安装的包共 %d 个\n" % (user_id, len(package_list)))
    return tuple(package_list)


def adb_disable_package(user_id:str, installed_apps:tuple[str], disable_apps:tuple[str]):
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


def adb_uninstall_package(user_id:str, installed_apps:tuple[str], uninstall_apps:tuple[str]):
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
    package_path = adb_get_device_info()
    if package_path:
        disable_apps, uninstall_apps = load_package_list(package_path)
        user_ids = adb_list_users()
        if user_ids:
            id = input("请输入要操作的user id: ")
            print('\n')
            if id in user_ids:
                installed_apps = adb_list_packages(id)
                print("正在执行user id: %s 的adb批处理操作\n" % id)
                adb_disable_package(id, installed_apps, disable_apps)
                adb_uninstall_package(id, installed_apps, uninstall_apps)
            else:
                print("不存在user id: %s\n" % id)

    print("\nadb批处理操作执行结束\n")
