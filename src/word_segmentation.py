import xlrd
from zhon.hanzi import punctuation

chinese_dict = []
word_max_len = None 


def dict_generate(excel_name):
    """打开一个词典
    Args：
        excel_name：词典库的excel格式的文档名
    Returns:
        一个有词语组成的list
    """

    execl = xlrd.open_workbook(excel_name)
    table = execl.sheets()[0] 
    nrows = table.nrows 
    dict = [ x for i in range(nrows) for x in table.row_values(i)[:1]]
    return dict


def word_segment(input_str):
    """简单分词实现
    
    基于词典chinese_dict，返回输入语句所有可能的分词结果
    1.  初始条件
    找到第一个可分的单词
    
    2.  求解公式
        s包含s0到sn个可分割的句子
        word_segment(s+c) = word_segment(s0) + s - s0 + c
                          = word_segment(s1) + s - s1 + c
                          = word_segment(s2) + s - s2 + c
                      
    上述任何一种情况存在则有解，否则无解
    
    Args:
        input_str:待分词的句子
    Returns:
        每种分词结果为一个list，每种分词结果再组成一个list，
        并作为结果返回    
    """
    
    global chinese_dict
    global word_max_len

    dim = len(input_str) + 1
    result = [[] for i in range(dim)]
    
    segment_position = []
    segment_position.append(0)
    for i in range(1, dim):
        # 如果遇到标点，则标点前的句子必须可分，而且后续的比较只需要从这个标点开始比即可
        if input_str[i-1:i] in punctuation:
            if can_segment:
                segment_position = []
                segment_position.insert(0, i)
                result[i] = result[i-1]
                continue
            else:
                return []
        
        can_segment = False
        for j in segment_position:
            # 大于最大的单词长度直接退出
            if i - j > word_max_len:
                break
        
            if input_str[j:i] in chinese_dict:
                can_segment = True
                # 为第一个分词做特殊处理
                if j == 0:
                    result[i].append([input_str[j:i]])
                else:
                    # 为每个情况生成一个新的分词组合
                    for current_segment in result[j]:
                        if j == 0:
                            temp = []
                            temp.append(input_str[j:i])
                        else:
                            temp = [x for x in current_segment]
                            temp.append(input_str[j:i])
                        # 将原来的情况和新的情况链接起来
                        result[i].append(temp)
        if can_segment:
            segment_position.insert(0, i)
                        
    return result[dim - 1]


chinese_dict = dict_generate('../data/综合类中文词库.xlsx')# 从词典库中读取的单词
word_max_len = max(map(len, chinese_dict))
