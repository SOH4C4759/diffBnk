# -*- coding: utf-8 -*-
from func import *
import binascii


class DiffBnk:
    @staticmethod
    def diffBnkSize(winBnkPath, androidBnkPath):
        """
        :param winBnkPath:更改为Windows Bnks的地址,例如：  r"E:\WwiseProject\Project_IMIL\GeneratedSoundBanks\Android"
        :param androidBnkPath:更改为Android Bnks的地址,例如： r"E:\WwiseProject\Project_IMIL\GeneratedSoundBanks\Android"
        """

        winBnks = get_known_files(winBnkPath)
        diff_list = compare_files(winBnks, androidBnkPath)

        file_path = r"diffSize.txt"
        save_diff_list(file_path, diff_list)
        print("差异数据数据已保存到文件中。")

    @staticmethod
    def diffBankContent(bnkA, bnkB):
        """
        :param bnkA:设置BNK_A的地址，例如：bnkA = r'E:\WwiseProject\Project_IMIL\GeneratedSoundBanks\Android\zh-CN\ST_Vo__Atk04.bnk'
        :param bnkB:设置BNK_B的地址，例如：bnkB = r'E:\WwiseProject\Project_IMIL\GeneratedSoundBanks\Windows\zh-CN\ST_Vo__Atk04.bnk'
        """

        with open(bnkA, 'rb') as f:
            hex_data = binascii.hexlify(f.read()).decode('utf-8')

        with open('bnkA.hex', 'w') as f:
            for i in range(0, len(hex_data), 2):
                f.write(hex_data[i:i + 2] + ' ')

        with open(bnkB, 'rb') as f:
            hex_data = binascii.hexlify(f.read()).decode('utf-8')

        with open('bnkB.hex', 'w') as f:
            for i in range(0, len(hex_data), 2):
                f.write(hex_data[i:i + 2] + ' ')

        print("Bnk 16进制文件已生成，可使用任意IDE的Diff功能查看差异")

    @staticmethod
    def diffErrBnk(language_IDs: list[str], platform_IDs: list[str], placeHolder_IDs: str, winBnkPath: str,
                   androidBnkPath: str, bSaveAsTxt=False):
        """
        :param language_IDs:Wwise工程中language的ID列表
        :param platform_IDs:Wwise工程中各平台的ID列表
        :param placeHolder_IDs:Wwise工程中占位空Event的ID
        :param winBnkPath:更改为Windows Bnks的地址,例如：  r"E:\WwiseProject\Project_IMIL\GeneratedSoundBanks\Android"
        :param androidBnkPath:更改为Android Bnks的地址,例如： r"E:\WwiseProject\Project_IMIL\GeneratedSoundBanks\Android"
        :param bSaveAsTxt:是否将处理信息记录为文档
        """
        global f
        winBnks = {}
        for root, dirs, files in os.walk(winBnkPath):
            for file in files:
                if file.endswith('.bnk'):
                    file_path = os.path.join(root, file)
                    file_size = get_file_size(file_path)
                    winBnks[file] = file_size

        if bSaveAsTxt:
            f = open('diff.txt', 'w')

        errBnk = []
        note = "bnk生成异常,自动化修复并重新生成 by:Sora"  # 可以自行更改备注

        for root, dirs, files in os.walk(androidBnkPath):
            for file in files:
                if file.endswith('.bnk') and file in winBnks:
                    winBnkSize = winBnks[file]

                    file_path = os.path.join(root, file)
                    androidBnkSize = get_file_size(file_path)

                    diff = winBnkSize - androidBnkSize
                    if diff != 0:
                        file = file.split(".")[0]
                        args = {"waql": f"from type SoundBank where name = \"{file}\""}
                        result = connect(None).call("ak.wwise.core.object.get", **args)['return']

                        if bSaveAsTxt:
                            f.write(file + "   " + diff.__str__() + "\n")

                        if result != []:
                            print(result[0])
                            errBnk.append(result[0])
                            setNotes(result[0]['id'], note)
                            setInclusions(result[0]['id'], [placeHolder_IDs])

        connect(None).call("ak.wwise.core.project.save")

        bnk_names = [{"name": bnk['name'], "rebuild": True} for bnk in errBnk]

        if generateBNK(bnk_names, language_IDs, False, platform_IDs, True, True, True, True):
            print("Wwise工程Bnks生成完毕，请Reconcile GeneratedSoundBanks地址，将修改内容添加至版本管理")


