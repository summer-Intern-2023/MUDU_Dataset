import os
import sys
import django
import sqlite3
import csv


# 设置项目根目录路径
script_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.abspath(os.path.join(script_directory, ".."))
sys.path.append(project_directory)

# 设置DJANGO_SETTINGS_MODULE环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "llmdataset.settings")

# 初始化Django
django.setup()
from setcollect.models import Tag, Word


def import_csv_to_sqlite_label(csv_file, db_file, table_name):
    # 连接到SQLite数据库
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 创建表
    create_table_query = "CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, tag_classification TEXT, tag_name TEXT)".format(
        table_name
    )
    cursor.execute(create_table_query)

    # 打开CSV文件并导入数据
    with open(csv_file, "r", newline="", encoding="gbk") as file:
        csv_data = csv.reader(file)
        next(csv_data)
        # 逐行读取CSV文件并插入数据
        for row in csv_data:
            tag_classification = row[0]  # 第一个单元格是分类名称

            # 从第二个单元格开始遍历每个标签，并插入到数据库中
            for tag_name in row[1:]:
                if (
                    tag_name and not Tag.objects.filter(tag_name=tag_name).exists()
                ):  # 检查标签名称是否为空且不存在于数据库中
                    print("Tag Classification:", tag_classification)  # 打印分类名称
                    print("Tag Name:", tag_name)  # 打印标签名称

                    # 创建Tag实体并保存到数据库
                    tag = Tag(tag_classification=tag_classification, tag_name=tag_name)
                    tag.save()

    # 提交更改并关闭数据库连接
    conn.commit()
    conn.close()


def import_csv_to_sqlite_word(csv_file, db_file, table_name):
    # 连接到SQLite数据库
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 创建表
    create_table_query = "CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, word_tag TEXT)".format(
        table_name
    )
    cursor.execute(create_table_query)

    with open(csv_file, "r", newline="", encoding="gbk") as file:
        csv_data = csv.reader(file)
        next(csv_data)
        # 逐行读取CSV文件并插入数据
        for row in csv_data:
            word_txt = row[0]  # 第一个单元格是分类名称
            for tag_name in row[1:]:
                if (
                    tag_name and Tag.objects.filter(tag_name=tag_name).exists()
                ):  # 检查标签名称是否为空且存在于数据库中
                    print("Word:", word_txt)  # 打印分类名称
                    print("Tag Name:", tag_name)  # 打印标签名称

                    word, created = Word.objects.get_or_create(word=word_txt)
                    tag = Tag.objects.get(tag_name=tag_name)
                    word.word_tag.add(tag)
                    word.save()
    # 提交更改并关闭数据库连接
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # CSV文件路径
    csv_file_label = os.path.join(project_directory, "label.csv")

    # SQLite数据库文件路径
    db_file_label = os.path.join(project_directory, "db.sqlite3")

    # 表名
    table_name_label = "setcollect_tag"

    # 导入CSV文件到SQLite数据库
    import_csv_to_sqlite_label(csv_file_label, db_file_label, table_name_label)

    # CSV文件路径
    csv_file_word = os.path.join(project_directory, "word.csv")

    # SQLite数据库文件路径
    db_file_word = os.path.join(project_directory, "db.sqlite3")

    # 表名
    table_name_word = "setcollect_word"

    # 导入CSV文件到SQLite数据库
    import_csv_to_sqlite_word(csv_file_word, db_file_word, table_name_word)
