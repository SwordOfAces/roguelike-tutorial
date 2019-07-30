import tcod as libtcod

from game_messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry anymore, your inventory is full', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message(f"You pick up the {item.name}", libtcod.blue)
            })
            self.items.append(item)

        return results


    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            results.append({'message', Message(f'The {item_entity.name} cannot be used.', libtcod.yellow)})
        else:
            kwargs = {**item_component.f_kwargs, **kwargs}
            use_results = item_component.use_function(self.owner, **kwargs)

            for result in use_results:
                if result.get('consumed'):
                    self.remove_item(item_entity)
            
            results.extend(use_results)

        return results


    def remove_item(self, item):
        self.items.remove(item)
