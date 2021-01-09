# iCS 🎉🎉🎉
该仓库将放于有关Sicau学校可用的脚本🙋🏻‍♂️  
有时间或手痒了就会持续更新下去🥳
```
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
                                                                               By White
                                                                              2020.01.10
```
- 若内容对您有所帮助,千万不要吝啬你的Star🌟!

## 1.教务处抢课脚本🗓
### 特性  
  
- [x] 实现登陆
- [x] 自动检测并切换学期  
- [ ] 抢课
> 已支持以下内容:
>+ 预选课 
>+ 指定编号课程
  
> 暂不支持以下内容:
>+ 带有实验的课程
- [ ] 查询
> 已支持以下内容:
>+ 指定编号课程信息  

> 暂不支持以下内容:
>- 查询预选课信息  

- [ ] 日志记录  
---
### 使用文档  
#### 须知:  
* 运行程序，按提示输入学号及教务处密码
>运行方法:  
>1.Py启动:  
>安装依赖requests,lxml第三方库,依次执行,已有可跳过.  
>`pip3 install requests`  
>`pip3 install lxml`
>安装完毕后,执行:
>`python3 jiaowu.py`
>
>2.可执行文件启动:
>`可执行文件在jiaowu文件夹里,双击执行即可`  
![程序初始界面](https://i.loli.net/2021/01/10/jBZ4tFa57x6OPNh.png "程序初始界面")
> ⚠️注意输入密码时,终端并不会回显,凭直觉输入密码即可    
   
* 登陆成功后,根据提示输入对应指令序号即可 
![登陆成功界面](https://i.loli.net/2021/01/10/JRWnf1DGuwQ2iIH.png "登陆成功界面")  
  
* 以下内容对各操作进行详细说明:   
```
1.查看预选课程:  
    在终端输入数字1,程序会自动获取已预选课程,并打印出已选课程清单信息.    
2.抢取预选课程  
    在终端输入数字2,程序会自动获取已预选课程,并打印出已选课程清单,并逐个选取预选课程,并实时显示正在选取的课程进度. 
3.抢指定编号课  
    在终端输入数字3,按照程序提示输入课程编号,程序打印对应的课程信息,并实时打印抢课信息.
4.查看课程信息  
    在终端输入数字4,按照程序提示输入课程编号,程序打印对应的课程信息.  
0.立即退出程序  
    在终端输入数字0,程序会自主退出并输出 感谢使用，程序已退出:) 字样
```

- 注意⚠️:  
```
1.课程编号获取方法:
在jiaowu文件夹内'教务处开课信息(含课程ID）.csv'里,或提前在教务网查询并记录课程编号.  
2.若输入指令序号有误,程序会提示并回到主菜单.  
3.无论当前指令是否顺利执行,当前指令执行完毕后,都会返回主菜单,即指令选择界面.  
```
- 重要🙋🏻‍♂️  
```
1.使用时一定要核对课程信息是否正确!
2.在程序使用结束后,在教务网上核对课程信息,若课程有误,请及时退课重选!
3.程序暂时无法抢取有实验课的理论课,因为实验课是有时间选择,届时请自行在教务处选取!
```
# 一切信息以教务处信息为准!本工具只起辅助作用!  
---




## 联系方式
[邮箱: xiaobaiyeaidaima@gmail.com](mailto:xiaobaiyeaidaima@gmail.com)  
[QQ: 2063546307](http://wpa.qq.com/msgrd?v=3&uin=2063546307&site=qq&menu=yes)  
[Vx: Sweetie_Falcon]()