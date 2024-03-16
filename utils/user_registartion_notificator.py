import importlib


async def user_dont_registrated(request):
    message_editor_module = importlib.import_module('handlers.message_editor')

    await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='user_non_registration')
