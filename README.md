### ����
��ؽ��ܼ��ĵ���[��ؽ���](INSTRUCTION.md)
### ʹ�÷���
���Ľ���������£�
- *Step<1>* �ڹ����д���һ����Event:PlaceHolder

![img.png](img/step1.png)

- *Step<2>* ѡ���´�����Event����סShift�����������Ҽ�-->copy GUID(s) to clipboard
- *Step<3>* �ڿ�¡��������Ŀ���½�python�ļ����������ṩ�ĺ�����,�����м���
```python
from diffBnk import *
DiffBnk.diffErrBnk([������languageID],
                   [������platformID],
                   �������Event��GUID,
                   ������windowsBnk�ĵ�ַ,
                   ������androidBnk�ĵ�ַ,
                   ������boolֵ���Ƿ񱣴��¼Ϊtxt,Ĭ��ΪFalse��)
```
*ע�⣺languageID&platformID����ͨ�������ı��༭���򿪹����ļ���.wproj)��ȡ*
!["languageID&platformID��ȡ"](img/projInfo.png)

### ��������
#### diffSizeBnk
����Diff������ַ�����д��ڴ�С�����bnk������txt�ĵ�

ʹ��ʾ����
```python
DiffBnk.diffBnkSize(r"E:\WwiseProject\Project_IMIL\GeneratedSoundBanks\Windows",
                    r"E:\WwiseProject\Project_IMIL\GeneratedSoundBanks\Android")
```
#### diffSizeContent
����Diff����bnk�ļ�������������16�����ļ�(.hex)����ͨ������IDE�������ļ�����Diff�鿴

ʹ��ʾ����
```python
DiffBnk.diffBankContent(r'E:\WwiseProject\Project_IMIL\GeneratedSoundBanks\Android\zh-CN\ST_Vo__Atk04.bnk',
                        r'E:\WwiseProject\Project_IMIL\GeneratedSoundBanks\Windows\zh-CN\ST_Vo__Atk04.bnk')
```