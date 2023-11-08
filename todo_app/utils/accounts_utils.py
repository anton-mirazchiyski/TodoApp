def set_placeholder(field, fields):
    placeholders = ['Username', 'Password', 'Repeat Password']
    for field, placeholder in zip(fields, placeholders):
        fields[field].widget.attrs['placeholder'] = placeholder
