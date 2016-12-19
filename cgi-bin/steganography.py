# -*- coding: utf-8 -*-
import codecs
import sha.py
import pyDes.py
import png
import numpy as np


def get_max_length(reader):
    w, h, pixels, metadata = reader.read_flat()
    pixel_byte_width = 4 if metadata['alpha'] else 3
    max_length = w * h * pixel_byte_width / 8
    return max_length


def read_txt_file(txt_path):
    with codecs.open(txt_path, encoding='UTF-8') as file_object:
        data = file_object.read()
        return data


def write_txt_file(new_txt_path, text):
    with codecs.open(new_txt_path, "w", encoding='UTF-8') as file_object:
        data = file_object.write(text)


def get_hash_key(str_secret_word):
    hash_func = sha.sha256.new()
    hash_func.update(str_secret_word)
    return hash_func.digest()[:8]


def get_DESformat_str(str_text):
    remainder = len(str_text) % 8
    if remainder == 0:
        return str_text
    else:
        return str_text + ' ' * (8 - remainder)


def get_header(str_text):
    header = 'length:' + "{:09d}".format(len(str_text))
    return header


def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


def frombits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def write_txt_to_image(reader, bit_text, new_image_path='new_image.png'):
    w, h, pixels, metadata = reader.read_flat()
    for i, bit in enumerate(bit_text):
        if bit:
            if pixels[i] % 2:
                continue
            else:
                pixels[i] += 1
        else:
            if pixels[i] % 2:
                pixels[i] -= 1
            else:
                continue
    output = open(new_image_path, 'wb')
    writer = png.Writer(w, h, **metadata)
    writer.write_array(output, pixels)
    output.close()


def get_txt_from_image(image_path):
    HEADER_BIT_LENGTH = 16 * 8
    reader = png.Reader(image_path)
    w, h, pixels, metadata = reader.read_flat()
    bits = np.zeros(HEADER_BIT_LENGTH)
    for i, pixel in enumerate(pixels):
        if i < HEADER_BIT_LENGTH:
            if pixel % 2:
                bits[i] = 1
            else:
                continue
    header = frombits(bits.astype(int))
    if header[:6] == 'length':
        try:
            length = int(header[7:16]) * 8
        except:
            length = len(pixels)
    else:
        length = len(pixels)
    if length + HEADER_BIT_LENGTH > len(pixels):
        result_length = len(pixels)
    else:
        result_length = length + HEADER_BIT_LENGTH
    bits = np.zeros(result_length)
    for i, pixel in enumerate(pixels):
        if i < result_length:
            if pixel % 2:
                bits[i] = 1
            else:
                continue
    result = frombits(bits.astype(int))[16:]
    return result


def txt_to_png(image_path, text_path, secret_word, new_image_path='new_image.png'):
    text = read_txt_file(text_path)
    str_text = text.encode('UTF-8')
    hash_key = get_hash_key(secret_word)
    cipher = pyDes.des.new(hash_key)
    str_text = get_DESformat_str(str_text)
    ciphertext = cipher.encrypt(str_text)
    header = get_header(str_text)
    reader = png.Reader(image_path)
    if (get_max_length(reader) < len(ciphertext) + len(header)):
        return u'Слишком большой файл'
    bit_text = tobits(header + ciphertext)
    reader = png.Reader(image_path)
    write_txt_to_image(reader, bit_text, new_image_path=new_image_path)
    return u'Успешно'


def txt_from_png(image_path, secret_word):
    str_text = get_txt_from_image(image_path)
    hash_key = get_hash_key(secret_word)
    str_text = get_DESformat_str(str_text)
    cipher = pyDes.des.new(hash_key)
    str_text = cipher.decrypt(str_text)
    return str_text
