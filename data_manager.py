# data_manager.py
from app.openai_service import RAGService
from datetime import datetime


def add_product_data():
    rag = RAGService()

    products = [
        {
            "document": "Áo dài truyền thống Hoàng Kim là sản phẩm cao cấp của cửa hàng, được may từ lụa tơ tằm 100%, có các size từ S đến XL. Giá: 1.500.000 VNĐ. Màu sắc: đỏ thẫm, vàng gold, xanh cobalt. Phù hợp cho các dịp lễ tết, cưới hỏi.",
            "metadata": {
                "category": "traditional",
                "type": "ao_dai",
                "price": 1500000,
                "timestamp": datetime.now().isoformat(),
                "occasion": "tet, wedding"
            }
        },
        {
            "document": "Áo sơ mi công sở Elegant được làm từ vải cotton pha polyester, form chuẩn văn phòng, có các size 38-44. Giá: 450.000 VNĐ. Màu sắc: trắng, xanh nhạt, hồng pastel. Phù hợp cho dân văn phòng, có thể giặt máy.",
            "metadata": {
                "category": "office",
                "type": "shirt",
                "price": 450000,
                "timestamp": datetime.now().isoformat(),
                "occasion": "office"
            }
        },
        {
            "document": "Quần âu Smart Fit được may từ vải tuyết mưa cao cấp, có độ co giãn nhẹ, form ôm vừa vặn. Giá: 550.000 VNĐ. Size: 29-34. Màu sắc: đen, xám, navy. Phù hợp mặc công sở hoặc các sự kiện trang trọng.",
            "metadata": {
                "category": "office",
                "type": "pants",
                "price": 550000,
                "timestamp": datetime.now().isoformat(),
                "occasion": "office, formal"
            }
        },
        {
            "document": "Đầm suông Morning Coffee được làm từ vải linen blend, thiết kế thanh lịch với túi hai bên. Giá: 750.000 VNĐ. Size: S-XXL. Màu sắc: be, xanh mint, nâu nhạt. Phù hợp đi café, dạo phố hoặc đi làm.",
            "metadata": {
                "category": "casual",
                "type": "dress",
                "price": 750000,
                "timestamp": datetime.now().isoformat(),
                "occasion": "casual, office"
            }
        },
        {
            "document": "Áo polo Weekend Casual được làm từ cotton 4 chiều, thấm hút mồ hôi tốt. Giá: 320.000 VNĐ. Size: M-XXL. Màu sắc: xanh rêu, đen, trắng sữa. Phù hợp mặc cuối tuần hoặc đi chơi thể thao.",
            "metadata": {
                "category": "casual",
                "type": "polo",
                "price": 320000,
                "timestamp": datetime.now().isoformat(),
                "occasion": "casual, sport"
            }
        },
        {
            "document": "Chân váy xếp ly Autumn Breeze được làm từ vải dạ mỏng, thiết kế xếp ly nhỏ thanh lịch. Giá: 480.000 VNĐ. Size: S-L. Màu sắc: đen, nâu đất, xám nhạt. Phù hợp mặc mùa thu đông, dễ phối đồ.",
            "metadata": {
                "category": "casual",
                "type": "skirt",
                "price": 480000,
                "timestamp": datetime.now().isoformat(),
                "season": "autumn, winter"
            }
        },
        {
            "document": "Set đồ thể thao Active Life gồm áo và quần được làm từ vải thun lạnh cao cấp, co giãn 4 chiều. Giá: 600.000 VNĐ/set. Size: M-XL. Màu sắc: xám đen, xanh navy, đen trắng. Phù hợp tập gym hoặc chạy bộ.",
            "metadata": {
                "category": "sport",
                "type": "set",
                "price": 600000,
                "timestamp": datetime.now().isoformat(),
                "occasion": "sport, gym"
            }
        },
        {
            "document": "Váy maxi Summer Bloom được làm từ vải voan hoa, thiết kế dài thanh lịch. Giá: 850.000 VNĐ. Size: S-L. Màu sắc: hoa xanh, hoa hồng, hoa vàng. Phù hợp đi biển, dự tiệc hoặc dạo phố.",
            "metadata": {
                "category": "casual",
                "type": "dress",
                "price": 850000,
                "timestamp": datetime.now().isoformat(),
                "occasion": "beach, party, casual"
            }
        },
        {
            "document": "Quần jean Daily Comfort được làm từ vải jean cotton có độ co giãn, form regular fit. Giá: 520.000 VNĐ. Size: 29-36. Màu sắc: xanh đậm, xanh nhạt, đen. Phù hợp mặc hàng ngày, bền đẹp.",
            "metadata": {
                "category": "casual",
                "type": "jeans",
                "price": 520000,
                "timestamp": datetime.now().isoformat(),
                "occasion": "daily"
            }
        },
        {
            "document": "Áo khoác Windbreaker Light được làm từ vải dù cao cấp, chống nước nhẹ, có mũ. Size: S-XXL. Màu sắc: đen, xanh army, be. Phù hợp mặc mùa mưa hoặc thời tiết se lạnh.",
            "metadata": {
                "category": "outerwear",
                "type": "jacket",
                "price": 680000,
                "timestamp": datetime.now().isoformat(),
                "season": "rainy, cold"
            }
        },
        {
            "document": "Áo khoác VN được làm từ vải dù cao cấp, chống nước nhẹ, có mũ. Size: S-XXL. Màu sắc: đen, xanh army, be. Phù hợp mặc mùa mưa hoặc thời tiết se lạnh.",
            "metadata": {
                "category": "outerwear",
                "type": "jacket",
                "price": 680000,
                "timestamp": datetime.now().isoformat(),
                "season": "rainy, cold"
            }
        }
    ]

    # Tách documents và metadata
    documents = [p["document"] for p in products]
    metadata = [p["metadata"] for p in products]

    # Thêm vào database
    success = rag.add_documents(documents, metadata)

    if success:
        print("Products added successfully!")
    else:
        print("Error adding products")


if __name__ == "__main__":
    add_product_data()