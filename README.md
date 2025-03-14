# CathD

![Version](https://img.shields.io/badge/version-0.0.5-green.svg?cacheSeconds=2592000)
![ProjectImage](https://raw.githubusercontent.com/ryyos/ryyos/refs/heads/main/images/erine/kawaiii.jpeg)

---

## Features ✨

- **Download Log**: The download feature is accompanied by a log for connection speed and remaining time required.
- **send to s3**: accompanied by a feature to directly send downloaded files to S3 with the s3fs library.
- **easy use**: Simple calls and easy S3FS configuration.

## Requirement ⚙️

- [Python](https://www.python.org/) v3.11.6+
- [s3fs](https://pypi.org/project/s3fs/) v2024.9.0+
- [loguru](https://pypi.org/project/loguru/) v0.7.2+

## Installation 🛠️

```sh
pip install cathd
```

## How To Usage 🤔

#### 1. Basic use

    If you only want to use the download feature and save it locally on your laptop

```python
from cathd import CathD

url = 'https://raw.githubusercontent.com/ryyos/ryyos/refs/heads/main/images/erine/kawaiii.jpeg'
path = 'data/erine_kawai.jpg'

CathD.download(
    url=url,
    path=path,
    save=True,
)
```

#### 2. Send to S3 with an external S3FS connection

    If you want to send the downloaded file to S3 and you want to use an external S3FS connection, you can enter your S3FS connection into the "s3fs_connection" param.

```python
import s3fs

from cathd import CathD

url = 'https://raw.githubusercontent.com/ryyos/ryyos/refs/heads/main/images/erine/kawaiii.jpeg'
path = 'data/erine_kawai.jpg'

client_kwargs = {
    "key": "aws_access_key_id",
    "secret": "aws_secret_access_key",
    "endpoint_url": "endpoint_url",
}

s3 = s3fs.core.S3FileSystem(**client_kwargs)

CathD.download(
    url=url,
    path=path,
    save=True,
    send_s3=True,
    s3fs_connection=s3
)

```

#### 3. Send to S3 with an internal S3FS connection

    If you want to send the downloaded file to the S3 with an internal connection or use the function from CathD to establish a connection to the S3, you can also do it like this

```python

from cathd import CathD

url = 'https://raw.githubusercontent.com/ryyos/ryyos/refs/heads/main/images/erine/kawaiii.jpeg'
path = 'data/erine_kawai.jpg'

CathD.build_s3fs(
    access_key_id="aws_access_key_id",
    secret_access_key="aws_secret_access_key",
    endpoint_url="endpoint_url",
    bucket="bucket"
)

CathD.download(
    url=url,
    path=path,
    save=True,
    send_s3=True,
)

```

## 🚀Structure

```
├── cathd
│   ├── CathD.py
│   ├── __init__.py
│   └── utils.py
├── LICENSE
├── README.md
└── setup.py
```

## Author

👤 **Rio Dwi Saputra**

- Twitter: [@ryyo_cs](https://twitter.com/ryyo_cs)
- Github: [@ryyos](https://github.com/ryyos)
- Instagram: [@ryyo.cs](https://www.instagram.com/ryyo.cs/)
- LinkedIn: [@rio-dwi-saputra-23560b287](https://www.linkedin.com/in/rio-dwi-saputra-23560b287/)

<a href="https://www.linkedin.com/in/rio-dwi-saputra-23560b287/">
  <img align="left" alt="Ryo's LinkedIn" width="24px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/linkedin.svg" />
</a>
<a href="https://www.instagram.com/ryyo.cs/">
  <img align="left" alt="Ryo's Instagram" width="24px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/instagram.svg" />
</a>
