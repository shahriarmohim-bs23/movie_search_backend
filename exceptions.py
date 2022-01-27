class NotFoundException(Exception):
    def __init__(self,resource, *args: object) -> None:
        super().__init__(*args)
        self.status_code = 404
        self.message = f'{resource} Not found'
        