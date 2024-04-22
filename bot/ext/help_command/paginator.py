class Paginator:

    def __init__(self, list) -> None:
        self.pages = [list[i:i + 8] for i in range(0, len(list), 8)]
        self.actual_page = 0

    @property
    def current_page(self):
        return self.pages[self.actual_page]

    def next_page(self):
        if self.actual_page + 1 < len(self.pages):
            self.actual_page += 1
    
    def previous_page(self):
        if self.actual_page > 0:
            self.actual_page -= 1


