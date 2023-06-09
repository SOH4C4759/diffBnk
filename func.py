import os
from typing import Union
from waapi import connect


def get_file_size(path):
    """
    获取文件大小，单位为KB
    """
    size = os.path.getsize(path) / 1024
    return round(size, 2)


def get_known_files(winBnkPath):
    """
    获取已知文件夹中的bnk文件名和大小
    """
    winBnks = {}
    for root, dirs, files in os.walk(winBnkPath):
        for file in files:
            if file.endswith('.bnk'):
                file_path = os.path.join(root, file)
                file_size = get_file_size(file_path)
                winBnks[file] = file_size
    return winBnks


def compare_files(winBnks, androidBnkPath):
    """
    与已知文件列表比较，返回同名文件的大小差异
    """
    l_diff = []
    for root, dirs, files in os.walk(androidBnkPath):
        for file in files:
            if file.endswith('.bnk') and file in winBnks:
                file_path = os.path.join(root, file)
                known_file_size = winBnks[file]
                file_size = get_file_size(file_path)
                diff = known_file_size - file_size
                if diff != 0:
                    l_diff.append((file, diff))
    return l_diff


def save_diff_list(file_path, diff_list):
    """
    将文件和大小差异的数据记录在一个txt文件中
    """
    with open(file_path, 'w') as f:
        for file, diff in diff_list:
            f.write(f"{file}: {diff} KB \n")


def optimized(args: Union[dict, object]):
    """用于优化参数为None时的json变量避免waapi调用错误"""
    return {k: v for k, v in args.items() if v is not None}


def get_file_size(path):
    """
    获取文件大小，单位为KB
    """
    size = os.path.getsize(path) / 1024
    return round(size, 2)


def setNotes(obj: str, value: str):
    """
    设置对象的备注
    :param obj: 所要重命名的对象的 ID (GUID)、名称或路径
    :param value: 对象的新名称
    """
    args = {
        "object": obj,
        "value": value
    }
    return connect(None).call("ak.wwise.core.object.setNotes", **args)


def generateBNK(soundbanks: list[dict[str, bool | any]], languages: list[str] = None, skipLanguages=False,
                platform: list[str] = None, rebuildSoundBanks=False,
                clearAudioFileCache=True, writeToDisk=True, rebuildInitBank=False):
    args = optimized({
        "soundbanks": soundbanks,
        "platforms": platform,
        "languages": languages,
        "skipLanguages": skipLanguages,
        "rebuildSoundBanks": rebuildSoundBanks,
        "clearAudioFileCache": clearAudioFileCache,
        "writeToDisk": writeToDisk,
        "rebuildInitBank": rebuildInitBank
    })
    return connect(None).call("ak.wwise.core.soundbank.generate", **args)


def setInclusions(_soundbank: str, objList: list[str], operation="add",
                  Filter=None):
    """
    修改声音库的收录列表。“操作”参数确定“包含”参数如何修改 SoundBank 的包含列表;“包含”可能会添加到 SoundBank 的包含列表中/从中删除/替换
    :param _soundbank: 要添加 Inclusion 的 SoundBank 的 ID (GUID)、名称或路径
    :param objList:要在 SoundBank 的 Inclusion 列表中添加/移除的对象的 ID (GUID)、名称或路径。
    :param operation:决定 'inclusions' 参数如何修改 SoundBank 的 Inclusion 列表
        可在SoundBank的Inclusion列表中添加/移除/替换inclusions'
    :param Filter：可用于筛选Inclusion的类型：events,structures,media
    :return:
    """
    if Filter is None:
        Filter = ["events", "structures", "media"]
    args = {
        "soundbank": _soundbank,
        "operation": operation,
        "inclusions": [{"object": _obj, "filter": Filter} for _obj in objList]
    }
    return connect(None).call("ak.wwise.core.soundbank.setInclusions", **args)