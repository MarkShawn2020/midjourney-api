import re

import pytest
from pydantic import ValidationError

from src.ds.discord import Attachment, ICallback, TriggerStatus


def test_typed_dict():
    data = Attachment(
        id='',
        filename='',
        size=0,
        url='',
        proxy_url=''
    )
    print({"data": data})
    
    data = Attachment(
        id='',
        filename='',
        size=0,
        url='',
    )
    print({"data": data})
    
    callback = ICallback(
        type='',
        id=0,
        content='',
        attachments=[],
        trigger_id=0,
        trigger_status=TriggerStatus.message,
    )
    print({"callback": callback})
    
    # 不能在 pydantic 中混用 带 NotRequired 的 typeddict，目前 pydantic v1 不支持
    # https://github.com/pydantic/pydantic/issues/3859#issuecomment-1139368707
    with pytest.raises(ValidationError, match=re.escape("""7 validation errors for ICallback
attachments -> 0 -> proxy_url
  field required (type=value_error.missing)
attachments -> 0 -> height
  field required (type=value_error.missing)
attachments -> 0 -> width
  field required (type=value_error.missing)
attachments -> 0 -> description
  field required (type=value_error.missing)
attachments -> 0 -> content_type
  field required (type=value_error.missing)
attachments -> 0 -> spoiler
  field required (type=value_error.missing)
attachments -> 0 -> ephemeral
  field required (type=value_error.missing)""")) as e:
        callback = ICallback(
            type='',
            id=0,
            content='',
            attachments=[data],
            trigger_id=0,
            trigger_status=TriggerStatus.message,
        )
        print({"callback": callback})
