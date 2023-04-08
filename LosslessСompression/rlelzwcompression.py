import collections
import math
import matplotlib.pyplot as plt


def get_sequences():
    with open("sequence.txt", "r", encoding="utf8") as file:
        original_sequences = [sequence.strip("\n") for sequence in file.readlines()]
    return original_sequences


def write_inf(file, original_sequence, entropy, encoded_rle, cr_rle, decoded_rle):
    file.write(f"Послідовність: {original_sequence}\n")
    file.write(f"Розмір послідовності: {len(original_sequence) * 16} bits\n")
    file.write(f"Ентропія: {entropy}\n \n")
    file.write(f"_____________Кодування_RLE_____________\n")
    file.write(f"Закодована RLE послідовність: {encoded_rle}\n")
    file.write(f"Розмір закодованої RLE послідовності: {len(encoded_rle) * 16} bits\n")
    file.write(f"Коефіцієнт стиснення RLE: {cr_rle}\n")
    file.write(f"Декодована RLE послідовність: {decoded_rle}\n")
    file.write(f"Розмір декодованої RLE послідовності: {len(decoded_rle) * 16} bits\n \n")
    file.write(f"_____________Кодування_LZW_____________\n")
    file.write(f"___________Поетапне кодування__________\n")


def save_sequence(original_sequence, entropy, encoded_rle, cr_rle, decoded_rle):
    try:
        with open("results_rle_lzw.txt", "a", encoding="utf8") as file:
            write_inf(file, original_sequence, entropy, encoded_rle, cr_rle, decoded_rle)
    except FileNotFoundError:
        with open("results_rle_lzw.txt", "w", encoding="utf8") as file:
            write_inf(file, original_sequence, entropy, encoded_rle, cr_rle, decoded_rle)


def encode_rle(sequence):
    count, result = 1, []
    for i, item in enumerate(sequence):
        if i == 0:
            continue
        elif item == sequence[i - 1]:
            count += 1
        else:
            result.append((sequence[i - 1], count))
            count = 1
    result.append((sequence[len(sequence) - 1], count))
    encoded = [f"{item[1]}{item[0]}" for i, item in enumerate(result)]
    return "".join(encoded), result


def encode_zlw(sequence):
    dictionary = {chr(i): i for i in range(65536)}
    result, size, current = [], 0, ""
    for c in sequence:
        new_str = current + c
        if new_str in dictionary:
            current = new_str
        else:
            result.append(dictionary[current])
            dictionary[new_str] = len(dictionary)
            element_bits = 16 if dictionary[current] < 65536 else math.ceil(math.log2(len(dictionary)))
            with open("results_rle_lzw.txt", "a", encoding="utf8") as file:
                file.write(f"Code: {dictionary[current]}, Element: {current}, bits: {element_bits}\n")
            current = c
            size += element_bits
    last = 16 if dictionary[current] < 65536 else math.ceil(math.log2(len(dictionary)))
    size += last
    result.append(dictionary[current])
    cr_lzv = round((len(sequence) * 16 / size), 2)
    with open("results_rle_lzw.txt", "a", encoding="utf8") as file:
        file.write(f"Code: {dictionary[current]}, Element: {current}, Bits: {last}\n")
        file.write("_____________________________________\n")
        file.write(f"Закодована LZW послідовність:{''.join(map(str, result))} \n")
        file.write(f"Розмір закодованої LZW послідовності: {size} bits \n")
        file.write(f"Коефіцієнт стиснення LZW: {cr_lzv}\n")
    return result, cr_lzv


def decode_rle(sequence):
    result = []
    for item in sequence:
        result.append(item[0] * item[1])
    return "".join(result)


def decode_zlw(sequence):
    dictionary = {i: chr(i) for i in range(65536)}
    result = dictionary[sequence[0]]
    current = result
    for code in sequence[1:]:
        if code in dictionary:
            sequence = dictionary[code]
        else:
            sequence = current + current[0]
        result += sequence
        dictionary[len(dictionary)] = current + sequence[0]
        current = sequence
    with open("results_rle_lzw.txt", "a", encoding="utf8") as file:
        file.write(f"Декодована LZW послідовність: {result}\n")
        file.write(f"Розмір декодованої LZW послідовності: {len(result) * 16} bits\n \n" + "_" * 100 + "\n \n")


def main():
    N_sequence, results = 100, []
    original_sequences = get_sequences()
    for sequence in original_sequences:
        counts = collections.Counter(sequence)
        probability = {symbol: count / N_sequence for symbol, count in counts.items()}
        entropy = -sum(p * math.log2(p) for p in probability.values())
        encoded_sequence, encoded = encode_rle(sequence)
        cr_rle = round(len(sequence) / len(encoded_sequence), 2)
        cr_rle = "-" if cr_rle < 1 else cr_rle
        decoded_sequence = decode_rle(encoded)
        save_sequence(sequence, entropy, encoded_sequence, cr_rle, decoded_sequence)
        encoded_zlv, cr_lzv = encode_zlw(sequence)
        decode_zlw(encoded_zlv)
        results.append([round(entropy, 2), cr_rle, cr_lzv])
    fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
    headers = ['Ентропія', 'КС RLE', 'КС LZW']
    row = [f'Послідовність {i}' for i in range(1, 9)]
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)
    fig.savefig("Результати стиснення методами RLE та LZW.png", dpi=600)


if __name__ == "__main__":
    main()
