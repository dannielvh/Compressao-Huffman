# Código de Huffman para compressão de textos

Trabalho elaborado individualmente, no qual foi utilizado os conhecimentos acerca das estruturas em árvores e compressão de dados através de uma implementação do Algoritmo de Huffman. Foi implementado um sistema de compressçao de textos usando o Algoritmo de Huffman por palavras, preservando então a estrutura original do texto, incluindo espaços, pontuação e quebras de linha. O programa então lê os blocos de texto e tokeniza cada elemento, calculando a frequência de cada token e construindo a árvore de Huffman correspondente, para no fim gerar os códigos binários e produzir uma bitstring comprimida para registrar no arquivo de saída o texto original, os tokens, as suas frequências, a árvore e o código que foi gerado, permitindo assim a recostrução exata do texto original.

Ao final do programa ele gera então um arquivo de saída com as árvores geradas, os tokens e o texto codificado, arquivo esse que estará localizado na pasta **data**, onde anteriormente já estava o arquivo de entrada.

### Instruções

Seguindo essas instruções será possível executar o programa:

```bash
git clone https://github.com/dannielvh/Compressao-Huffman.git
cd Compressao-Huffman

# WINDOWS
python src/Huffman.py

#LINUX
python3 src/Huffman.py
```

Para plena funcionalidade do código o arquivo **input.dat** deve estar dentro da pasta **data**, e assim fica livre para o usuário modificar as frases. Cada bloco de texto deve estar separado por uma linha em branco.
