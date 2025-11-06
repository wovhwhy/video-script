import streamlit as st
from utils import generate_script

st.title("视频脚本生成器")
#加侧边栏
with st.sidebar:
    #设置type="password"，则用户输入的内容不会直接显示出来，会比较安全，text_input还会返回用户当前的输入
    openai_api_key =   st.text_input("请输入OpenAI API秘钥:", type="password")
    openai_api_base = st.text_input("OpenAI API Base URL (留空使用官方)", value="", help="例如：https://poloai.top/v1/")
    st.markdown("[获取OpenAI API秘钥](https://platform.openai.com/account/api-keys)")

suject=st.text_input("请输入视频的主题")
video_length=st.number_input("请输入视频的大致时长", min_value=0.1,step=0.1)
creativity=st.slider("请选择视频脚本的创造力(数字小说明更严谨，数字大说明更多样)",min_value=0.0, max_value=1.0, value=0.2,step=0.1)

#用户没有点击返回false，点击了返回true
submit=st.button("生成脚本")
#确认用户提供了api秘钥和字体等信息
if submit and not openai_api_key:
    #展示提示信息用st.info
    st.info("请输入你的OpenAI API秘钥")
    st.stop()#执行到这里后，后面的代码不会展示了
if submit and not suject:
    st.info("请输入视频的主题")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("视频长度需要大于或等于0.1")
    st.stop()
if submit:
    #调用generate_script函数生成脚本,返回的是search_result, title, script
    #但是generate_script生成式需要时间的，不会立刻返回，给它一个加载
    with st.spinner(("AI正在思考中，请稍等...")):
        # 将用户填写的 base url 传入（若为空则由 utils 使用默认官方地址）
        search_result, title, script = generate_script(suject, video_length, creativity, openai_api_key, openai_api_base or None)
    st.success("视频脚本生成成功！")
    #把获得的内容展示出来
    st.subheader("标题：")
    st.write(title)
    st.subheader("视频脚本：")
    st.write(script)
    with st.expander("维基百科搜索结果"):
        st.info(search_result)
                     
