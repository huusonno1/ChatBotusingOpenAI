from openai import OpenAI
import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
from typing import Dict, List, Any, Optional

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
        self.max_history = 5

    def add_documents(self, documents: List[str], metadata: Optional[List[Dict[str, Any]]] = None) -> bool:
        """
        Thêm documents và metadata vào ChromaDB
        """
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

    async def get_relevant_context(self, query: str, n_results: int = 5) -> str:
        """
        Lấy context liên quan từ ChromaDB dựa trên query
        """
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
                metadata_str = "\n".join([
                    f"- {k.title()}: {v}"
                    for k, v in meta.items()
                    if k not in ['timestamp', 'source']
                ])
                context_parts.append(
                    f"[Độ liên quan: {relevance_score:.2f}]\n"
                    f"Thông tin: {doc}\n"
                    f"Chi tiết:\n{metadata_str}"
                )

            return "\n\n".join(context_parts)

        except Exception as e:
            print(f"Error getting context: {str(e)}")
            return ""

    def _update_conversation_history(self, role: str, content: str) -> None:
        """
        Cập nhật lịch sử hội thoại
        """
        self.conversation_history.append({"role": role, "content": content})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

    def _get_category_statistics(self, metadatas: List[Dict[str, Any]]) -> Dict[str, Dict]:
        """
        Tính toán thống kê cho mỗi category
        """
        categories = set(meta['category'] for meta in metadatas)
        category_stats = {}

        for cat in categories:
            cat_items = [meta for meta in metadatas if meta['category'] == cat]
            cat_prices = [item['price'] for item in cat_items if 'price' in item]

            category_stats[cat] = {
                'count': len(cat_items),
                'price_range': {
                    'min': min(cat_prices) if cat_prices else 0,
                    'max': max(cat_prices) if cat_prices else 0
                }
            }

        return category_stats

    async def get_openai_response(self, message: str) -> str:
        """
        Xử lý tin nhắn và trả về response từ OpenAI
        """
        try:
            # Lấy context từ ChromaDB
            context = await self.get_relevant_context(message)
            if not context:
                return "Tôi không có đủ thông tin để trả lời câu hỏi này của bạn."

            # Lấy thêm thông tin thống kê
            results = self.collection.query(
                query_texts=[message],
                n_results=10,
                include=["documents", "metadatas"]
            )

            documents = results['documents'][0]
            metadatas = results['metadatas'][0]

            # Tính toán thống kê
            categories = set(meta['category'] for meta in metadatas)
            types = set(meta['type'] for meta in metadatas)
            category_stats = self._get_category_statistics(metadatas)

            # Tạo system prompt
            system_prompt = f"""Bạn là một trợ lý bán hàng chuyên nghiệp tại một cửa hàng thời trang. Hãy sử dụng kiến thức từ context để tư vấn một cách chi tiết và chuyên nghiệp nhất.
                NHIỆM VỤ CHÍNH:
                1. PHẢN HỒI:
                - Trả lời dựa trên context được cung cấp
                - Không bịa thêm thông tin không có trong context
                - Khi không đủ thông tin, trả lời: "Tôi không có đủ thông tin để trả lời câu hỏi này"
                
                2. CÁCH TƯ VẤN SẢN PHẨM:
                - Luôn cung cấp đầy đủ: tên sản phẩm, giá, chất liệu, size, màu sắc
                - Chủ động gợi ý mục đích sử dụng và dịp phù hợp
                - Nếu được hỏi về giá, luôn kèm theo thông tin chất liệu và tính năng của sản phẩm
                
                3. THÔNG TIN TỔNG QUAN CỬA HÀNG:
                Danh mục sản phẩm:
                {chr(10).join(f"- {cat}: {category_stats[cat]['count']} sản phẩm, giá từ {category_stats[cat]['price_range']['min']:,.0f}đ - {category_stats[cat]['price_range']['max']:,.0f}đ" for cat in categories)}
                
                4. PHÂN LOẠI SẢN PHẨM:
                - Category: {', '.join(categories)}
                - Type: {', '.join(types)}
                
                5. HƯỚNG DẪN GIÁ:
                - Luôn định dạng giá: X.XXX.XXX VNĐ
                - Giải thích lý do giá (chất liệu, tính năng)
                - Đề xuất các sản phẩm tương tự trong tầm giá
                
                6. XỬ LÝ CÂU HỎI MỞ:
                - Liệt kê tổng quan các category
                - Số lượng sản phẩm mỗi category
                - Khoảng giá từng category
                - Đề xuất xem chi tiết category phù hợp
                
                Context:
                {context}
                """
            # Cập nhật lịch sử với tin nhắn của user
            self._update_conversation_history("user", message)

            # Gọi OpenAI API
            messages = [
                {"role": "system", "content": system_prompt},
                *self.conversation_history
            ]

            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7
            )

            response = completion.choices[0].message.content

            # Cập nhật lịch sử với câu trả lời của assistant
            self._update_conversation_history("assistant", response)

            return response

        except Exception as e:
            return f"Lỗi: {str(e)}"

    def clear_conversation_history(self) -> None:
        """
        Xóa lịch sử hội thoại
        """
        self.conversation_history = []