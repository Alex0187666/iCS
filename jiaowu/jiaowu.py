'''
Function:
    Sicau教务抢课
Author:
    XWhite
GitHub项目地址:
    https://github.com/Upsetin/iCS
更新日期:
    2021-01-10
'''



import requests, re, getpass, csv, os

from lxml import etree



class Sicau():

    def __init__(self):
        global isLogin
        self.Requests = requests.session()
        '''首次运行创建文件'''
        try:
            with open('config.txt','r') as f:
                ck = f.read().replace(' ','').replace('\n','')
        except:
            print('首次运行,正在创建配置文件...')
            with open('config.txt', 'a') as f:
                f.write(' ')
            ck = ''
        if ck:
            self.ck = ck
            print('正在加载配置文件...')
            #检测配置信息是否可用
            if '2020%2D2021%2D1' in self.ck:
                print('\r当前学期为:2020-2021-1',end='\r')
                print('\r已更改学期为:2020-2021-2',end='\r')
                self.ck.replace('2020%2D2021%2D1', '2020%2D2021%2D2')
            self.Cktest()
        else:
            print('配置文件不可用,请登陆')
            username = input("请输入学号:")
            password = getpass.getpass("请输入密码:")
            self.Login(username=username,password=password)
        try:
            f = csv.reader(open('教务处开课信息(含课程ID）.csv', encoding='utf-8'))
            data = list(f)
            self.url = os.path.dirname(os.path.abspath(__file__))
            os.chdir(self.url)
            # print(self.url)
            self.info = data
            self.bh_id,self.name_id = {},{}
            for i in data[1:]:
                self.bh_id[i[1]] = i[0]
                self.name_id[i[1]] = str(i[3]) + '-' + str(i[4])
        except:
            print('请将本程序与"教务处开课信息(含课程ID）.csv"文件放于同一文件下')


    '''登陆'''
    def Login(self,username,password):
        global isLogin,SemesterNum

        print('\r正在尝试登陆...', end='\r')

        '''获取登陆参数sign'''
        a = self.Requests.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp')
        sign = etree.HTML(a.text).xpath('//input[@name="sign"]/@value')[0]
        # print('got sign:',sign)

        '''进行登陆'''
        url = "http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp"
        payload = 'user=%s&pwd=%s&lb=S&submit=&sign=%s' % (username, password, sign)
        response = self.Requests.request("POST", url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload)

        '''检测登陆状态'''
        ck = ''
        for i, j in response.cookies.items():
            db = i + '=' + j + ';'
            ck += db
        self.ck = ck
        if len(self.ck) <= 70:
            print("登陆失败,用户名或密码错误，请重新尝试\n")
        else:
            print('\r登陆成功...', end='\r')
            if self.Requests.cookies.get('jcrj%5Fxueqi') != '2020%2D2021%2D2':
                print('\r检测当前学期不为:2020-2021-1',end='\r')
                self.Requests.cookies['jcrj%5Fxueqi'] = '2020%2D2021%2D2'
                print('\r已更改学期为:2020-2021-2    ',end='\r')
                SemesterNum = '当前学期:2020-2021-2'
                self.IntoConfig(self.ck.replace('2020%2D2021%2D1','2020%2D2021%2D2'))
            print('\r已写入配置文件config.txt中       ',end='\r')
            isLogin = True
            # '''学期检测'''
            # self.semesterTest()


    '''写入登陆ck'''
    def IntoConfig(self,content):
        with open('config.txt','w') as f:
            f.write(str(content))


    '''检测Ck是否可用'''
    def Cktest(self):
        headers = {
            'Proxy-Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/xszhinan.asp?title_id1=9&xueqi=2020-2021-2',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': self.ck
        }
        a = self.Requests.get(url='http://jiaowu.sicau.edu.cn/jiaoshi/bangong/main/xqzt.asp?dizhi=/jiaoshi/bangong/main/welcome1.asp',headers=headers)
        content = a.content
        respond = content.decode('gb2312', 'ignore')

        try:
            global SemesterNum,isLogin
            SemesterNum = etree.HTML(respond).xpath('//a[@class="menu"]/text()')[0]
            SemesterNum = SemesterNum[:-5]
            isLogin = True
        except:
            print('配置信息不可用,请尝试登陆')
            username = input("请输入学号:")
            password = getpass.getpass("请输入密码:")
            self.Login(username=username, password=password)


    '''检测学期信息'''
    def semesterTest(self):
        url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/main/xqzt.asp?dizhi=/jiaoshi/bangong/main/welcome1.asp'
        a = self.Requests.get(url)
        content = a.content
        respond = content.decode('gb2312', 'ignore')
        global SemesterNum
        SemesterNum = etree.HTML(respond).xpath('//a[@class="menu"]/text()')[0]
        SemesterNum = SemesterNum[:-5]
        if '2020-2021-2' not in SemesterNum:
            print('\r检测到当前学期状态不为2020-2021-2,正在尝试更改学期...', end='\r')
            self.ChangeSemester()


    '''更改学期状态'''
    def ChangeSemester(self):
        url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/main/xqzt.asp?xueqi=2020-2021-2&dizhi=/jiaoshi/bangong/main/welcome1.asp'
        a = self.Requests.get(url)
        content = a.content
        respond = content.decode('gb2312', 'ignore')
        print('\r返回消息:"%s"' % (re.findall("language=javascript>alert\(\'(.*?)\'\);", respond)[0]), end='\r')
        self.semesterTest()


    '''获取预选课程'''
    def GetPreClasses(self):
        url = 'http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/kaike_yuxuan.asp?title_id1=1'
        a = self.Requests.get(url)
        content = a.content
        respond = content.decode('gb2312', 'ignore')
        html = etree.HTML(respond)
        info = html.xpath('//div[@align="center"]/a/text()')
        if info:
            # info = info[1:]
            num = 0
            print('%s\t%s' % ('序号', '课程名称'))
            for i in info:
                num += 1
                print('%s\t%s'%(num,i[:-6]))
        else:
            print('返回信息: 您暂时没有预选2020-2021-2学期课程!')





    '''选课'''
    def ConfireClass(self, ClassID):
        '''查取课程编号对应的bianhao'''
        bianhao = self.bh_id.get(ClassID, None)
        if bianhao:
            print('\n正在尝试选取%s...',end='\r')
            url = 'http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/xuan_2018.asp?bianhao=' + str(bianhao)
            a = self.Requests.get(url)
            respond = a.content.decode('gb2312', 'ignore')
            print('\r                           ',end='\r')
            # print(respond)
            print('\r返回消息:', re.findall("<script language=JavaScript>alert\('(.*?)'\);", respond)[0], end='\r')
        else:
            print('\r输入课程编号有误，请核对后重试:)', end='\r')


    '''获取课程编号对应信息'''
    def FindUpBiaohao(self, ClassIDs=[]):
        num = 0
        for ClassID in ClassIDs:
            if ClassID in self.name_id.keys():
                for i in self.info:
                    if str(i[1]) == ClassID:
                        num += 1
                        print('''序号:%s
         课程编号:   %s
         课程名称:   (%s)%s
         任课单位:   %s
         任课教师:   %s
         上课时间:   %s
         教室地点:   %s
    计划-已选-余容:   %s
         优选专业:   %s'''%(num,i[1],i[5],i[4],i[2],i[14],i[7],i[6],str(i[15])+'-'+str(i[16])+'-'+str(i[17]),i[18]))
            else:
                print('\r输入课程编号有误，请核对后重试:)', end='\r')
        if num:
            print('\n共%s个搜索结果'%(num))




    '''抢预选课'''
    def ConfirePre(self):
        def Confire(addr):
            baseUrl = 'http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan'
            Url = baseUrl + addr
            a = self.Requests.get(Url)
            respond = a.content.decode('gb2312', 'ignore')
            print('\r                           ', end='\r')
            print('\r返回消息:', re.findall("<script language=JavaScript>alert\('(.*?)'\);", respond)[0], end='\r')
        url = 'http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/kaike_yuxuan.asp?title_id1=1'
        a = self.Requests.get(url)
        content = a.content
        respond = content.decode('gb2312', 'ignore')
        html = etree.HTML(respond)
        info = html.xpath('//div[@align="center"]/a/text()')
        if info:
            urls = html.xpath('//div[@align="center"]/a/@href')[1:]
            info = info[1:]
            num = 0
            print('%s\t%s' % ('序号', '课程名称'))
            for i in info:
                num += 1
                print('%s\t%s' % (num, i))
            for i,j in zip(info,urls):
                print('\r正在尝试选取:',i,end='\r')
                baseUrl = 'http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/'
                Url = baseUrl + j
                a = self.Requests.get(Url)
                respond = a.content.decode('gb2312', 'ignore')
                print('\r                           ', end='\r')
                print('\r返回消息:', re.findall("<script language=JavaScript>alert\('(.*?)'\);", respond)[0], end='\r')

        else:
            print('返回信息: 您暂时没有预选2020-2021-2学期课程!')

    '''获取本地的课程信息'''
    def FindByKeywords(self,ClassName):
        if ClassName in self.name_id.keys():
            print('有结果')
        else:
            db,numData = [],[]
            for i in ClassName:
                db.append(i)
            for i,j in self.name_id.items():
                # print('nameList:',j)
                if set(db).issubset(j):
                    numData.append(i)
        self.FindUpBiaohao(numData)




if __name__ == '__main__':
    Info = ''' 
                        iii              CCCS           SSSSS                           
                        iii          CCCCCCCCCCC     SSSSSSSSSSS                        
                        iii         CCCCC    CCC    SSSSS    SSS                        
                                   CCCC             SSS                                 
                   iiiiiiii        CCC              SSS                                 
                    iiiiiii        CCC              SSSS                                
                        iii        CCC               SSSSSSSS                           
                        iii        CCC                 SSSSSSSSS                        
                        iii        CCC                     SSSSSS                       
                        iii        CCC                        SSS                       
                        iii        CCCC                       SSSS                      
                        iii        CCCC                       SSS                       
                        iii         CCCCC    CCC    SSS     SSSSS                       
                   iiiiiiiiiiiii      CCCCCCCCCC    SSSSSSSSSSSS                        
                                         CCCC          SSSSSS      

                                    预祝您考试顺利！   
                    (本工具仅作为辅助作用         使用前请详细查看教程）  
                      GitHub地址:https://github.com/Upsetin/iCS 

        '''
    print(Info)
    SemesterNum = '-'
    isLogin = False
    while not isLogin:
        iCS = Sicau()
    Judge = True
    while Judge:
        while True:
            try:
                # print('{:*^50}'.format('请输入对应操作指令:)'),'\n*','{:^50}'.format('1:查看预选课'),'*','\n*','{:^48}'.format('2:抢预选课'),'*','\n*','{:^50}'.format('3:抢指定课程编号课'),'*','\n*','{:^50}'.format('4:查看课程编号对应课程信息'),'*','\n*','{:^50}'.format('0:退出程序',),'*\n',sep='')
#                 print(f'''
# ************************操作指令菜单**********************
# *{SemesterNum}                             *
# *                         抢课区                        *
# *                      1:抢指定编号课                    *
# *                      2:抢取预选课程                    *
# *                                                      *
# *                         查询区                        *
# *                      3:查看预选课程                    *
# *                      4:查看课程信息                    *
# *                      5:搜索关键词课程信息               *
# *                      0:立即退出程序                    *
# *                                                      *
# *************************操作指令菜单*********************
# 请输入指令数字:''',end='')
                print('\n')
                print(f'\n{SemesterNum}\n「抢课区」1:抢指定编号课  2:抢取预选课程\n「查询区」3:查看预选课程  4:查看课程信息  5:搜索关键词课程信息\n「退出程序」0:立即退出程序')
                num = int(input('请输入指令数字:'))
                break
            except:
                print("\r输入指令有误...", end='\r')
        if num == 0:
            Judge = False
            print("\n感谢使用，程序已退出:)")
        elif num == 1:
            ClassID = input("请输入课程ID:")
            iCS.ConfireClass(ClassID)
        elif num == 2:
            iCS.ConfirePre()
        elif num == 3:
            iCS.GetPreClasses()
        elif num == 4:
            ClassID = input("请输入课程ID:")
            iCS.FindUpBiaohao([ClassID])
        elif num == 5:
            ClassName = input("请输入课程名称关键词(搜索慕课请输入MOOC):")
            iCS.FindByKeywords(ClassName)
        else:
            print('⚠️输入指令有误,请核对后重试!')
