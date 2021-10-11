"""
@File    :   resc.py
@Author  :   UjhhgtgTeams
@Version :   1.0
@Contact :   feyxiexzf@gmail.com
@License :   (C)Copyright 2020-2021, UjhhgtgTeams
@Desc    :   The resources for the sudoku solver.
"""

from locale import getdefaultlocale

# Debug Options
# Only for debugging or packaging
forceLocales = True  # Available Options: True, False
# END


localesFull = {
    "zh": {
        "btnRunName": "开始计算!",
        "btnFastModeName": "执行极速计算!",
        "calcText": "正在计算中......",
        "fastModeText": "正在后台计算中......",
        "invalidItemsText": "检测到错误的输入! 请检查并重试!",
        "calcEndText": "计算完成!"
    },
    "en": {
        "btnRunName": "SHOW",
        "btnFastModeName": "FAST",
        "calcText": "Calculating......",
        "fastModeText": "Calculating in the background......",
        "invalidItemsText": "Invalid item(s) appeared. Please check and retry.",
        "calcEndText": "Finished!"
    }
}
if forceLocales:
    locales = localesFull["en"]
else:
    if getdefaultlocale()[0][:2] != "zh" and getdefaultlocale()[0][:2] != "en":
        locales = localesFull["en"]
    else:
        locales = localesFull[getdefaultlocale()[0][:2]]
sudoku = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]
