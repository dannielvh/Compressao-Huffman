import os
import json
import heapq
import re
from collections import Counter

# Construção dos nós das árvores

class Node:
    __slots__ = ("freq", "symbol", "left", "right", "leaf")

    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.leaf = (symbol is not None)

    def to_serializable(self):
        if self.leaf:
            return {"symbol": self.symbol, "freq": self.freq}
        return {
            "freq": self.freq,
            "left": self.left.to_serializable(),
            "right": self.right.to_serializable()
        }

# Quebra o texto em tokens, que vão ser as palavras e as pontuações
# Desse jeito vai ser possível utilizar os tokens para reconstruir os textos integralmente

def tokenize(text):
    tokens = re.findall(
        r"\w+|[^\w\s]|\s",
        text,
        flags=re.UNICODE
    )
    return tokens

# Construção da árvore de Huffman

def build_huffman_tree(freqs):
    heap = []
    uid = 0

    for sym, f in freqs.items():
        heapq.heappush(heap, (f, uid, Node(f, symbol=sym)))
        uid += 1

    if len(heap) == 0:
        return None

    if len(heap) == 1:
        return heap[0][2]

    while len(heap) > 1:
        f1, id1, n1 = heapq.heappop(heap)
        f2, id2, n2 = heapq.heappop(heap)
        parent = Node(f1 + f2, left=n1, right=n2)
        heapq.heappush(heap, (parent.freq, uid, parent))
        uid += 1

    return heapq.heappop(heap)[2]

# Gera os códigos das palavras enquanto caminha pela árvore

def generate_codes(root):
    codes = {}
    if root is None:
        return codes

    def dfs(node, prefix):
        if node.leaf:
            codes[node.symbol] = prefix if prefix != "" else "0"
            return
        dfs(node.left, prefix + "0")
        dfs(node.right, prefix + "1")

    dfs(root, "")
    return codes

# Funções que trabalham com a bistring
# Fazendo a codificação e a decodificação

def encode(tokens, codes):
    return "".join(codes[t] for t in tokens)


def decode(bitstring, root):
    if root.leaf:
        return root.symbol * len(bitstring)

    node = root
    result = []
    for bit in bitstring:
        node = node.left if bit == "0" else node.right
        if node.leaf:
            result.append(node.symbol)
            node = root
    return "".join(result)

# Lê o input pra fazer a separação dos blocos de texto

def split_texts_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    raw = raw.replace("\r\n", "\n").replace("\r", "\n")

    blocks = [b for b in re.split(r"\n\s*\n", raw) if b != ""]
    return blocks

# Escreve o output com todas as informações

def write_output(out_path, results):
    with open(out_path, "w", encoding="utf-8") as f:
        for i, r in enumerate(results, start=1):
            f.write(f"--- Texto #{i} ---\n\n")

            f.write("Texto original:\n")
            f.write(r["original"] + "\n\n")

            f.write("Frequências por token:\n")
            for tok, fr in sorted(r["freqs"].items(), key=lambda x: (-x[1], x[0])):
                f.write(f"{repr(tok)}: {fr}\n")
            f.write("\n")

            f.write("Árvore:\n")
            f.write(json.dumps(r["tree"], ensure_ascii=False, indent=2) + "\n\n")

            f.write("Códigos:\n")
            for tok, code in r["codes"].items():
                f.write(f"{repr(tok)}: {code}\n")
            f.write("\n")

            f.write("Bitstring:\n")
            f.write(r["bitstring"] + "\n\n")


def process(input_path, output_path):
    texts = split_texts_from_file(input_path)

    results = []
    for txt in texts:
        tokens = tokenize(txt)
        freqs = Counter(tokens)
        root = build_huffman_tree(freqs)

        codes = generate_codes(root)
        bitstring = encode(tokens, codes)

        results.append({
            "original": txt,
            "tokens": tokens,
            "freqs": dict(freqs),
            "tree": root.to_serializable(),
            "codes": codes,
            "bitstring": bitstring,
        })

    write_output(output_path, results)
    print(f"\n[OK] Processados {len(results)} textos → {output_path}\n")


def main():
    input_path = "data/input.dat"
    output_path = "data/output.dat"

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    process(input_path, output_path)


if __name__ == "__main__":
    main()

