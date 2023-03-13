import pymysql
import matplotlib.pyplot as plt
import numpy as np
import nltk

class OperationMysql:
    def __init__(self):
        # 创建一个连接数据库的对象
        self.conn = pymysql.connect(
            host='127.0.0.1',  # 连接的数据库服务器主机名
            port=3306,  # 数据库端口号
            user='root',  # 数据库登录用户名
            passwd='123456',
            db='digdata',  # 数据库名称
            charset='utf8',  # 连接编码
            cursorclass=pymysql.cursors.DictCursor
        )
        # 使用cursor()方法创建一个游标对象，用于操作数据库
        self.cur = self.conn.cursor()
 
    # 查询一条数据
    def search_one(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchone()  # 使用 fetchone()方法获取单条数据.只显示一行结果
        return result
    
    def search_all(self,sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()  # 显示所有结果
        return result

op_mysql = OperationMysql()

#sqlData:由数据库查询得到的未标准化数据
sqlData = op_mysql.search_all("select * from `学生综合完成情况` natural join `入学信息` natural join exam1 natural join exam3 natural join exam4 natural join fexam")

#watchTimes:所有视频观看时长
watchTimes = op_mysql.search_all('select `视频观看时长` from `学生综合完成情况` where `视频观看时长`!=""')

#maxDiscuss:第二大的讨论数
maxDiscuss = op_mysql.search_all('select `讨论数` from `学生综合完成情况` order by `讨论数` desc limit 1,1')

#maxChapter：第二大的章节学习次数
maxChapter = op_mysql.search_all('select `章节学习次数` from `学生综合完成情况` order by `章节学习次数` desc limit 1,1')

#全局变量定义处

sidDict = {} #sid字典
pSumScore = {'上海':660,'江苏':680} #存储不同省份的高考总分
maxWatchTime = 0 #最大视频观看时长
secondDiscussNum = int(maxDiscuss[0].get('讨论数')) #第二大讨论数
secondChapterTime = int(maxChapter[0].get('章节学习次数')) #第二大章节学习次数
stuNum = len(sqlData) #学生总数
avgClassNum = 173 #三个班级中最大人数 

#计算最大视频观看时长
for wtdict in watchTimes:
    wt = float(wtdict.get('视频观看时长')[0:-2])
    maxWatchTime = max(maxWatchTime,wt)
    
#对不同的数据进行解析
class formatMgr:
    #解析sid: 9bf026952aac0f2955f0139010883ac0->0
    def fsid(self,sid):
        sidLen = len(sidDict) #sidLen为sid映射值,即简化的sid
        sidDict[sid] = sidLen
        return sidLen
    
    #解析字符串分数为浮点分数: 37/50->0.74
    def str2fra(self,data):
        s = int(data.split('/')[0])
        f = int(data.split('/')[1])
        return round(s/f,2)
    
    #解析视频观看时长：461.9分钟->461.9
    def fwatchTime(self,data):
        watchTime = data[0:-2]
        return float(watchTime)
    
    #标准化高考分数,返回将分数除以总分
    def fcollegeScore(self,score,province):
        if province in pSumScore.keys():
            sumScore = pSumScore[province]
        else:
            sumScore = 750 #否则默认750分
        return round(score/sumScore,2)
    
    #标准化次数，返回data/maxTime，且若data>maxTime或data为None则返回-1
    def ftime(self,data,maxTime):
        if data == None:
            return -1
        time = int(data)
        if time > maxTime:
            return -1
        else:
            return round(time/maxTime,2)
    

#标准化
def formatSql(sql):
    fmgr = formatMgr()
    formatData = [] 
    sid = fmgr.fsid(sql.get('SID'))
    taskFinishRate = fmgr.str2fra(sql.get('任务完成数'))
    mvProcessRate = fmgr.str2fra(sql.get('课程视频进度'))
    chapterProcessRate = fmgr.str2fra(sql.get('章节测验进度'))
    mvWatchtimeRate = round(fmgr.fwatchTime(sql.get('视频观看时长'))/maxWatchTime,2)
    discussRate = fmgr.ftime(sql.get('讨论数'),secondDiscussNum)
    chapterRate = fmgr.ftime(sql.get('章节学习次数'),secondChapterTime)
    scoreRate = fmgr.fcollegeScore(sql.get('高考分数'),sql.get('省份'))
    rank1 = fmgr.ftime(sql.get('rank1'),avgClassNum)
    rank3 = fmgr.ftime(sql.get('rank3'),avgClassNum)
    rank4 = fmgr.ftime(sql.get('rank4'),avgClassNum)
    rankf = fmgr.ftime(sql.get('rankf'),avgClassNum)
    if discussRate==-1 or chapterRate==-1 or rank1==-1 or rank3==-1 or rank4==-1 or rankf==-1:
        return None
    rankScore = 1 - (rank1*0.1+rank3*0.2+rank4*0.35+rankf*0.35)
    formatData = [sid,taskFinishRate,mvProcessRate,chapterProcessRate,mvWatchtimeRate,discussRate,chapterRate,scoreRate,rankScore]
    return formatData


    
datas = []
for oneSql in sqlData:
    fsql = formatSql(oneSql)
    if fsql == None:
        continue
    datas.append(fsql)
    
dataArray = np.array(datas)  #dataArray为预处理完成后的值