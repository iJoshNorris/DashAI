from datasets import Features
from typing import Dict, Any
from datasets import Dataset
from datasets import ClassLabel, Value
from DashAI.back.types.dashai_value import DashAIValue
from DashAI.back.types.categorical import Categorical
from DashAI.back.types.value_types import Integer, Float, Text, Time, Boolean, Timestamp, Date, Duration, Decimal, Binary

#encode_nested_example debe ser revisado pero en otro codigo




class DashAIFeatures(Features):
    """Wrapper for Hugging Face for representing features."""

    def __init__(self, *args, **kwargs):
        if not args:
            raise TypeError("At least one feature is required")
        self, *args = args
        super(DashAIFeatures, self).__init__(*args, **kwargs)
        self._column_requires_decoding: Dict[str, bool] = {
            col: self._requires_decoding(feature) for col, feature in self.items()
        }
    