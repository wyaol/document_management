import random
import shutil
import time
import re
from enum import Enum
from .utils import creat_docx, format_chapter_name
import os

outlines_ready = []
outlines_progressing = []
outlines_done = []
connectors = []
count = 0

with open('input/thank.txt', 'r') as fp:
    thanks = fp.read().split("\n\n")


class OutlineStatus(Enum):
    WAIT_FOR_START = 0
    PROGRESSING = 1
    DONE = 2


class ChatGPTConnector:

    def __init__(self, conversation_id: str, paragraphs: [], title: str):
        self.conversation_id = conversation_id
        self.paragraphs = paragraphs
        self.title = title

    def add_title(self, title):
        self.title = title


class Outline:

    def __init__(self, id: int, content: str):
        self.id = id
        self.content = content

    def get_simple_content(self):
        return {
            'id': self.id,
            'content:': self.content[:100] + '...'
        }


def add_one_outline(outline_content: str):
    outlines_ready.append(Outline(int(time.time()), outline_content))
    return {
        'ready': [item.get_simple_content() for item in outlines_ready],
        'progressing': [item.get_simple_content() for item in outlines_progressing],
        'done': [item.get_simple_content() for item in outlines_done]
    }


def get_outlines() -> [Outline]:
    return {
        'ready': [item.get_simple_content() for item in outlines_ready],
        'progressing': [item.get_simple_content() for item in outlines_progressing],
        'done': [item.get_simple_content() for item in outlines_done]
    }


def pop_one_outline():
    if len(outlines_ready) == 0:
        return None
    outline = outlines_ready.pop()
    outlines_progressing.append(outline)
    return outline


def add_one_paragraph(conversation_id, paragraph):
    for connector in connectors:
        if connector.conversation_id == conversation_id:
            connector.paragraphs.append(paragraph)
    connectors.append(ChatGPTConnector(conversation_id, [paragraph], conversation_id))


def add_title(conversation_id, title):
    for connector in connectors:
        if connector.conversation_id == conversation_id:
            connector.add_title(title)
    connectors.append(ChatGPTConnector(conversation_id, [], title))


def finish_one_connector(conversation_id):
    for connector in connectors:
        if connector.conversation_id == conversation_id:
            connectors.pop(connectors.index(connector))
        creat_docx(connector.title, connector.paragraphs)


def get_thank():
    global thanks
    return random.choice(thanks)


def add_articles(paragraphs):
    # 判断回答里是否包含章节，包含则删除重复的章节
    paragraphs = [re.sub(r'\d\.\d.*?\n\n', '', item) for item in paragraphs]
    paragraphs = [re.sub(r'第.章\n\n', '', item) for item in paragraphs]

    title = None
    for i in range(len(paragraphs)):
        if i % 2 == 0:  # ji shu
            paragraphs[i + 1] = paragraphs[i + 1].replace('\n\n', '\n')
            match_obj = re.match(r'.*?我的第一个请求是(.*?)-(.*?)-(.*?)-(.*?)-?，.*?', paragraphs[i], re.S)
            if not match_obj:
                match_obj = re.match(r'.*?我的第一个请求是(.*?)-(.*?)-(.*?)，.*?', paragraphs[i], re.S)
            if not match_obj:
                match_obj = re.match(r'.*?我的第一个请求是(.*?)-(.*?)，.*?', paragraphs[i], re.S)
            if not match_obj:
                match_obj = re.match(r'.*?我的第一个请求是(.*?)，.*?', paragraphs[i], re.S)
            if not match_obj:
                match_obj = re.match(r'.*?我的第一个请求是(.*?)，.*?', paragraphs[i], re.S)
            if not match_obj:
                match_obj = re.match(r'.*?-(.*?)-(.*?)-(.*?)-(.*?)，.*?', paragraphs[i], re.S)
            if not match_obj:
                match_obj = re.match(r'.*?-(.*?)-(.*?)-(.*?)，.*?', paragraphs[i], re.S)
            if not match_obj:
                match_obj = re.match(r'.*?-(.*?)-(.*?)，.*?', paragraphs[i], re.S)
            if not match_obj:
                match_obj = re.match(r'.*?-(.*?)，.*?', paragraphs[i], re.S)
            if not match_obj:
                match_obj = re.match(r'.*?-(.*?)，.*?', paragraphs[i], re.S)

            if match_obj:
                title = title if title is not None else match_obj.groups()[0]
                paragraphs[i + 1] = format_chapter_name(match_obj.groups()[1:]) + paragraphs[i + 1]
            else:
                print([paragraphs[i]])

    global count
    count += 1
    title = title if title is not None else str(count)
    paragraphs = [paragraphs[i] for i in range(len(paragraphs)) if i % 2 != 0]

    # 调正章节顺序
    if '摘要' in paragraphs[-1] and '本文框架' in paragraphs[-2] and '研究方法' in paragraphs[-3] and '国内外研究现状' in paragraphs[
        -4] and '研究意义' in paragraphs[-5]:
        abstract = paragraphs[-1].replace('（包含关键词）', '')
        paragraphs = [abstract] + paragraphs[-5: -1] + paragraphs[:-5]

    # 增加致谢
    paragraphs.append('\n\n' + get_thank())

    creat_docx(title, paragraphs)


def delete_documents():
    files = os.listdir('output')
    for file in files:
        # os.remove('output/%s' % file)
        shutil.move('output/%s' % file, 'backup/%s' % file)


def revert_outline(document_id):
    for item in outlines_progressing:
        if str(item.id) == str(document_id):
            outlines_progressing.remove(item)
            outlines_ready.append(item)
    for item in outlines_done:
        if str(item.id) == str(document_id):
            outlines_done.remove(item)
            outlines_ready.append(item)
    return {
        'ready': [item.get_simple_content() for item in outlines_ready],
        'progressing': [item.get_simple_content() for item in outlines_progressing],
        'done': [item.get_simple_content() for item in outlines_done]
    }


def delete_outlines():
    global outlines_ready
    outlines_ready = []
    global outlines_progressing
    outlines_progressing = []
    global outlines_done
    outlines_done = []
    return {
        'ready': [item.get_simple_content() for item in outlines_ready],
        'progressing': [item.get_simple_content() for item in outlines_progressing],
        'done': [item.get_simple_content() for item in outlines_done]
    }
