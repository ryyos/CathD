import requests
import s3fs

from tqdm import tqdm
from loguru import logger
from time import perf_counter
from cathd.utils import Help

class CathD:
    
    __s3fs_connection = None
    __bucket = None
    
    @classmethod
    def build_s3fs(cls, access_key_id: str, secret_access_key: str, endpoint_url: str, bucket: str) -> any:
        if not cls.__s3fs_connection:
            cls.__s3fs_connection = s3fs.core.S3FileSystem(**{
                "key": access_key_id,
                "secret": secret_access_key,
                "endpoint_url": endpoint_url
            })
        cls.__bucket = bucket
        return cls.__s3fs_connection
        ...
    
    @classmethod
    def download(cls, url: str, path: str = None, retry: int = 10, send_s3: bool = False, save: bool = False, s3fs_connection: any = None, bucket: str = None, **kwargs) -> bytes:
        if path: Help.create_dir(paths='/'.join(path.split('/')[:-1]))
        headers = kwargs.get("header", {})
        def _save(body: any, destination: str) -> str:
            try:
                filepath: str = f"{destination}"
                filename: str = Help.name_file(filepath)
                with open(filepath, "wb") as f:
                    for chunk in body:
                        if chunk:
                            f.write(chunk)
                logger.info(f"File {filename} saved successfully.")
                return filepath
            except Exception as e:
                logger.error(f"Error saved file: {str(e)}")
                return ""
            ...
            
        def _upload(body: any, destination: str) -> str:
            try:
                __bucket: str = cls.__bucket if cls.__bucket else bucket
                connection = cls.__s3fs_connection if cls.__s3fs_connection else s3fs_connection
                
                if (not __bucket) and s3fs_connection:
                    raise Exception('please enter the bucket if you using external s3fs connection')
                if (not connection) and bucket:
                    raise Exception('what would you do with that bucket if you didn"t have an s3fs connection?')
                if (not connection) and send_s3:
                    raise Exception('you want to send to s3 but there is no s3fs connection that you provide?')
                
                filepath: str = f"{__bucket}/{destination}"
                filename: str = Help.name_file(filepath)
                
                with connection.open(filepath, "wb") as f:
                    for chunk in body:
                        if chunk:
                            f.write(chunk)
                logger.info(f"File {filename} uploaded to S3 successfully.")
                return filepath
            except Exception as e:
                logger.error(f"Error uploading file to S3: {str(e)}")
                return ""
            
        start = perf_counter()
        if path:
            filename: str = Help.name_file(path)
            logger.info(f"PROCESS DOWNLOAD [ {Help.name_file(path)} ] :: START [ {Help.now()} ]")
        else:
            logger.info(f"PROCESS DOWNLOAD :: START [ {Help.now()} ]")
        chunks = list()
        downloaded = 0
        
        for index in range(retry):
            try:
                header = {'Range': f'bytes={downloaded}-'}
                headers.update(header)
                with requests.get(url, headers=headers, stream=True, timeout=600, **kwargs.get("requests", {})) as r:
                    total_size = downloaded + int(r.headers.get('Content-Length', 0))
                    r.raise_for_status()
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc='DOWNLOAD', ncols=100, initial=downloaded) as pbar:
                        for chunk in r.iter_content(chunk_size=262144):
                            if chunk and chunk not in chunks:
                                chunks.append(chunk)
                                downloaded += len(chunk)
                                pbar.update(len(chunk))
                                
                    if downloaded < total_size:
                        raise Exception('Download has not yet been completed')
                    if save:
                        if not path: raise Exception('please insert path!')
                        _save(chunks, path)
                    if send_s3:
                        if not path: raise Exception('please insert path!')
                        _upload(chunks, path)
                        
                    return b''.join(chunks)
            except Exception as err:
                if index+1 == retry: raise Exception(err)
                logger.error(f'MESSAGE [ {err} ] TRY AGAIN [ {index} ]')
        logger.info(f"DOWNLOAD [ {filename} ] :: TIME REQUIRED [ {'{:.2f}'.format(perf_counter() - start)} ]")
    ...