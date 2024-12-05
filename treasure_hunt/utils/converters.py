def string_to_matrix(input_string: str) -> list[list]:
    """
    Converte uma string no formato 'x | x | x' para uma matriz (lista de listas),
    convertendo valores numéricos para inteiros.

    Args:
        input_string (str): String no formato 'x | x | x\nx | x | x'.

    Returns:
        list[list]: Matriz representando os valores da string, com números como inteiros.
    """
    # Divide a string em linhas
    rows = input_string.strip().split("\n")
    
    matrix = [
        [int(value.strip()) if value.strip().isdigit() else value.strip() for value in row.split("|")]
        for row in rows
    ]
    
    return matrix
