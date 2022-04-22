# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random

import pandas as pd
def random_lst():
    df = pd.read_csv('./data/vuln_untagged.csv')
    software_index = dict()
    for i in range(df.shape[0]):
        name = df.loc[i,'name']
        if name not in software_index:
            software_index[name]=[]
        software_index[name].append(i)
    sum = 0
    df_lst = []
    for name in software_index:
        num = int(len(software_index[name])/df.shape[0]*(df.shape[0]*0.1))
        if num == 0:
            num = 1
        sum = sum+num
        software_index[name]=random.sample(software_index[name],num)
        df_lst = df_lst+software_index[name]
    print(software_index)
    df_shuf = df.drop([i for i in range(df.shape[0]) if i not in df_lst])
    df_shuf.reset_index(drop=True, inplace=True)
    df_shuf.to_csv('./data/vuln_untagged_shuf.csv')

def get_df_msg(df2,index):
    cve = df2.loc[index, 'cve']
    date = df2.loc[index, 'date']
    score = df2.loc[index, 'score']
    rating = df2.loc[index, 'rating']
    cvss = df2.loc[index, 'cvss']
    cwe = df2.loc[index, 'cwe']
    return cve,date,score,rating,cvss,cwe

def print_hi(name):
    df = pd.read_csv('./data/VerCve.csv')
    df['vuln_cves'] = df['vuln_cves'].fillna(0)
    df = df.drop([index for index in range(df.shape[0]) if df.loc[index,'vuln_cves']==0])
    df.reset_index(drop=True,inplace=True)
    cves = str(df['vuln_cves']).split()
    dirs = str(df['Direct']).split()
    df2 = pd.read_csv('./data/cve-cwe1.csv')
    Tcwe = []
    print("untagged&vuln: \n395个软件的869个开源依赖的2915个版本")
    print("558种cve")
    cvemsg = dict()
    Timesta = dict()
    CWE = dict()

    for index in range(df2.shape[0]):
        cve, date, score, rating, cvss, cwe = get_df_msg(df2,index)
        Tcwe.append(cwe)
        cvemsg[cve]=(cve,date,score,rating,cvss,cwe)
        # Time statistics
        if date not in Timesta:
            Timesta[date]=1
        else:
            Timesta[date] = Timesta[date]+1
        if cwe not in CWE:
            CWE[cwe]=1
        else:
            CWE[cwe] = CWE[cwe]+1
    CWE = sorted(CWE.items(), key=lambda x: -x[1])
    CWE_X = [c[0] for c in CWE]
    CWE_Y = [c[1] for c in CWE]
    Tcwe = list(set(Tcwe))
    print("{}种CWE".format(len(Tcwe)))
    Time_X = []
    Time_Y = []
    for d in Timesta:
        Time_X.append(d)
        Time_Y.append(Timesta[d])

    print(df)
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')
    random_lst()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
