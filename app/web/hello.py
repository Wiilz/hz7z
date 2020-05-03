from datetime import datetime
from app.config.enums import TestEnum
from app.extensions.success_response import Success


def hello():
    return Success(data=f"{TestEnum.ok.value}, {TestEnum.ok.zh_value}, {datetime.now()}")
