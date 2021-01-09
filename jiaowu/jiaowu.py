import requests, re
from lxml import etree

import getpass


class Sicau():
    '''登陆'''

    def __init__(self, username='', password=''):
        global isLogin
        self.Requests = requests.session()
        print('\r正在尝试登陆...', end='\r')
        '''获取登陆参数sign'''
        a = self.Requests.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp')
        sign = etree.HTML(a.text).xpath('//input[@name="sign"]/@value')[0]
        # print('got sign:',sign)

        '''进行登陆'''
        url = "http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp"

        payload = 'user=%s&pwd=%s&lb=S&submit=&sign=%s' % (username, password, sign)
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'http://jiaowu.sicau.edu.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://jiaowu.sicau.edu.cn/web/web/web/index.asp',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        response = self.Requests.request("POST", url, headers=headers, data=payload)

        ck = ''
        for i, j in response.cookies.items():
            db = i + '=' + j + ';'
            ck += db
        self.ck = ck
        if len(self.ck) <= 70:
            print("\r登陆失败,用户名或密码错误，请重新尝试\n", end='\r')
        else:
            print('\r登陆成功...', end='\r')
            isLogin = True
            self.semesterTest()

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

    '''获取预算课程'''

    def GetPreClasses(self):
        url = 'http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/xuan_2018.asp?bianhao=' + str(
            899679718199025481334403813310638134631381992934860344979721228986024077)
        a = self.Requests.get(url)
        content = a.content
        respond = content.decode('gb2312', 'ignore')
        print('\r返回消息:', re.findall("<script language=JavaScript>alert\('(.*?)'\);", respond)[0], end='\r')

    '''选课'''

    def ConfireClass(self, ClassID):

        '''查取课程编号对应的bianhao'''
        data = {'test': 'test'}
        bianhao = data.get(ClassID, None)
        if bianhao:
            url = 'http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/xuan_2018.asp?bianhao=' + str(bianhao)
            a = self.Requests.get(url)
            respond = a.content.decode('gb2312', 'ignore')
            print('\r返回消息:', re.findall("<script language=JavaScript>alert\('(.*?)'\);", respond)[0], end='\r')
        else:
            print('\r输入课程编号有误，请核对后重试:)', end='\r')

    '''获取课程对应的biaohao'''

    def FindUpBiaohao(self, ClassID):
        data = {'test': 'test'}
        StuID = data.get(ClassID, '\r输入课程编号有误，请核对后重试:)')
        '''输出对应课程信息'''
        print(StuID, end='\r')

    '''抢预选课'''

    def ConfirePre(self):
        pass

    '''获取本地的课程信息'''

    def GetLocalInfo(self):
        pass


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
            (本工具仅作为辅助作用，后果自担，使用前请详细查看教程）                    
'''
    print(Info, end='\r')
    SemesterNum = '-'
    isLogin = False
    while not isLogin:
        username = input("请输入学号:")
        password = getpass.getpass("请输入密码:")
        iCS = Sicau(username=username, password=password)
    Judge = True
    while Judge:
        while True:
            try:
                # print('{:*^50}'.format('请输入对应操作指令:)'),'\n*','{:^50}'.format('1:查看预选课'),'*','\n*','{:^48}'.format('2:抢预选课'),'*','\n*','{:^50}'.format('3:抢指定课程编号课'),'*','\n*','{:^50}'.format('4:查看课程编号对应课程信息'),'*','\n*','{:^50}'.format('0:退出程序',),'*\n',sep='')
                print(f'''
\r
*******************请输入对应操作指令:)********************
*{SemesterNum}                             * 
*                      1:查看预选课程                    *
*                      2:抢取预选课程                    *
*                      3:抢指定编号课                    *
*                      4:查看课程信息                    *
*                      0:立即退出程序                    *
*******************请输入对应操作指令:)********************
''', end='\r')
                num = int(input())
                break
            except:
                print("\r输入指令有误...", end='\r')
        if num == 0:
            Judge = False
            print("\r感谢使用，程序已退出:》", end='\r')
        elif num == 1:
            iCS.GetPreClasses()
        elif num == 2:
            pass
        elif num == 3:
            ClassID = input("请输入课程ID")
            iCS.ConfireClass(ClassID)
        elif num == 4:
            ClassID = input("请输入课程ID")
            iCS.FindUpBiaohao(ClassID)
