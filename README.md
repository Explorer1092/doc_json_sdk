# DOC-JSON-SDK （PYTHON）

## 什么是DOC-JSON

![doc-json-model 简要描述](docs/_static/doc-json-model.jpg)

## DOC-JSON-SDK功能特点
- 提供DocMind文档结构化输出的doc-json结果反序列化对象，以及辅助功能函数SDK

## 使用场景

### 使用场景： DocMind 文档智能解析调用
[阿里云官网 文档智能解析调用](https://help.aliyun.com/document_detail/450741.html)


## 集成方式
- 源码安装
```shell
#poetry 准备环境
poetry install
#使用虚拟环境
poetry shell
# 构建
poetry build
twine check $pkg_path
# 上传
twine upload -r aliyun-pypi pkg_path --verbose
```

- python 3.7以上 环境

集团环境
```shell
pip3 install -i http://yum.tbsite.net/aliyun-pypi/simple/ --extra-index-url https://mirrors.aliyun.com/pypi/simple/   --trusted-host=yum.tbsite.net  doc_json_sdk
```
云上环境
```shell
pip install https://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/sdk/doc_json_sdk-1.0.11-py3-none-any.whl
```

> release:
> - 1.0.11 : 当前版本，修复llm_enhancement参数支持，优化代码结构，兼容Python 3.12和macOS环境，修复字体文件包含问题，增强文档解析兼容性，全面增强错误处理
> - 1.0.10 : 已废除，存在其他字段缺失问题
> - 1.0.9 : 已废除，存在styleId缺失问题
> - 1.0.8 : 已废除，存在文档解析兼容性问题
> - 1.0.4 : 已废除，不兼容Python 3.12
> - 1.0.3 : 已废除，请勿使用
> - 1.0.0 : 正式版本
> - 0.1.9.0: 新调用和接口方式
> - 0.1.8.0：修复


- 设置DocMind文档智能解析环境变量

```shell
export ALIBABA_CLOUD_ACCESS_KEY_ID=<access_key_id>
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=<access_key_secret>
#调用服务
```


## 功能方法示例
### 1、获得json数据：
- 调用[文档智能解析 阿里云官网SDK调用](https://help.aliyun.com/document_detail/450738.htm?spm=a2c4g.11186623.0.0.13c61957cjPmNC#f1465a1028tbl)API


### 2、json加载/公有云服务调用
加载对象可以是：
- doc-json 字符串对象
```python
from doc_json_sdk.loader.document_model_loader import DocumentModelLoader
def test_local_json_document():
    file_path = "gongshi.json"
    loader = DocumentModelLoader()
    document = loader.load(doc_json_fp=open(file_path,"r"))
```

- 公有云环境调用（配置ALIBABA_CLOUD_ACCESS_KEY_ID，ALIBABA_CLOUD_ACCESS_KEY_SECRET）
```python
from doc_json_sdk.loader.document_model_loader import DocumentModelLoader
from doc_json_sdk.handler.document_handler import DocumentExtractHandler, DocumentDigitalExtractHandler
from doc_json_sdk.handler.document_parser_handler import DocumentParserHandler, DocumentParserWithCallbackHandler
def test_document_hander():
    file_path = "gongshi.png"
    file_url = None
    # DocumentExtractHandler:文档智能解析，DocumentDigitalExtractHandler:文档电子解析
    loader = DocumentModelLoader(handler=DocumentExtractHandler())
    document = loader.load(file_path=file_path,file_url=file_url)
```

- 公式参数调用/markdown输出/json保存
```python
from doc_json_sdk.loader.document_model_loader import DocumentModelLoader
from doc_json_sdk.handler.document_handler import DocumentExtractHandler
def test_render_formula_markdown():
    file_path = "gongshi.png"
    file_url = None
    handler = DocumentExtractHandler()
    loader = DocumentModelLoader(handler=handler)
    document = loader.load(file_path=file_path,file_url=file_url,
                           formula_enhancement=True,
                           markdown_result=True,
                           save_json_path="/Users/sanchuan/Downloads/docmind.json")
```


- 私有化服务调用（配置PRIVATE_DOCMIND_HOST或显式传入）
```python
from doc_json_sdk.loader.document_model_loader import DocumentModelLoader
from doc_json_sdk.handler.document_private_handler import  PrivateDocumentExtractHandler,PrivateDigitalDocumentExtractHandler
def test_private_document_hander():
    file_path = "gongshi.png"
    file_url = None
    loader = DocumentModelLoader(handler=PrivateDocumentExtractHandler(host="127.0.0.1:7001"))
    document = loader.load(file_path=file_path,file_url=file_url)
```


### 3、功能函数

#### 3.1 对DocumentModel使用处理为markdown

使用内置函数处理为markdown
```python
from doc_json_sdk.loader.document_model_loader import DocumentModelLoader
from doc_json_sdk.handler.document_handler import DocumentExtractHandler, DocumentDigitalExtractHandler
from doc_json_sdk.handler.document_parser_handler import DocumentParserHandler, DocumentParserWithCallbackHandler
from doc_json_sdk.render.document_model_render import DocumentModelRender
def test_render_markdown():
    file_path = "gongshi.png"
    file_url = None
    loader = DocumentModelLoader(handler=DocumentExtractHandler())
    document = loader.load(file_path=file_path,file_url=file_url,markdown_result=True)
    render = DocumentModelRender(document_model=document)
    with open("/Users/sanchuan/Downloads/docmind.md","w") as f:
        f.write(render.render_markdown_result())
```

可视化查看处理效果
```python
from doc_json_sdk.loader.document_model_loader import DocumentModelLoader
from doc_json_sdk.handler.document_handler import DocumentExtractHandler, DocumentDigitalExtractHandler
from doc_json_sdk.handler.document_parser_handler import DocumentParserHandler, DocumentParserWithCallbackHandler
from doc_json_sdk.render.document_model_render import DocumentModelRender
def test_document_hander():
    file_path = "gongshi.png"
    file_url = None
    loader = DocumentModelLoader(handler=DocumentExtractHandler())
    document = loader.load(file_path=file_path,file_url=file_url)
    render = DocumentModelRender(document_model=document)
    render.render_image_result("/Users/sanchuan/Downloads")

```


#### 3.2 对Layout版面块使用
LayoutModel 对象分为内容信息（来源电子解析/OCR）、版面类型信息（来源OCR/NLP）、逻辑关系信息（来源NLP）

![doc-json-layout-model 简要描述](docs/_static/doc-json-layout-model.jpg)

```python
from doc_json_sdk.model.enums.layout_type_enum import LayoutTypeEnum

for layout in document:
    type_enum = layout.get_layout_type_enum()
    if (type_enum == LayoutTypeEnum.Elements.FOOTER or
            type_enum == LayoutTypeEnum.Elements.HEADER or
            type_enum == LayoutTypeEnum.Elements.NOTE):
        #  header and footer notes
        pass
    elif type_enum == LayoutTypeEnum.Elements.IMAGE:
        # image with head_line or split_line
        if layout.type.find("_line")!=-1:
            continue
    elif type_enum == LayoutTypeEnum.Elements.TABLE:
        #table
        pass
    else:
        # paragraph or note(table or figure)
        pass

```


