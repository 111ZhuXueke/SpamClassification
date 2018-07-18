import os
import sys
import time

startTime = time.time();
index_path = "./index"
# 判别邮件是否属于垃圾邮件
def labelDict(path):
    type = {"spam":"1","ham":"0"};
    index_file = open(path);
    index_dict = {};
    try:
        for line in index_file:
            str = line.split(" ");
            if len(str) == 2:
                key,value = str
            else:continue;
            value = value.replace('../data','').replace('\n','')
            index_dict[value] = type[key.lower()]
    finally:
        index_file.close();
    return index_dict;

# 格式化邮件内容，取出有用信息
def standaScalerEmailContent(path):
    file = open(path, "r", encoding="gb2312", errors='ignore')
    content_dict = {}
    try:
        is_content = False;
        for line in file:
            line = line.strip();
            if line.startswith("From:"):
                content_dict["from"] = line[5:]
            elif line.startswith("To:"):
                content_dict['to'] = line[3:]
            elif line.startswith("Date:"):
                content_dict['date'] = line[5:]
            else:
                is_content = True;

            if is_content:
                if "content" in content_dict:
                    content_dict['content'] += line
                else:
                    content_dict['content'] = line
    finally:
        file.close();
    return content_dict;

# 返回邮件内容，每一个邮件之间使用 \n 隔开
def dictCaseToStringLine(path):
    content_dict = standaScalerEmailContent(path);
    #  去掉所有英文 ','，保留中文逗号
    result_str = content_dict.get('from', 'unkown').replace(',','').strip() + ',';
    result_str += content_dict.get('to', 'unkown').replace(',','').strip() + ',';
    result_str += content_dict.get('date', 'unkown').replace(',','').strip() + ',';
    result_str += content_dict.get('content', 'unkown').replace(',','').strip();
    return result_str;

index_dict = labelDict(index_path);
data_path = 'D:\\python\\data\\email\\trec06c\\data';
list0 = os.listdir(data_path);
# 得到文件夹目录
for item in list0:
    item_path = data_path + '\\' + item;
    # 获取文件夹下面的每一个文件夹
    list1 = os.listdir(item_path);
    # 将每一个文件下面的邮件内容分别合并
    marge_file = "D:\\python\\data\\email\\trec06c\\pros" + "\\" + "process_" + str(item);
    print("File %s正在写入......" % marge_file,end='')
    with open(marge_file,'w',encoding = 'utf-8') as writer:
        for item2 in list1:
            item2_path = item_path + "\\" + item2;
            index_key = "/" + item + "/" + item2;
            if index_key in index_dict:
                lineStr = dictCaseToStringLine(item2_path);
                # 末尾追加垃圾邮件标识
                lineStr += "," + index_dict[index_key] + "\n";
                writer.writelines(lineStr);
    print("写入完毕!")
with open("D:\\python\\data\\email\\trec06c\\pros\\result_process",'w',encoding = 'utf-8') as writer:
    print("File result_process正在写入......" ,end='')
    for item in list0:
        file_path = "D:\\python\\data\\email\\trec06c\\pros\\" + "process_" + str(item);
        with open(file_path, encoding = 'utf-8') as file:
            for line in file:
                writer.writelines(line)
    print("写入完毕!")
endTime = time.time();
print('数据处理总共耗时%.2fs'%(endTime - startTime));



