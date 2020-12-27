class BilibiliAPIException(Exception):

    def __init__(self, errCode: int) -> None:
        super().__init__()
        self.errCode = errCode
    
    def __str__(self):
        return f"api.bilibili.com returned code {self.errCode} instead of 0."