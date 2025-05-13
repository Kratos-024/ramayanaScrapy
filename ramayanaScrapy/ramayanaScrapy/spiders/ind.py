def find_missing(chapters, max_value=77):
    # Convert all values to integers
    chapter_nums = set(int(ch) for ch in chapters)
    
    # Full set from 1 to max_value
    full_set = set(range(1, max_value + 1))
    
    # Find missing
    missing = sorted(full_set - chapter_nums)
    return missing

chapters = ['69', '77', '71', '72', '68', '75', '74', '76', '65', '62', '61', '73', '63', '56', '64', '66', '54', '57', '55', '59', '58', '60', '67', '70', '52', '48', '53', '33', '31', '32', '27', '28', '29', '24', '25', '23', '19', '20', '21', '22', '17', '16', '26', '18', '15', '12', '13', '14', '10', '9', '8', '7', '6', '4', '11', '5', '2', '3', '1']

missing_chapters = find_missing(chapters)
print("Missing chapters:", missing_chapters)