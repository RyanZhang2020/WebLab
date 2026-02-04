from xhtml2pdf import pisa
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from xhtml2pdf import pisa
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def convert_html_to_pdf(source_html, output_filename):
    # 1. 明确注册字体到 ReportLab 全局环境
    try:
        # 使用绝对路径以防万一
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, "simhei.ttf")
        
        # 注册名为 "SimHei" 的字体
        pdfmetrics.registerFont(TTFont('SimHei', font_path))
        print(f"DEBUG: 字体已注册: {font_path}")
    except Exception as e:
        print(f"ERROR: 注册字体失败: {e}")

    # 读取HTML文件
    with open(source_html, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 2. 在 CSS 中仅引用字体名称，不使用 @font-face src 加载
    # xhtml2pdf 会在找不到 font-face 定义时查找 ReportLab 的注册字体
    pdf_specific_css = """
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        body {
            font-family: "SimHei", sans-serif;
            background-color: #ffffff;
        }
        h1, h2, h3, h4, h5, h6 {
             font-family: "SimHei", sans-serif;
        }
        div, p, span, li, a {
            font-family: "SimHei", sans-serif;
        }
        .book-container {
            box-shadow: none !important;
            padding: 0 !important;
        }
    </style>
    """
    
    # 将新的CSS插入到 </head> 之前
    html_content = html_content.replace("</head>", f"{pdf_specific_css}</head>")

    # 打开输出文件
    result_file = open(output_filename, "wb")

    # 转换
    pisa_status = pisa.CreatePDF(
        src=html_content,    # HTML 内容
        dest=result_file,    # 输出文件对象
        encoding='utf-8'
        # 不再需要 link_callback 处理字体，因为字体已预注册
    )

    # 关闭文件
    result_file.close()

    # 检查错误
    if pisa_status.err:
        print(f"转换过程中出现了一些错误: {pisa_status.err}")
        return False
    else:
        print(f"成功生成 PDF: {os.path.abspath(output_filename)}")
        return True

if __name__ == "__main__":
    source = "sapiens_story.html"
    output = "sapiens_story.pdf"
    
    if os.path.exists(source):
        convert_html_to_pdf(source, output)
    else:
        print(f"找不到源文件: {source}")
