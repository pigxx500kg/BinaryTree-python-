import prettytable as pt


def getDataList(fileName):
    dataFile = open(fileName, 'r')  # 打开文件
    dataList = []
    for line in dataFile:
        # 原表格中有空行,所以剔除
        if line.strip().split(',') == ['', '', '', '', '', '', '']:
            pass
        else:
            dataList.append(line.strip().split(','))
    return dataList


def getMonthlyAverages(dataList):
    """
   使用Date，Volume, Adj，Close计算每月平均价格。下面是一个计算月平均价格的公式，其中Vi代表Volume，Ci是当天调整收盘价（Adj
    Close）。
    averagePrice = (V1 * C1 + V2 * C2 + …….+ Vn * Cn) / (V1 + V2 + ……+ Vn)
    为每个月创建包含两个项的元组，包括该月的平均价格和日期（只需要年份和月份）。
    将每个月的元组添加到列表中（例如monthlyAveragesList），计算所有月的平均值后，返回此列表。
    在这里使用元组，是因为这些值计算出来后不想意外的更改它们！
    """
    dateList = []
    monthlyAveragesList = []
    for i in range(1, len(dataList)):  # 从数据的第二行开始抽出其日期
        date = dataList[i][0].split('/')  # ['2013', '1', '2']
        if len(date[1]) == 1:
            dateList.append(date[0] + '0' + date[1])  # 年月的组合 例如201301 201312
        else:
            dateList.append(date[0] + date[1])
    lastDate = dateList[0]  # 第一个日期
    priceSum = 0
    volumeSum = 0
    for i in range(0, len(dateList) - 1):
        currentDate = dateList[i]
        if currentDate == lastDate:
            priceSum += float(dataList[i + 1][5]) * float(dataList[i + 1][6])  # （调整后的价格 * 成交量）的总和
            volumeSum += float(dataList[i + 1][6])  # 成交量总和
        else:
            monthlyAveragesList.append((priceSum / volumeSum, lastDate))
            lastDate = currentDate
            priceSum = float(dataList[i + 1][5])
            volumeSum = float(dataList[i + 1][6])
    return monthlyAveragesList  # 元组列表，其中一项如(364.77004620107874, '201301')


def printInfo(monthlyAverageList):
    """
    使用getMonthlyAverages函数得到月平均价格列表
    需要查找和显示Google股价中6个最好（最高平均价格）和6个最坏（最低平均价格）的月份。
    按从高到低的顺序显示，要求精确到小数点后2位。对输出进行格式化，得到美观的输出（包括信息标题栏）。
    此函数不返回任何值。
    """
    seqTable = pt.PrettyTable(["Date", "Monthly Average Price"])  # 从小到大
    revTable = pt.PrettyTable(["Date", "Monthly Average Price"])  # 从大到小
    monthlyAverageList.sort()
    for i in range(6):
        # 如果使用round函数则不能把只有一位小数的股价变成两位 如1053.3 ->1053.3
        seqTable.add_row(
            [monthlyAverageList[i][1][0:4] + '-' + monthlyAverageList[i][1][4:6], "%.2f" % monthlyAverageList[i][0]])
    monthlyAverageList.reverse()
    for i in range(6):
        revTable.add_row(
            [monthlyAverageList[i][1][0:4] + '-' + monthlyAverageList[i][1][4:6], "%.2f" % monthlyAverageList[i][0]])
    print("The lowest six months of Google's stock price：\n\n{}\n\n".format(seqTable))
    print("The highest six months of Google's stock price：\n\n{}".format(revTable))


if __name__ == '__main__':
    fileLocation = "C:/Users/Administrator/Desktop/table.csv"  # 绝对路径
    dataList = getDataList(fileLocation)
    monthlyAverageList = getMonthlyAverages(dataList)
    printInfo(monthlyAverageList)
