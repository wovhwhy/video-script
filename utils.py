#这个文件存放和ai大模型交互的代码

#为了对请求进行封装，generate_script函数我们可以通过调用它来得到视频的标题和脚本内容，generate_script函数任务：
#--获取视频的标题
#--调用维基百科api获取相关的信息
#--获得视频的脚本内容


#subject: 视频的主题，如“科幻片”、“动作片”等
#video_length: 视频的长度，单位为秒
#creativity: 视频的创造力，取值范围为0-10，数值越高代表创造力越高
#api_key: 因为我们这里是调用用户的api秘钥，不只是自己的

#为了获得提示模版
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
#WikipediaAPIWrapper内部使用维基百科官方的api进行搜索。并且返回给我们搜索的结果的摘要
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

import os

def generate_script(subject, video_length, creativity, api_key, api_base_url=None):
    """生成视频脚本。

    参数:
    - subject: 视频主题
    - video_length: 视频长度（单位由调用方决定，UI 中为分钟/秒待一致化）
    - creativity: 温度/创造力值（传给模型的 temperature）
    - api_key: 用户提供的 API Key
    - api_base_url: 可选，OpenAI 兼容服务的 base URL（如 https://poloai.top/v1/）。留空则使用官方默认。
    """
    print("传入的 OPENAI_API_KEY 是：", api_key)
    print("传入的 OPENAI_API_BASE_URL：", api_base_url)
    print("当前 Python 环境路径：", os.path.dirname(os.__file__))

#AI获得标题的提示模版,ChatPromptTemplate.from_messages方法接受消息列表作为提示参数
    title_template = ChatPromptTemplate.from_messages([
        ("human", "请为一个关于{subject}的视频生成一个有吸引力的标题，视频长度为{video_length}秒，创造力水平为{creativity}。")
    ])
#AI获得脚本内容的提示模版
    script_template = ChatPromptTemplate.from_messages([
        ("human", """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。视频标题:{title}，视频时长:{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。要求开头抓住眼球，中间提供干货内容，结尾有惊喜。脚本格式为【开头】【中间】【结尾】。你可以参考以下维基百科内容:
        ```{wikipedia_search}```""")
    ])

#参数openai_api_key对入户传入的openai_api_key进行赋值
    # 选择 base_url：优先使用函数参数，其次读取环境变量 OPENAI_API_BASE，最后使用官方默认
    base_url = api_base_url or os.getenv("OPENAI_API_BASE") or "https://api.openai.com/v1/"
    model = ChatOpenAI(api_key=api_key, temperature=creativity, base_url=base_url)

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject, "video_length": video_length, "creativity": creativity}).content

    search = WikipediaAPIWrapper(lang="zh")  
    search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_result}).content

    return search_result, title, script
