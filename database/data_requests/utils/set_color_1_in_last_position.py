async def set_other_color_on_last_position(color_models):
    last_color = [color for color in color_models if color.id == 1]
    if last_color:
        color_models = [color for color in color_models if color.id != 1]
        color_models.append(last_color[0])
    elif not isinstance(color_models, list):
        color_models = list(color_models)

    return color_models