def auto_egp():

    from urllib.request import urlopen
    import xml.etree.ElementTree as ET
    import os
    import pandas as pd
    from datetime import datetime

    today = datetime.now().strftime('%d%m%Y')
    tomonth = datetime.now().strftime('%B')
    toyear = datetime.now().strftime('%Y')
    today_d = datetime.now().strftime('%d')
    tomonth_m = datetime.now().strftime('%m')

    path_location = 'EGP/' + toyear + '/' + tomonth

    file_csv = path_location + '/' + today + '.csv'

    url = 'http://process3.gprocurement.go.th/EPROCRssFeedWeb/egpannouncerss.xml'
    parameter_deptId = '?deptId='
    parameter_anounceType = '&anounceType='


    deptId_txt = open('deptid.txt', 'r')
    anounceType_txt = open('anouncetype.txt', 'r')

    deptId_ = []
    anounceType_ = []

    for deptId in deptId_txt:
        deptId_.append(deptId)
    for anounceType in anounceType_txt:
        anounceType_.append(anounceType)

    if os.path.isdir(path_location) == False:
        os.makedirs(path_location)

    list_test = {}

    for deptId in deptId_:
        for anounceType in anounceType_:
            url_str = url + parameter_deptId + deptId + parameter_anounceType + anounceType
            url_str = url_str.replace('\n', '')

            url_open = urlopen(url_str)

            root = ET.parse(url_open).getroot()

            # get title
            for rss in root:
                for channel in rss:
                    if channel.tag == 'item':
                        # print(channel.tag)
                        for item in channel:
                            if item.tag == 'description' or item.tag == 'guid':
                                pass
                            else:
                                list_test.update({
                                    item.tag: []
                                })
                        list_test.update({
                            'deptID': [],
                            'pubT': [],
                            'pubD': [],
                            'pubM': [],
                            'pubY': []
                        })

            # get data
            for rss in root:
                for channel in rss:
                    if channel.tag == 'item':
                        # print(channel.tag)
                        for item in channel:
                            # print(item.tag)
                            if item.tag == 'description' or item.tag == 'guid':
                                pass
                            else:
                                # print(item.text)
                                list_test[item.tag].append(item.text)
                        deptId_str = deptId
                        deptId_str = deptId_str.replace('\n', '')
                        list_test['deptID'].append(deptId_str)
                        anounceType_str = anounceType
                        anounceType_str = anounceType_str.replace('\n', '')
                        #print(anounceType_str)
                        if anounceType_str == 'W0':
                            list_test['pubT'].append(1)
                        elif anounceType_str == 'D1':
                            list_test['pubT'].append(2)
                        elif anounceType_str == 'P0':
                            list_test['pubT'].append(3)
                        elif anounceType_str == '15':
                            list_test['pubT'].append(4)
                        elif anounceType_str == 'D0':
                            list_test['pubT'].append(5)
                        elif anounceType_str == 'W1':
                            list_test['pubT'].append(6)
                        elif anounceType_str == 'D2':
                            list_test['pubT'].append(7)
                        elif anounceType_str == 'W2':
                            list_test['pubT'].append(8)
                        else:       # B0
                            list_test['pubT'].append(9)
                        list_test['pubD'].append(today_d)
                        list_test['pubM'].append(tomonth_m)
                        list_test['pubY'].append(toyear)

            # print(list_test)

            if list_test != {}:

                df = pd.DataFrame(list_test)

                # .csv ภาษาไทย เอ่อออ

                if os.path.isfile(file_csv) == True:
                    df.to_csv(file_csv, index=False, mode='a', header=False)
                else:
                    df.to_csv(file_csv, index=False)



def data_duplicate():

    import pandas as pd
    from datetime import datetime
    import os

    today = datetime.now().strftime('%d%m%Y')
    tomonth = datetime.now().strftime('%B')
    toyear = datetime.now().strftime('%Y')

    path_location = 'EGP/' + toyear+ '/' + tomonth

    file_csv = path_location + '/' + today + '.csv'

    # ตัดข้อมูลซ้ำ
    if os.path.isfile(file_csv) == True:
        df = pd.read_csv(file_csv)
        df.drop_duplicates(inplace=True)
        # print(df)
        df.to_csv(file_csv, index=False)
    else:
        print('No Directory')



def upload_mariadb():

    import mysql.connector
    import pandas as pd
    from datetime import datetime
    import os

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='',
        port='3306'
    )

    today = datetime.now().strftime('%d%m%Y')
    tomonth = datetime.now().strftime('%B')
    toyear = datetime.now().strftime('%Y')

    path_location = 'EGP/' + toyear + '/' + tomonth

    file_csv = path_location + '/' + today + '.csv'

    if os.path.isfile(file_csv) == True:
        df = pd.read_csv(file_csv)
        # print(df)


        def loopcheck(link_):
            sql = "SELECT * FROM `egp` WHERE link='" + link_ + "'"
            cursor = conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            return data

        # print(loopcheck("http://process3.gprocurement.go.th/egp2procmainWeb/jsp/procsearch.sch?servlet=gojsp&proc_id=ShowHTMLFile&processFlows=Procure&projectId=65087489973&templateType=W2&temp_Announ=A&temp_itemNo=0&seqNo=1"))

        for i in range(len(df['link'])):
            # print(loopcheck(i))
            if loopcheck(df['link'][i]) == []:
                # print("INSERT")
                # print(df['link'][i])
                sql = "INSERT INTO `egp`(`title`, `link`, `pubDate`, `numID`, `pubT`, `pubD`, `pubM`, `pubY`) VALUES ('" + str(df['title'][i]) + "','" + str(df['link'][i]) + "','" + str(df['pubDate'][i]) + "','" + str(df['numID'][i]) + "','" + str(df['pubT'][i]) + "','" + str(df['pubD'][i]) + "','" + str(df['pubM'][i]) + "','" + str(df['pubY'][i]) + "')"
                # print(sql)
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
                cursor.close()
            # else:
            #     print("NOT INSERT")
    else:
        print('No Directory')

    conn.close()





print("""

            AutoEGP By Avatart0Dev :)
    
""")

auto_egp()
data_duplicate()
upload_mariadb()    # Database MariaDB
