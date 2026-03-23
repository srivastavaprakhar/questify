from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.settings import Settings
from llama_index.embeddings.openai.base import BaseEmbedding
from config import DB_PATH, INDEX_PATH
from sqlite_loader import get_sqlite_db
from typing import Optional


class E5SmallV2Embedding(BaseEmbedding):
    model_name: str = "intfloat/e5-small-v2"
    _tokenizer: Optional[AutoTokenizer] = None
    _model: Optional[AutoModel] = None

    def __init__(self, model_name="intfloat/e5-small-v2"):
        super().__init__(model_name=model_name)
        print(f"Loading embedding model: {model_name} on CPU")
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModel.from_pretrained(model_name)
        self._model.eval()  # Evaluation mode (no gradients)

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element is last hidden state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return (token_embeddings * input_mask_expanded).sum(1) / input_mask_expanded.sum(1)

    def _get_embedding(self, text: str) -> np.ndarray:
        encoded_input = self._tokenizer(text, padding=True, truncation=True, return_tensors="pt")
        encoded_input = {k: v.to("cpu") for k, v in encoded_input.items()}
        with torch.no_grad():
            model_output = self._model(**encoded_input)
        embedding = self._mean_pooling(model_output, encoded_input['attention_mask'])
        embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)
        return embedding[0].cpu().numpy()

    def _get_text_embedding(self, text: str) -> np.ndarray:
        return self._get_embedding(text)

    def _get_query_embedding(self, query: str) -> np.ndarray:
        return self._get_embedding(query)

    async def _aget_query_embedding(self, query: str) -> np.ndarray:
        return self._get_embedding(query)


def build_index(db_path=DB_PATH, persist_path=INDEX_PATH):
    print("Building index from SQLite database...")
    documents = get_sqlite_db(db_path)

    # Tune for fewer chunks = faster retrieval
    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    nodes = splitter.get_nodes_from_documents(documents)

    embed_model = E5SmallV2Embedding()
    Settings.embed_model = embed_model

    index = VectorStoreIndex(nodes)
    index.storage_context.persist(persist_dir=persist_path)
    print(f"Index saved to {persist_path}")

    return index

def load_index(persist_path=INDEX_PATH):
    embed_model = E5SmallV2Embedding()
    Settings.embed_model = embed_model
    return load_index_from_storage(StorageContext.from_defaults(persist_dir=persist_path))
