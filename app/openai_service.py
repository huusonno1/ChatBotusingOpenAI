from openai import OpenAI
import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime

load_dotenv()


class RAGService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.db_path = "./chroma_db"

        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)

        self.chroma_client = chromadb.PersistentClient(path=self.db_path)
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_name="text-embedding-ada-002"
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name="product_knowledge_base",
            embedding_function=self.embedding_function,
            metadata={"description": "Product information database"}
        )

        self.conversation_history = []
        self.max_history = 3

    def add_documents(self, documents: list[str], metadata: list[dict] = None):
        try:
            ids = [f"doc_{datetime.now().timestamp()}_{i}" for i in range(len(documents))]

            if metadata is None:
                metadata = [
                    {
                        "timestamp": datetime.now().isoformat(),
                        "source": "manual_input"
                    } for _ in documents
                ]

            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadata
            )

            print(f"Added {len(documents)} documents to the knowledge base")
            return True

        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            return False

    async def get_relevant_context(self, query: str, n_results: int = 3) -> str:
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )

            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0]

            context_parts = []
            for doc, meta, dist in zip(documents, metadatas, distances):
                relevance_score = 1 - (dist / max(results['distances'][0]))
                context_parts.append(f"[Relevance: {relevance_score:.2f}] {doc}")

            return "\n\n".join(context_parts)

        except Exception as e:
            print(f"Error getting context: {str(e)}")
            return ""

    def _update_conversation_history(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

    async def get_openai_response(self, message: str) -> str:
        try:
            context = await self.get_relevant_context(message)

            if not context:
                return "Tôi không có đủ thông tin để trả lời câu hỏi này của bạn."

            # Cập nhật lịch sử với tin nhắn của user
            self._update_conversation_history("user", message)

            system_prompt = f"""You are a helpful bilingual (Vietnamese/English) shopping assistant. Answer questions based on the context and conversation history below.
            If you cannot answer the question based on the context, say "Tôi không có đủ thông tin để trả lời câu hỏi đó."

            Be natural and conversational in your responses. If prices are mentioned, always include them.
            When the user uses pronouns in Vietnamese (nó, cái này, cái đó, etc.) or English (it, this, that), refer to the conversation history to understand what they're referring to.

            Always respond in Vietnamese.

            Context:
            {context}
            """

            # Tạo messages array với system prompt và lịch sử hội thoại
            messages = [
                {"role": "system", "content": system_prompt},
                *self.conversation_history
            ]

            # Gọi OpenAI API
            completion = self.client.chat.completions.create(
                model="gpt-4o",  # Sửa lỗi chính tả từ gpt-4o
                messages=messages,
                temperature=0.5
            )

            response = completion.choices[0].message.content

            # Cập nhật lịch sử với câu trả lời của assistant
            self._update_conversation_history("assistant", response)

            return response

        except Exception as e:
            return f"Lỗi: {str(e)}"

    def clear_conversation_history(self):
        """Xóa lịch sử hội thoại"""
        self.conversation_history = []