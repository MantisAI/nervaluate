from abc import ABC, abstractmethod
from typing import List, Dict, Any

from .entities import Entity


class DataLoader(ABC):
    """Abstract base class for data loaders."""

    @abstractmethod
    def load(self, data: Any) -> List[List[Entity]]:
        """Load data into a list of entity lists."""


class ConllLoader(DataLoader):
    """Loader for CoNLL format data."""

    def load(self, data: str) -> List[List[Entity]]:  # pylint: disable=too-many-branches
        """Load CoNLL format data into a list of Entity lists."""
        if not isinstance(data, str):
            raise ValueError("ConllLoader expects string input")

        if not data:
            return []

        result: List[List[Entity]] = []
        # Strip trailing whitespace and newlines to avoid empty documents
        documents = data.rstrip().split("\n\n")

        for doc in documents:
            if not doc.strip():
                result.append([])
                continue

            current_doc = []
            start_offset = None
            end_offset = None
            ent_type = None
            has_entities = False

            for offset, line in enumerate(doc.split("\n")):
                if not line.strip():
                    continue

                parts = line.split("\t")
                if len(parts) < 2:
                    raise ValueError(f"Invalid CoNLL format: line '{line}' does not contain a tab separator")

                token_tag = parts[1]

                if token_tag == "O":
                    if ent_type is not None and start_offset is not None:
                        end_offset = offset - 1
                        if isinstance(start_offset, int) and isinstance(end_offset, int):
                            current_doc.append(Entity(label=ent_type, start=start_offset, end=end_offset))
                        start_offset = None
                        end_offset = None
                        ent_type = None

                elif ent_type is None:
                    if not (token_tag.startswith("B-") or token_tag.startswith("I-")):
                        raise ValueError(f"Invalid tag format: {token_tag}")
                    ent_type = token_tag[2:]  # Remove B- or I- prefix
                    start_offset = offset
                    has_entities = True

                elif ent_type != token_tag[2:] or (ent_type == token_tag[2:] and token_tag[:1] == "B"):
                    end_offset = offset - 1
                    if isinstance(start_offset, int) and isinstance(end_offset, int):
                        current_doc.append(Entity(label=ent_type, start=start_offset, end=end_offset))

                    # start of a new entity
                    if not (token_tag.startswith("B-") or token_tag.startswith("I-")):
                        raise ValueError(f"Invalid tag format: {token_tag}")
                    ent_type = token_tag[2:]
                    start_offset = offset
                    end_offset = None
                    has_entities = True

            # Catches an entity that goes up until the last token
            if ent_type is not None and start_offset is not None and end_offset is None:
                if isinstance(start_offset, int):
                    current_doc.append(Entity(label=ent_type, start=start_offset, end=len(doc.split("\n")) - 1))
                has_entities = True

            result.append(current_doc if has_entities else [])

        return result


class ListLoader(DataLoader):
    """Loader for list format data."""

    def load(self, data: List[List[str]]) -> List[List[Entity]]:  # pylint: disable=too-many-branches
        """Load list format data into a list of entity lists."""
        if not isinstance(data, list):
            raise ValueError("ListLoader expects list input")

        if not data:
            return []

        result = []

        for doc in data:
            if not isinstance(doc, list):
                raise ValueError("Each document must be a list of tags")

            current_doc = []
            start_offset = None
            end_offset = None
            ent_type = None

            for offset, token_tag in enumerate(doc):
                if not isinstance(token_tag, str):
                    raise ValueError(f"Invalid tag type: {type(token_tag)}")

                if token_tag == "O":
                    if ent_type is not None and start_offset is not None:
                        end_offset = offset - 1
                        if isinstance(start_offset, int) and isinstance(end_offset, int):
                            current_doc.append(Entity(label=ent_type, start=start_offset, end=end_offset))
                        start_offset = None
                        end_offset = None
                        ent_type = None

                elif ent_type is None:
                    if not (token_tag.startswith("B-") or token_tag.startswith("I-")):
                        raise ValueError(f"Invalid tag format: {token_tag}")
                    ent_type = token_tag[2:]  # Remove B- or I- prefix
                    start_offset = offset

                elif ent_type != token_tag[2:] or (ent_type == token_tag[2:] and token_tag[:1] == "B"):
                    end_offset = offset - 1
                    if isinstance(start_offset, int) and isinstance(end_offset, int):
                        current_doc.append(Entity(label=ent_type, start=start_offset, end=end_offset))

                    # start of a new entity
                    if not (token_tag.startswith("B-") or token_tag.startswith("I-")):
                        raise ValueError(f"Invalid tag format: {token_tag}")
                    ent_type = token_tag[2:]
                    start_offset = offset
                    end_offset = None

            # Catches an entity that goes up until the last token
            if ent_type is not None and start_offset is not None and end_offset is None:
                if isinstance(start_offset, int):
                    current_doc.append(Entity(label=ent_type, start=start_offset, end=len(doc) - 1))

            result.append(current_doc)

        return result


class DictLoader(DataLoader):
    """Loader for dictionary format data."""

    def load(self, data: List[List[Dict[str, Any]]]) -> List[List[Entity]]:
        """Load dictionary format data into a list of entity lists."""
        if not isinstance(data, list):
            raise ValueError("DictLoader expects list input")

        if not data:
            return []

        result = []

        for doc in data:
            if not isinstance(doc, list):
                raise ValueError("Each document must be a list of entity dictionaries")

            current_doc = []
            for entity in doc:
                if not isinstance(entity, dict):
                    raise ValueError(f"Invalid entity type: {type(entity)}")

                required_keys = {"label", "start", "end"}
                if not all(key in entity for key in required_keys):
                    raise ValueError(f"Entity missing required keys: {required_keys}")

                if not isinstance(entity["label"], str):
                    raise ValueError("Entity label must be a string")

                if not isinstance(entity["start"], int) or not isinstance(entity["end"], int):
                    raise ValueError("Entity start and end must be integers")

                current_doc.append(Entity(label=entity["label"], start=entity["start"], end=entity["end"]))
            result.append(current_doc)

        return result
