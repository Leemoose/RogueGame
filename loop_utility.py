from loop_workflow import *
def get_loop_mapping_from_string():
    loop_type_mapping = {"victory": LoopType.victory,
                         "action": LoopType.action,
                         "trade": LoopType.trade,
                         "inventory": LoopType.inventory,
                         "enchant": LoopType.enchant}
    return loop_type_mapping