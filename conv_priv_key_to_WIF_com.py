import binascii
import hashlib
import base58

def hex_to_wif(hex_key):
    """
    Converts a hexadecimal private key to WIF format.

    Args:
        hex_key (str): Hexadecimal private key (any length).

    Returns:
        str: Private key in WIF format.
    """

    # Convert to bytes
    byte_key = binascii.unhexlify(hex_key)

    # Version byte (0x80 for mainnet)
    version_byte = b"\x80"

    # Add compression flag (0x01)
    compressed_flag = b"\x01"

    # Concatenate version, key, and compression flag
    wif_key = version_byte + byte_key + compressed_flag

    # Double SHA256 hash
    sha256_1 = hashlib.sha256(wif_key).digest()
    sha256_2 = hashlib.sha256(sha256_1).digest()

    # Checksum (first 4 bytes of second hash)
    checksum = sha256_2[:4]

    # Concatenate key, compression flag, and checksum
    wif_key += checksum

    # Encode in Base58
    wif_encoded = base58.b58encode(wif_key)

    return wif_encoded.decode("utf-8")

def get_private_key():
    """
    Prompt the user to input the private key in hexadecimal format.

    Returns:
        str: Hexadecimal private key.
    """
    return input("Digite a chave privada em formato hexadecimal: ").strip()

def save_wif_to_file(wif_key, output_file):
    """
    Save the WIF key to a text file.

    Args:
        wif_key (str): Private key in WIF format.
        output_file (str): Name of the output file.
    """
    with open(output_file, "w") as f:
        f.write(f"{wif_key}\n")
    print(f"A chave WIF foi salva no arquivo: {output_file}")

def main():
    output_file = "WIF_UN_BALANCE_WIN.txt"  # Nome do arquivo de saída

    hex_key = get_private_key()
    wif_key = hex_to_wif(hex_key)
    save_wif_to_file(wif_key, output_file)
    print(f"A chave WIF é: {wif_key}")

if __name__ == "__main__":
    main()
