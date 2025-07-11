from dataclasses import dataclass
from typing import List


@dataclass
class BBox:
    tag: int
    confidence: float

    def __repr__(self):
        return f"(tag={self.tag}, conf={self.confidence})"


def bbox_sort(boxes: List[BBox]) -> List[BBox]:
    # 按照：tag 升序，confidence 降序 排序
    return sorted(boxes, key=lambda b: (b.tag, -b.confidence))


def main():
    # 测试数据
    boxes = [
        BBox(2, 0.7),
        BBox(1, 0.8),
        BBox(2, 0.6),
        BBox(1, 0.5),
        BBox(3, 0.9),
        BBox(1, 0.95),
        BBox(3, 0.3),
        BBox(2, 0.4),
        BBox(3, 0.2),
        BBox(1, 0.85),
        BBox(2, 0.75),
    ]

    print("原始数据：")
    print(boxes)

    sorted_boxes = bbox_sort(boxes)

    print("\n排序后：")
    for b in sorted_boxes:
        print(b)


if __name__ == "__main__":
    main()
