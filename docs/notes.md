## discord

### circular import

在 3.9 的环境里，直接导入 `from discord.types.message import Attachment` 会导致循环依赖，并且官方也没有相关的
issues： https://github.com/Rapptz/discord.py/issues?q=is%3Aissue+circular

```python
from typing import List, TypedDict, Optional

from discord.types.snowflake import Snowflake
from typing_extensions import NotRequired


class Attachment(TypedDict):
    """
    copied from /midjourney-api-pyT_O9IA-py3.9/lib/python3.9/site-packages/discord/types/message.py    
    """
    id: Snowflake
    filename: str
    size: int
    url: str
    proxy_url: str
    height: NotRequired[Optional[int]]
    width: NotRequired[Optional[int]]
    description: NotRequired[str]
    content_type: NotRequired[str]
    spoiler: NotRequired[bool]
    ephemeral: NotRequired[bool]
```

所以尝试直接copy了一份，但依旧有新的问题， `NotRequired` 首先不能从 `typing`
中导入（3.11才支持，see：`/Applications/PyCharm.app/Contents/plugins/python/helpers/typeshed/stdlib/typing.pyi`
），其次从 `typing_extensions`
中导入后依旧不起作用，会报 field missing 的错误：

```text
attachments -> 0 -> description
  field required (type=value_error.missing)
attachments -> 0 -> ephemeral
  field required (type=value_error.missing)
```

盲猜可能是 python 版本的问题，使用 3.10 试试！
