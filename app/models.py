import datetime
from typing import List
from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime

class SalesOrder(BaseModel):
    id: UUID = uuid4()
    invoice_number: str | None
    date_created: datetime | str = datetime.now()

    def __getitem__(self, item):
        return getattr(self, item)

    model_config = {
        "json_schema_extra" : {
            "examples" : [
                {
                    "id" : "c83282f3-1f55-4206-88f1-e0de75565300",
                    "invoice_number" : "1",
                    "date_created" : "2024-07-12T10:56:44.697700"
                }
            ]
        }
    }
