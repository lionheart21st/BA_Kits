# pandas的read_excel方法功能强大，当然 参数也非常多（而且 往往赋值方式不同 含义还不同），这里做了必要、简洁的总结 :)
### 该方法非常重要 在读取Excel数据的同时 进行必要的预处理 从而提高整个数据处理流程的效率和质量！



# 最常用参数

* io参数：指定所要读取的Excel文件的路径  //通常直接作为位置参数使用
* sheet_name参数：指定所要读取的sheet页，可以用字符串（sheet页名）、数字（sheet页索引）和列表（多个sheet页）赋值    //读取多张sheet页时，返回值类型为字典，key是sheet页索引 value是DataFrame
* header参数：指定表头行，可以用数值（表示第几行是表头）、列表（复合表头）和None（无表头）赋值
* index_col参数：指定索引列，可以用数值（列索引）、字符串（列名）和列表（多个索引列）赋值  //注意：使用列表的时候 列表元素只能是数值 不能是字符串
* usecols参数：指定导入列，可以使用列表（元素可以是字符串即列名，也可以是数值解列索引）、字符串（Excel列标、切片）和lambda函数（逻辑）赋值
* skiprows参数：跳过指定行（有时候Excel表格在sheet页的“当中”），可以用数值（表示从头跳过几行）、列表（元素为数值 表示行索引，表示跳过哪些行）  //注意：没有“跳过列”参数，使用usecols来实现“跳过列”
* names参数：自定义表头，使用列表（列表元素就是自定义的列名）赋值



# 预处理参数

* dtype参数：指定列的dtype类型，使用字典（key列名，value类型）赋值

* parse_dates参数：指定列解析为时间戳（datetime64[ns]）格式，可以使用True(表示 把行索引解析为时间戳)、列表（指定哪些列解析为时间戳）、二维列表（指定哪些列 合并解析为时间戳）、字典（key为合并解析后的列名，value指定哪些列进行合并解析）

* date_parser参数：指定时间解析方法（主要针对 中文时间格式的解析），可以用lambda函数赋值（比如：lambda x:pd.to_datetime(x,format='%Y年%m月%d日')）

* na_values参数：自定义缺失值（解析为NaN），可以用数值和字符串（表示 自定义单个缺失值）、列表（表示 定义多个缺失值）、字典（表示 自定义的缺失值在哪列有效）

* converters参数：指定列进行数据转换，使用字典，比如：converters={'销量':lambda x:np.NaN if str(x).isspace() else str(x).strip()}  //对'销量'列（dtype是object）做这样的处理：如果 单元格数据是空 就解析为NaN（缺失值），如果非空 则去重单元格数据首尾可能存在的空格（数据清洗）

* true_values、false_values参数：自定义真值与“假值”，使用字符串列表赋值，全列数据都在这两个列表中 才会被解析为True或则False

* thousands参数：指定千分位的标记（金额数据常用千分位表示），比如 thousands=","将逗号指定为千分位分隔符

* nrows参数：指定读取Excel表的多少行数（不算表头）

* mangle_dupe_cols参数：默认为True 表示自动重命名“重复的列名”，赋值为False 表示如果有“重复的列名”就抛异常  //Excel表格中，是允许列名重复的！

  