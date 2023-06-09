import os
from typing import Union
from waapi import connect


def get_file_size(path):
    """
    ��ȡ�ļ���С����λΪKB
    """
    size = os.path.getsize(path) / 1024
    return round(size, 2)


def get_known_files(winBnkPath):
    """
    ��ȡ��֪�ļ����е�bnk�ļ����ʹ�С
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
    ����֪�ļ��б�Ƚϣ�����ͬ���ļ��Ĵ�С����
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
    ���ļ��ʹ�С��������ݼ�¼��һ��txt�ļ���
    """
    with open(file_path, 'w') as f:
        for file, diff in diff_list:
            f.write(f"{file}: {diff} KB \n")


def optimized(args: Union[dict, object]):
    """�����Ż�����ΪNoneʱ��json��������waapi���ô���"""
    return {k: v for k, v in args.items() if v is not None}


def get_file_size(path):
    """
    ��ȡ�ļ���С����λΪKB
    """
    size = os.path.getsize(path) / 1024
    return round(size, 2)


def setNotes(obj: str, value: str):
    """
    ���ö���ı�ע
    :param obj: ��Ҫ�������Ķ���� ID (GUID)�����ƻ�·��
    :param value: �����������
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
    �޸����������¼�б�������������ȷ������������������޸� SoundBank �İ����б�;�����������ܻ���ӵ� SoundBank �İ����б���/����ɾ��/�滻
    :param _soundbank: Ҫ��� Inclusion �� SoundBank �� ID (GUID)�����ƻ�·��
    :param objList:Ҫ�� SoundBank �� Inclusion �б������/�Ƴ��Ķ���� ID (GUID)�����ƻ�·����
    :param operation:���� 'inclusions' ��������޸� SoundBank �� Inclusion �б�
        ����SoundBank��Inclusion�б������/�Ƴ�/�滻inclusions'
    :param Filter��������ɸѡInclusion�����ͣ�events,structures,media
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