
import wikipediaapi
import re
from collections import defaultdict
from itertools import combinations
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk
import pandas as pd

nltk.download('stopwords')

# --- Bước: Lấy dữ liệu từ nhiều chủ đề khác nhau trên Wikipedia ---
topics = [
    "Artificial intelligence",
    "Travel",
    "Game",
    "Sports",
    "Robotics",
    "Data mining",
    "Music",
    "Deep learning"
]

wiki = wikipediaapi.Wikipedia('en')
texts = []

for topic in topics:
    page = wiki.page(topic)
    if page.exists():
        print(f"Lấy bài viết: {topic}")
        texts.append(page.text)
    else:
        None

# Gộp toàn bộ thành 1 collection
text = "\n".join(texts)

# --- Bước: Index collection (không stemming) ---
tokens = re.findall(r'\b[a-zA-Z]+\b', text.lower())
tokens = [t for t in tokens if t not in stopwords.words('english')]
vocab = sorted(set(tokens))
selected_words = vocab[:1000]

# --- Bước: Tạo stem classes ---
stemmer = PorterStemmer()
stem_classes = defaultdict(list)
for word in selected_words:
    stem = stemmer.stem(word)
    stem_classes[stem].append(word)

# --- Bước: Tính Dice’s coefficient ---
sentences = [re.findall(r'\b[a-zA-Z]+\b', s.lower()) for s in text.split('.')]

def dice_coefficient(a, b):
    n_a = sum(a in s for s in sentences)
    n_b = sum(b in s for s in sentences)
    n_ab = sum(a in s and b in s for s in sentences)
    if n_a + n_b == 0:
        return 0
    return 2 * n_ab / (n_a + n_b)

dice_results = []
for stem, words in stem_classes.items():
    if len(words) > 1:
        for a, b in combinations(words, 2):
            score = dice_coefficient(a, b)
            if score > 0:
                dice_results.append((a, b, score))

# --- Bước: Xuất kết quả ---
print(f"\nTổng số bài viết: {len(texts)}")
print(f"Tổng số từ: {len(tokens)}")
print(f"Số lượng từ duy nhất: {len(vocab)}")
print(f"Số nhóm stem: {len(stem_classes)}")

print("\nVí dụ vài nhóm stem:")
for i, (stem, words) in enumerate(stem_classes.items()):
    if len(words) > 1:
        print(f"{stem}: {words[:50]}")
    if i > 25:
        break

print("Ví dụ Dice’s coefficient:")
for a, b, score in dice_results[:10]:
    print(f"{a} - {b}: {score:.2f}")

# --- (Tuỳ chọn) Lưu kết quả ra file CSV ---
df = pd.DataFrame(dice_results, columns=["word1", "word2", "dice"])
df.to_csv("wiki_dice_results.csv", index=False)
print("\nKết quả được lưu trong file: wiki_dice_results.csv")
