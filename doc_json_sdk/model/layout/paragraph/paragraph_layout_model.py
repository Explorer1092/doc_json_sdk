from typing import List

from doc_json_sdk.model.layout.layout_model import LayoutModel
from doc_json_sdk.model.layout.paragraph.block import Block
from doc_json_sdk.model.logic.kv_model import KvModel


class ParagraphLayoutModel(LayoutModel):
    """

    段落版面

    """

    blocks: List[Block]
    """字块信息列表"""

    line_height: int
    """行平均高度"""

    first_lines_chars: int
    """文字首行缩进"""

    kv = List[KvModel]
    """段落Kv"""

    def __init__(self, paragraph_layout_model: dict):
        super().__init__(paragraph_layout_model)
        self.blocks = []
        self.line_height = paragraph_layout_model.get('lineHeight', 20)
        self.first_lines_chars = paragraph_layout_model.get('firstLinesChars', 0)  # 修正变量名和赋值
        if 'blocks' not in paragraph_layout_model:
            return
        for i in paragraph_layout_model.get('blocks', []):
            self.blocks.append(Block(i))

    def get_blocks(self) -> []:
        return self.blocks

    def set_kv(self, kv: []):
        self.kv = kv

    def get_line_height(self):
        return self.line_height
        pass

    def get_first_line_chars(self):
        return self.first_lines_chars  # 修正变量名
        pass
