import requests,re,csv,time
from lxml import etree

from selenium import webdriver


def Login(username='你的学号',password='密码'):
    driver = webdriver.Chrome()
    driver.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp')
    driver.find_element_by_id('txtUser').send_keys(username)
    driver.find_element_by_id('Userpwd').send_keys(password)
    driver.find_element_by_xpath('//input[@value="S"]').click()
    driver.find_element_by_name('submit').click()



class ClassesInfo():
    def __init__(self):
        self.OutFile([['课程ID','编号', '任课单位', '分组编号', '课程', '课程性质', '教室', '上课时间', '周次', '学分', '理论学时', '实验学时', '实践', '总学时', '教师',
                  '计划人数', '已选人数', '余容', '优选专业', '锁定', '校区', '课程类别', '课程体系', '排课类别', '单列实验']])

    def GetInfoUrl(self,url='http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/kai.asp?title_id1=2'):
        a = requests.get(url, headers={'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'Origin': 'http://jiaowu.sicau.edu.cn', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Referer': 'http://jiaowu.sicau.edu.cn/web/web/web/index.asp', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Cookie': '_ga=GA1.3.412538794.1597571429; ASPSESSIONIDASSSSDDB=JPPBNHEAEFPGDMGNDLLGDAAJ; jcrj%5Fuser=201900550; jcrj%5Fpwd=275358; jcrj%5Fauth=True; jcrj%5Fnj=2019; jcrj%5Fjwc%5Fcheck=y; ASPSESSIONIDAQQTTABD=KLGMIAPAIBMNJJFIKCJABNND; jcrj%5Ftemp=4470636248; jcrj%5Fxm=%CD%F5%BA%E7%BD%DC; jcrj%5Fxt%5Ffb=%D1%C5%B0%B2; jcrj%5Fxt%5Fxxq=%D1%C5%B0%B2; jcrj%5Fsf%5Fpj=%B7%F1; jcrj%5Fxibie=%C9%FA%C3%FC%BF%C6%D1%A7%D1%A7%D4%BA; jcrj%5Fzy=%C9%FA%CE%EF%B9%A4%B3%CC; jcrj%5Ftymfg=%C0%B6%C9%AB%BA%A3%CC%B2; jcrj%5Fxzy=%BC%C6%CB%E3%BB%FA%BF%C6%D1%A7%D3%EB%BC%BC%CA%F5; jcrj%5Fbanhao=%C9%FA%B9%A4201903; jcrj%5Fsf=%D1%A7%C9%FA; jcrj%5Fjc24=%CE%DE; jcrj%5Fjc23=%CE%DE; jcrj%5Fjc52=%CE%DE; jcrj%5Fjc64=%CE%DE; jcrj%5Fjc63=%CE%DE; jcrj%5Fjc62=%CE%DE; jcrj%5Fjc61=%CE%DE; jcrj%5Fjc14=%CE%DE; jcrj%5Fjc41=%CE%DE; jcrj%5Fsession=jwc%5Fcheck%2Cauth%2Cuser%2Cpwd%2Cxt%5Ffb%2Cxt%5Fxxq%2Csf%2Cxueqi%2Csf%5Fpj%2Ctemp%2Cxm%2Cnj%2Cbanhao%2Cxibie%2Czy%2Cxzy%2Cjwc%5Fcheck%2Cxqdz%2Ctymfg%2Cxk%5Fzy%2Cxk%5Fcongxiu%2Cjc11%2Cjc12%2Cjc13%2Cjc14%2Cjc15%2Cjc21%2Cjc22%2Cjc23%2Cjc24%2Cjc25%2Cjc31%2Cjc32%2Cjc33%2Cjc34%2Cjc35%2Cjc41%2Cjc42%2Cjc43%2Cjc44%2Cjc45%2Cjc51%2Cjc52%2Cjc53%2Cjc54%2Cjc55%2Cjc61%2Cjc62%2Cjc63%2Cjc64%2Cjc65%2Cww%5Fzd%2C; jcrj%5Fww%5Fzd=%B1%E0%BA%C5; jcrj%5Fjc21=111111111111111111000000000000; jcrj%5Fjc22=000111111111111000000000000000; jcrj%5Fjc25=000000001111111110000000000000; jcrj%5Fjc51=111111111111111100000000000000; jcrj%5Fjc53=%CE%DE; jcrj%5Fjc54=000001111111111110000000000000; jcrj%5Fjc55=%CE%DE; jcrj%5Fjc31=%CE%DE; jcrj%5Fjc32=010101010101010100000000000000; jcrj%5Fjc33=%CE%DE; jcrj%5Fjc34=001010101010101000000000000000; jcrj%5Fjc35=%CE%DE; jcrj%5Fjc11=111111111111111100000000000000; jcrj%5Fjc12=011111100000000000000000000000; jcrj%5Fjc13=111111111111111000000000000000; jcrj%5Fjc15=000000000001010100000000000000; jcrj%5Fjc65=%CE%DE; jcrj%5Fjc42=111111111111110000000000000000; jcrj%5Fjc43=011111111111111000000000000000; jcrj%5Fjc44=000101010101010000000000000000; jcrj%5Fjc45=111111111111111000000000000000; jcrj%5Fxk%5Fzy=%B7%F1; jcrj%5Fxk%5Fcongxiu=%CA%C7; jcrj%5Fxqdz=http%3A%2F%2Fjiaowu%2Esicau%2Eedu%2Ecn%2Fxuesheng%2Fgongxuan%2Fgongxuan%2Fkai%2Easp%3Ftitle%5Fid1%3D2; jcrj%5Fxueqi=2020%2D2021%2D2'})
        content = a.content.decode('gb2312', 'ignore')
        html = etree.HTML(content)
        names = html.xpath('//td[@width="549"]/a/text()')
        urls = html.xpath('//td[@width="549"]/a/@href')
        # print(names)
        # print(urls)
        db = []
        for i in urls:
            i = 'http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/' + i
            db.append(i)
        self.names,self.urls = names,db
        self.GetInfo()


    def GetInfo(self):

        '''webdriver'''
        # 设置Chrome为无显示
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')
        option.add_argument('--headless')
        driver = webdriver.Chrome(options=option)
        driver.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp')
        driver.find_element_by_id('txtUser').send_keys('201900550')
        driver.find_element_by_id('Userpwd').send_keys('275358')
        driver.find_element_by_xpath('//input[@value="S"]').click()
        driver.find_element_by_name('submit').click()
        driver.get(url='http://jiaowu.sicau.edu.cn/jiaoshi/bangong/main/xqzt.asp?xueqi=2020-2021-2')

        alert = driver.switch_to.alert  # 创建弹窗对象
        alert.accept()  # 点击弹窗中的【确定】

        for i,j in zip(self.names,self.urls):
            if i != '全校课程汇总':
                continue
            print(f'正在收集{i}信息:',j)
            '''webdriver'''
            driver.get(j)

            content = driver.page_source
            self.ToInfo(content)
            # 翻页操作
            while True:
                try:
                    driver.find_element_by_xpath('//td[@title="下一页"]/a').click()
                    # time.sleep(3)
                    content = driver.page_source
                    self.ToInfo(content)
                except:
                    print("已到最后一页")
                    break


    def ToInfo(self,content):
        html = etree.HTML(content)
        '''栏目及内容'''
        names = html.xpath('//td[@class="g_body"]')
        db = []
        for i in names:
            string = i.xpath('string(.)').replace('\n', '').replace(' ', '')
            if string:
                pass
            else:
                string = '-'
            db.append(string)
        bianhao = html.xpath('''//a[@onclick="return confirm('确定要选择此课程嘛？')"]/@href''')
        # print(bianhao)
        Info = []
        for i in range(0, len(db), 24):
            Info.append(db[i:i + 24])
        # 组合信息
        for i, j in zip(Info, bianhao):
            j = re.findall('\d{10,}', j)[0]
            i.insert(0, j)
        print(Info)
        for i in Info:
            for j in i:
                pass
                # print('{:^20}'.format(j), end='')
        self.OutFile(Info)

    def OutFile(self,Data):
        FileNmae = '教务处开课信息(含课程ID）.csv'
        file = open(FileNmae, 'a', encoding='utf-8')
        f = csv.writer(file)
        f.writerows(
            Data
        )
        file.close()


if __name__ == '__main__':
    #写入表头
    cs = ClassesInfo()
    cs.GetInfoUrl()
