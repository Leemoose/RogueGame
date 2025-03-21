

def rank_destroy_items_in_inventory(ai, loop):
    if ai.parent.inventory.get_inventory_size() > 0:
        return ai.randomize_action("destroy_items")
    else:
        return -1

def do_destroy_items_in_inventory(ai, loop):
    for item in ai.parent.get_inventory():
        item.set_destroy(True)
        ai.parent.inventory.do_drop(item, loop.generator.item_map)
        loop.add_message(f"{item.name} consumed by {ai.parent.name}")