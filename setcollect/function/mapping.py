from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import (
    PromptTemplate,
)
from langchain.llms import OpenAI

import sys

from setcollect.models import (
    UserInfo,
    Conversation,
    Question,
    LModel,
    Tag,
    Title,
    Sentences,
    Word,
)

response_schemas_word_to_titles = [
    ResponseSchema(name="Emotion", description="第一个步骤的回答"),
    ResponseSchema(
        name="Words",
        description="应该是从词库中挑选的词语",
    ),
    ResponseSchema(
        name="Sentences",
        description="用词语们生成的一些句子，每个句子可以包含多个词语",
    ),
]
output_parser_word_to_titles = StructuredOutputParser.from_response_schemas(
    response_schemas_word_to_titles
)
format_instructions_word_to_titles = (
    output_parser_word_to_titles.get_format_instructions()
)

#  templete for mapping words to titles
template_word_to_titles = """/
    你是一个小学语文老师，请根据这个题目的要求和内容从一下词库中挑选可能用在作文中的词语。以下是题目要求: {title}。以下是词库: {word_list}。
    根据以下步骤来完成任务，任务顺序按照数字从小到大排序：
    1: 分析作文题目的情感基调, 并单独输出情感基调的列表. 列出所有感情基调
    2: 根据上述的分析结果从词库中列举出合适的词语, 如果没有合适的词语则输出一个空的list. 列出所有的词语 例如: ["词语1", "词语2", "词语3"]
    3: 根据挑选的词语,并且将词语造句, 可以在一个句子中运用多个词语. 造句的时候需要注意句子的语法和逻辑并且需要符合作文的主题和情感基调. 句子要适用于作文的开头, 中间, 或者结尾. 列举出所有的句子. 列出所有的句子 例如: ["句子1", "句子2", "句子3"]
    最后的输出应该是这个格式的 [[情感基调], [词语], [句子] {format_instructions}
    """

"""
output a generator that
generate (title((type = string) name(type = list), emotion(type = list), words(type = list), sentences(type = list)) 
from mapping words to titles
"""


def mapping_titles_to_words():
    word_list = []
    model = OpenAI(
        openai_api_key="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",
        temperature=0,
    )

    prompt = PromptTemplate(
        template=template_word_to_titles,
        input_variables=["title", "word_list"],
        partial_variables={"format_instructions": format_instructions_word_to_titles},
    )

    for word in Word.objects.all():
        word_list.append(word.word)

    for title in Title.objects.all():
        _input = prompt.format(title=title.title, word_list=word_list)
        output = model(_input)
        output = output_parser_word_to_titles.parse(output)
        yield title, output["Emotion"], output["Words"], output["Sentences"]
