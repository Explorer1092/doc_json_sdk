import json
import os
from typing import Dict
from typing import Callable

from alibabacloud_credentials.client import Client as CredClient

from alibabacloud_docmind_api20220711 import models as docmind_api20220711_models
from alibabacloud_docmind_api20220711.client import Client as docmind_api20220711Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from doc_json_sdk.utils.log_util import log
from doc_json_sdk.handler.document_handler_interface import DocumentHandler


class DocumentExtractHandler(DocumentHandler):
    """
    
    文档提取处理
    
    -------------------
    
    access_key_id [optional] 阿里云开通DocMind服务AK
    access_key_secret [optional] 阿里云开通DocMind服务SK
    
    """

    def __init__(self):
        self._access_key_id = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID')
        self._access_key_secret = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
        self._cred = CredClient()
        self._DOCMIND_HOST = os.environ.get('DOCMIND_HOST', f'docmind-api.cn-hangzhou.aliyuncs.com')
        log.info("ask host %s", self._DOCMIND_HOST)
        pass

    def stream_get_document_json(self, file_path, file_url: str = None, **kwargs):
        pass

    def get_document_json(self, file_path: str = None, file_url: str = None, **kwargs) -> Dict:
        """
        获取doc json信息

        ----------------------------
            :param file_path: 本地文件路径
        :return: doc-json
        """
        if file_url is not None:
            response = self._submit_url(file_url, **kwargs)
        elif file_path is not None:
            response = self._submit_file(file_path, **kwargs)
        else:
            raise ValueError("file_url and file_path is null")
        if response.body.data.id is None:
            raise Exception(response.body)
        print(response.body.data.id)
        while 1:
            res = self._query(response.body.data.id,**kwargs)
            if res:
                if res.completed:
                    break
        json_dict = json.loads(json.dumps(eval(str(res))))
        return json_dict

    def get_document_json_by_request_id(self, request_id: str, **kwargs):
        return self._query(request_id,**kwargs)

    def _submit_file(self, file_path: str, **kwargs):
        config = open_api_models.Config(
            access_key_id=self._access_key_id if self._access_key_id is not None else self._cred.get_access_key_id(),
            access_key_secret=self._access_key_secret if self._access_key_secret is not None else self._cred.get_access_key_secret(),
            connect_timeout=60000,
            read_timeout=60000,
            endpoint=self._DOCMIND_HOST,
            http_proxy=kwargs["http_proxy"] if "http_proxy" in kwargs else None,
            https_proxy=kwargs["https_proxy"] if "https_proxy" in kwargs else None
        )
        client = docmind_api20220711Client(config)
        formula_enhancement = True if "formula_enhancement" in kwargs and kwargs["formula_enhancement"] else False
        # llm_enhancement参数不被SubmitDocStructureJobRequest支持，已移除
        structure_type = kwargs["structure_type"] if "structure_type" in kwargs and kwargs[
            "structure_type"] else "doctree"
        request = docmind_api20220711_models.SubmitDocStructureJobAdvanceRequest(
            file_url_object=open(file_path, "rb"),
            file_name=file_path.rsplit("/", 1)[-1],
            file_name_extension=file_path.rsplit(".", 1)[-1],
            formula_enhancement=formula_enhancement,
            structure_type=structure_type
        )
        runtime = util_models.RuntimeOptions()
        runtime.read_timeout = 60000
        runtime.connect_timeout = 60000
        if "http_proxy" in kwargs:
            runtime.https_proxy = kwargs["http_proxy"]
        if "http_proxys" in kwargs:
            runtime.https_proxys = kwargs["http_proxys"]
        try:
            response = client.submit_doc_structure_job_advance(request, runtime)
            log.info("doc_structure_job_advance with %s", response.body)
            return response
        except Exception as error:
            log.error(str(error))
            UtilClient.assert_as_string(str(error))
            raise error

    def _submit_url(self, file_url: str, **kwargs):
        config = open_api_models.Config(
            access_key_id=self._access_key_id if self._access_key_id is not None else self._cred.get_access_key_id(),
            access_key_secret=self._access_key_secret if self._access_key_secret is not None else self._cred.get_access_key_secret(),
            connect_timeout=60000,
            read_timeout=60000,
            endpoint=self._DOCMIND_HOST,
            http_proxy=kwargs["http_proxy"] if "http_proxy" in kwargs else None,
            https_proxy=kwargs["https_proxy"] if "https_proxy" in kwargs else None
        )
        client = docmind_api20220711Client(config)
        file_path = file_url[:file_url.rfind("?")] if (file_url.rfind("?") != -1) else file_url[file_url.rfind("/"):]
        formula_enhancement = True if "formula_enhancement" in kwargs and kwargs["formula_enhancement"] else False
        # llm_enhancement参数不被SubmitDocStructureJobRequest支持，已移除
        structure_type = kwargs["structure_type"] if "structure_type" in kwargs and kwargs[
            "structure_type"] else "doctree"
        request = docmind_api20220711_models.SubmitDocStructureJobRequest(
            file_url=file_url,
            file_name=file_path.rsplit("/", 1)[-1],
            formula_enhancement=formula_enhancement,
            structure_type=structure_type
        )
        try:
            response = client.submit_doc_structure_job(request)
            log.info("doc_structure_job with %s", response.body)
            return response
        except Exception as error:
            log.error(str(error))
            UtilClient.assert_as_string(str(error))
            raise error

    def _query(self, response_id: str, **kwargs):
        config = open_api_models.Config(
            access_key_id=self._access_key_id if self._access_key_id is not None else self._cred.get_access_key_id(),
            access_key_secret=self._access_key_secret if self._access_key_secret is not None else self._cred.get_access_key_secret(),
            connect_timeout=60000,
            read_timeout=60000,
            endpoint=self._DOCMIND_HOST,
            http_proxy=kwargs["http_proxy"] if "http_proxy" in kwargs else None,
            https_proxy=kwargs["https_proxy"] if "https_proxy" in kwargs else None
        )
        client = docmind_api20220711Client(config)
        try:
            reveal_markdown = True if "reveal_markdown" in kwargs and kwargs["reveal_markdown"] else False
            use_url_response_body = True if "use_url_response_body" in kwargs and kwargs["use_url_response_body"] else False
            request = docmind_api20220711_models.GetDocStructureResultRequest(
                id=response_id,
                reveal_markdown=reveal_markdown,
                use_url_response_body=use_url_response_body
            )
            response = client.get_doc_structure_result(request)
            return response.body
        except Exception as error:
            log.error(str(error))
            UtilClient.assert_as_string(str(error))
            raise error


class DocumentDigitalExtractHandler(DocumentHandler):
    """
    电子解析结果获取
    """

    def __init__(self):
        self._access_key_id = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID')
        self._access_key_secret = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
        self._cred = CredClient()
        self._DOCMIND_HOST = os.environ.get('DOCMIND_HOST', f'docmind-api.cn-hangzhou.aliyuncs.com')
        log.info("ask host %s", self._DOCMIND_HOST)
        pass

    def get_document_json(self, file_path: str = None, file_url: str = None, **kwargs) -> Dict:
        config = open_api_models.Config(
            access_key_id=self._access_key_id if self._access_key_id is not None else self._cred.get_access_key_id(),
            access_key_secret=self._access_key_secret if self._access_key_secret is not None else self._cred.get_access_key_secret(),
            connect_timeout=60000,
            read_timeout=60000,
            endpoint=self._DOCMIND_HOST,
            http_proxy=kwargs["http_proxy"] if "http_proxy" in kwargs else None,
            https_proxy=kwargs["https_proxy"] if "https_proxy" in kwargs else None
        )
        client = docmind_api20220711Client(config)
        reveal_markdown = True if "reveal_markdown" in kwargs and kwargs["reveal_markdown"] else False
        use_url_response_body = True if "use_url_response_body" in kwargs and kwargs["use_url_response_body"] else False
        if file_url is not None:
            if file_path is None:
                file_path = file_url[:file_url.rfind("?")] if file_url.find("?") != -1 else file_url
                file_path = file_path[file_path.rfind("/") + 1:]
            request = docmind_api20220711_models.SubmitDigitalDocStructureJobRequest(
                file_url=file_url,
                file_name=file_path.rsplit("/", 1)[-1],
                file_name_extension=file_path.rsplit(".", 1)[-1],
                reveal_markdown=reveal_markdown,
                use_url_response_body=use_url_response_body
            )
            response = client.submit_digital_doc_structure_job(request)
        elif file_path is not None:
            request = docmind_api20220711_models.SubmitDigitalDocStructureJobAdvanceRequest(
                file_url_object=open(file_path, "rb"),
                file_name=file_path.rsplit("/", 1)[-1],
                file_name_extension=file_path.rsplit(".", 1)[-1],
                reveal_markdown=reveal_markdown,
                use_url_response_body=use_url_response_body
            )
            runtime = util_models.RuntimeOptions()
            runtime.read_timeout = 60000
            runtime.connect_timeout = 60000
            if "http_proxy" in kwargs:
                runtime.https_proxy = kwargs["http_proxy"]
            if "http_proxys" in kwargs:
                runtime.https_proxys = kwargs["http_proxys"]
            response = client.submit_digital_doc_structure_job_advance(request, runtime)
        else:
            raise ValueError("file_url and file_path is null")
        if response is None:
            raise EnvironmentError("response null")
        if response.body.id==None:
            raise Exception(response.body)
        try:
            log.info("digital_doc_structure_job with %s", response.body.id)
            print(response.body.id)
            return json.loads(json.dumps(eval(str(response.body))))
        except Exception as error:
            log.error(str(error))
            UtilClient.assert_as_string(str(error))
            raise error

    def get_document_json_by_request_id(self, request_id: str):
        raise NameError("digital without method get_document_json_by_request_id")