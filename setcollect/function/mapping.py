from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts.example_selector import (
    MaxMarginalRelevanceExampleSelector,
    SemanticSimilarityExampleSelector,
)
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import FewShotPromptTemplate

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

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()


def mapping_titles_to_words():
    word_list = ""
    model = OpenAI(
        openai_api_key="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",
        temperature=0,
    )

    # #  templete for mapping words to titles
    # template = """/
    # 你是一个小学语文老师，根据这个题目的要求和内容从以下词库中挑选可能用在作文中的词语。以下是题目要求: {title}。以下是词库: {word_list}。
    # 根据以下步骤来完成任务，任务顺序按照数字从小到大排序：
    # 1：分析作文题目的情感基调.
    # 2：根据上述的分析结果从词库中列举出合适的词语，并输出一个列表，list中的词语是你认为可以用在作文中的词语。如果没有合适的词语则输出一个空的list。{format_instructions}
    # 3：根据挑选的词语，并且将词语造句，可以在一个句子中运用多个词语。造句的时候需要注意句子的语法和逻辑并且需要符合作文的主题和情感基调。句子要适用于作文的开头，中间，或者结尾。列举出所有的句子。{format_instructions}
    # 注意：不需要在前面加上 ”答案：“ 和 ”句子：” 并且每个词语和句子按照字符串的形式存储。
    # """

    # prompt = PromptTemplate(
    #     template=template,
    #     input_variables=["title", "word_list"],
    #     partial_variables={"format_instructions": format_instructions},
    # )

    example_prompt = PromptTemplate(
        input_variables=["title", "word_list"],
        template="Title: {title}\Word_list: {word_list}",
    )

    # These are a lot of examples of a pretend task of creating antonyms.
    examples = [
        {
            "title": "我和爸爸去扫墓",
            "word_list": "缅怀, 祭奠, 祭拜, 祭祀, 祭扫, 扫墓, 扫墓祭奠, 扫墓祭拜, 扫墓祭祀, 扫墓祭扫",
        },
        {
            "title": "春天的故事",
            "word_list": "生机勃勃, 万物复苏, 鸟语花香, 春暖花开, 春意盎然, 春回大地, 春风拂面, 舒适宜人, 春意盎然, 春风拂面, 清风徐徐, 草长莺飞",
        },
        {
            "title": "夏日的荷花",
            "word_list": "烈日炎炎, 酷暑难耐, 酷热难耐, 酷暑难当, 酷热难当, 出淤泥而不染, 荷花盛开, 水面荷花, 荷花开放, 荷花绽放",
        },
        {
            "title": "秋天的落叶",
            "word_list": "落叶纷纷, 落叶满地, 落叶飘零, 落叶飘落, 落叶飘零, 落叶飘落, 落叶纷飞, 落叶纷纷, 落叶满地",
        },
        {
            "title": "一件开心的事",
            "word_list": "开心, 高兴, 欢乐, 欢喜, 欢快, 欢畅, 欢欣, 欢腾, 欢声笑语, 欢天喜地, 欢天喜地, 欢呼雀跃, 欢欣鼓舞",
        },
        {
            "title": "一件难忘的事",
            "word_list": "记忆深刻, 记忆犹新, 刻骨铭心, 欣喜若狂, 悲痛欲绝, 流连忘返, 辗转反侧",
        },
    ]

    example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
        # This is the list of examples available to select from.
        examples,
        # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
        OpenAIEmbeddings(
            openai_api_key="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"
        ),
        # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
        Chroma,
        k=3,
    )

    mmr_prompt = FewShotPromptTemplate(
        # We provide an ExampleSelector instead of examples.
        example_selector=example_selector,
        example_prompt=example_prompt,
        suffix="根据作文题目从词库中列举出可以用在1到6年级作文中的词语,并输出一个列表.\
                注意: 你只能从词库中选择词语，不能从上述的例子中选择词语, 也不能单独生成新的词语, 如果词库中没有符合的词语就返回一个空的列表\
                作文题目: {title}, 词库: {word_list}\n Output: {format_instructions}\
                注意: 你只能从词库中选择词语，不能从上述的例子中选择词语, 也不能单独生成新的词语, 如果词库中没有符合的词语就返回一个空的列表",
        input_variables=["title", "word_list"],
        partial_variables={"format_instructions": format_instructions},
    )

    for word in Word.objects.all():
        word_list += " " + word.word
    print(word_list)

    for title in Title.objects.all():
        _input = mmr_prompt.format(title=title.title, word_list=word_list)
        output = model(_input)
        output = output_parser.parse(output)
        print(title.title, output)
