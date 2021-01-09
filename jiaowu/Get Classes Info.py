import requests,re,csv,time
from lxml import etree

from selenium import webdriver


def Login(username='201900550',password='275358'):
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
        a = requests.get(url, headers={'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'Origin': 'http://jiaowu.sicau.edu.cn', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Referer': 'http://jiaowu.sicau.edu.cn/web/web/web/index.asp', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Cookie': 'jcrj%5Fbanhao=%E7%94%9F%E5%B7%A5201903;jcrj%5Fnj=2019;jcrj%5Fpwd=275358;jcrj%5Fsession=xt%5Ffb%2Cxt%5Fxxq%2Csf%2Cxueqi%2Csf%5Fpj%2Ctemp%2Cuser%2Cpwd%2Cxm%2Cnj%2Cbanhao%2Cxibie%2Czy%2Cxzy%2C;jcrj%5Fsf=%E5%AD%A6%E7%94%9F;jcrj%5Fsf%5Fpj=%E5%90%A6;jcrj%5Ftemp=6915399432;jcrj%5Fuser=201900550;jcrj%5Fxibie=%E7%94%9F%E5%91%BD%E7%A7%91%E5%AD%A6%E5%AD%A6%E9%99%A2;jcrj%5Fxm=%E7%8E%8B%E8%99%B9%E6%9D%B0;jcrj%5Fxt%5Ffb=%E9%9B%85%E5%AE%89;jcrj%5Fxt%5Fxxq=%E9%9B%85%E5%AE%89;jcrj%5Fxueqi=2020%2D2021%2D1;jcrj%5Fxzy=%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6%E4%B8%8E%E6%8A%80%E6%9C%AF;jcrj%5Fzy=%E7%94%9F%E7%89%A9%E5%B7%A5%E7%A8%8B;'})
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

        for i,j in zip(self.names,self.urls):
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
        urls = html.xpath('//a[@onclick="return confirm(\'确定要选择此课程嘛？\')"]/@href')
        Info = []
        for i in range(0, len(db), 24):
            Info.append(db[i:i + 24])
        # 组合信息
        for i, j in zip(Info, urls):
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
