
async def make_context_text(objs):
    context = ""
    for item in objs:
        context += f"<em><b>{item.title}</b></em>\n\n{item.description}\n<b>{item.address}</b>"

    return context