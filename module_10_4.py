import random
import time
import threading
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

    def is_free(self):
        return self.guest is None


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        
        wait_time = random.randint(3, 10)
        time.sleep(wait_time)
        print(f"{self.name} покушал(-а) и ушёл(ушла).")


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)
        self.lock = threading.Lock()

    def guest_arrival(self, *guests):
        for guest in guests:
            table = self.find_free_table()
            if table:
                self.seat_guest(table, guest)
            else:
                self.queue.put(guest)
                print(f"{guest.name} ждёт в очереди.")

    def find_free_table(self):
        for table in self.tables:
            if table.is_free():
                return table
        return None

    def seat_guest(self, table, guest):
        table.guest = guest
        guest.start()
        print(f"{guest.name} сел(-а) за стол номер {table.number}.")

        threading.Thread(target=self.monitor_guest, args=(table,)).start()

    def monitor_guest(self, table):
        table.guest.join()
        with self.lock:
            print(f"{table.guest.name} покинул(-а) стол номер {table.number}.")
            table.guest = None


            if not self.queue.empty():
                next_guest = self.queue.get()
                self.seat_guest(table, next_guest)


def main():
    tables = [Table(i) for i in range(1, 6)]
    cafe = Cafe(*tables)


    guests = [Guest(f"Гость {i}") for i in range(1, 11)]


    cafe.guest_arrival(*guests)


if __name__ == "__main__":
    main()