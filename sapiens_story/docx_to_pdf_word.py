import sys
import os
import win32com.client

def convert_docx_to_pdf(docx_path, pdf_path):
    # 获取绝对路径，COM 组件通常需要绝对路径
    docx_path = os.path.abspath(docx_path)
    pdf_path = os.path.abspath(pdf_path)

    print(f"正在打开 Word 文档: {docx_path}")
    
    word = None
    doc = None
    
    try:
        # 使用 win32com 启动 Word
        word = win32com.client.Dispatch('Word.Application')
        # 后台运行，不显示界面
        word.Visible = False
        
        doc = word.Documents.Open(docx_path)
        print("文档已打开，正在导出为 PDF...")
        
        # wdFormatPDF = 17
        doc.SaveAs(pdf_path, FileFormat=17)
        print(f"成功生成 PDF: {pdf_path}")
        
    except Exception as e:
        print(f"转换失败: {e}")
    finally:
        if doc:
            try:
                doc.Close()
            except:
                pass
        if word:
            try:
                word.Quit()
            except:
                pass

if __name__ == "__main__":
    # 确保依赖包存在: pip install pywin32
    source = "sapiens_story.docx"
    output = "sapiens_story_final.pdf"
    
    if os.path.exists(source):
        convert_docx_to_pdf(source, output)
    else:
        print(f"找不到源导致: {source}")
