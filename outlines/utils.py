import docx


def creat_docx(title, paragraphs: [str]):
    # 创建一个新的 Word 文档
    doc = docx.Document()
    # 向文档中添加段落
    for paragraph in paragraphs:
        doc.add_paragraph(paragraph)

    # 保存文档
    doc.save('output/%s.docx' % title)


def format_chapter_name(chapter_names):
    chapter_names = [item.replace('：', ' ') for item in chapter_names if item != '']
    chapter_name_numbers = [item.split(' ')[0] for item in chapter_names]
    res = chapter_names[len(chapter_names) - 1]
    for i in range(len(chapter_name_numbers) - 1):
        choose = chapter_name_numbers[len(chapter_name_numbers) - 1 - i]
        next_chapter_name = chapter_names[len(chapter_names) - 2 - i]
        last_number = choose.split('.')[-1]
        if last_number == '1':
            res = next_chapter_name + '\n\n' + res
        else:
            break
    return '\n\n' + res + '\n\n'
