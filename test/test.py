import sys
sys.path.append("../src")
from word_segmentation import word_segment

print(word_segment("我们学习人工智能，人工智能是未来"))
print(word_segment("我喜欢做饭"))