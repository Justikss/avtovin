async def set_other_color_on_last_position(color_models, without_other=False):
    last_color = [color for color in color_models if color.id == 1]
    ic(last_color)
    if not isinstance(color_models, list):
        color_models = list(color_models)

    if last_color:
        color_models = [color for color in color_models if color.id != 1]
        if not without_other:
            color_models.append(last_color[0])

    ic(color_models)

    return color_models