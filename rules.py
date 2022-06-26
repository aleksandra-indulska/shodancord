from typing import List

from pydantic import BaseModel


class MessageRule(BaseModel):
    regex_pattern: str
    response: str


class MessageRules(BaseModel):
    __root__: List[MessageRule]


if __name__ == '__main__':
    with open('rules.schema.json', 'w') as file:
        file.write(MessageRules.schema_json())
