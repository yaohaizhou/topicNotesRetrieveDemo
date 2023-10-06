import logging
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s, %(levelname)s, %(message)s')


class ProgressLog(object):

    def __init__(self) -> None:
        self._reset()

    def _reset(self):
        self.desc = None
        self.total = None
        self.cur = None
        self.start_time = None
        self.end_time = None

    def init(self, total: int, desc: str) -> None:
        self._reset()
        self.desc = desc
        self.total = total
        self.cur = 0
        self.start_time = time.time()

    def update(self, n: int = 1) -> None:
        self.cur += n
        assert self.cur <= self.total
        if self.cur == self.total:
            self.end_time = time.time()
        print_log(
            "Url: %s, Progress: %2d/%2d, Time: %.1fs" %
            (self.desc, self.cur, self.total, time.time() - self.start_time))

    def close(self, tokens: int, cost: float) -> None:
        time_used = self.end_time - self.start_time
        print_log("Url: %s, Succeed, Time: %.1fs, Tokens: %d, Cost: %.3f$" %
                  (self.desc, time_used, tokens, cost))
        self._reset()


def print_log(text: str, mode: str = "info") -> None:
    if mode == "info":
        logging.info(text)
    elif mode == "warning":
        logging.warning(text)
    else:
        raise NotImplementedError("mode %s not found" % mode)
