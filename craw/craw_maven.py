from util import  *
def search_cve(group: str, title: str ,version:str):
    #print("key:",keyword)
    session = get_proxy_session()
    print("url:")
    #url = 'https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-databind/2.10.2'
    url = 'https://mvnrepository.com/artifact/'+group+'/'+title+'/'+version
    # https: // mvnrepository.com / artifact / org.libreoffice / ridl
    print("https://mvnrepository.com/artifact/{}/{}/{}".format(group, title, version))
    #try:
    res = session.get(url)
    # except:
    #     print("err")
    #print("res:", res.text)
    return res
def craw_msg():
    # 先default 后has
    #df = pd.read_csv('pkg_shuf.csv')
    df = pd.read_csv('vuln_untagged_shuf.csv')
    write_csv(path='vuln_untagged_mvn1.csv', row=['name', 'version', 'software_id', 'License', 'Organization', 'HomePage', 'Date', 'Repositories', 'Used_by_artifacts', 'vuln_cves', 'Direct','Categories'])
    for index in range(0,df.shape[0]):
        print("index: ",index)
        lic, cat, org, hp, date = "", "", "", "", ""
        rep = []
        used = 0
        vul = []
        dir = []
        name = df.loc[index, 'name']
        #name = 'io.undertow:undertow-core'
        group, title = name.split(':')
        version = df.loc[index, 'version']
        # if df.loc[index,'vuln']==True:
        if True:
            DO = True
            TIME = 0
            while DO==True and TIME<10:
                try:
                    res = search_cve(group, title, version)
                    TIME = TIME +1
                    DO = False
                except:
                    print("err")
                    DO = True
            if TIME>=10:
                continue
            print("-----------find--------------")
            bs = BeautifulSoup(res.text, 'html.parser')
            table = bs.find(class_='grid')
            if table ==None:
                continue
            for tr in table.find_all('tr'):
                type = tr.next.text
                #print(type)
                if type == 'Vulnerabilities':
                    for tag in tr.find_all(class_='vuln'):
                        string = tag.string
                        if 'CVE' in string:     #
                            vul.append(string)
                            direct = True           # 是否直接漏洞
                            for ch in tag.previous_elements:  # 往前遍历 如果遇到dependency 就不是direct
                                if 'dependenc' in ch.text:
                                    direct = False
                                    break
                                if 'Direct' in ch.text:
                                    break
                            dir.append(direct)
                    #print(vul)
                    #print(dir)
                if type == 'License':
                    lic = tr.td.text
                    #print(lic)
                if type == 'Organization':
                    org = tr.td.text
                    #print(org)
                if type == 'HomePage':
                    hp = tr.td.text
                    #print(hp)
                if type == 'Date':
                    date = tr.td.text
                    #print(date)
                if type ==  'Repositories':
                    for re in tr.find_all(class_="b lic"):
                        rep.append(re.text)
                    #print(rep)
                if type == 'Used By':
                    art = tr.a.text.replace(' artifacts','').replace(',','')
                    used = int(art)
                    #print(used)
                if type == 'Categories':
                    cat = tr.td.text
            #print()
        write_csv(path='vuln_untagged_mvn1.csv', row=[name,version,df.loc[index,'software_id'],lic,org,hp,date,rep,used,vul,dir,cat])

if __name__ == '__main__':
    craw_msg()