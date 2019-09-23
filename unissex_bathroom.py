# builtin imports
from multiprocessing import Process, Queue
import threading
import random
import time
from time import sleep

# internal libs imports
from constants import (
    MALE,
    FEMALE,
    THIRD_GENDER
)

from utils import (
    print_green,
    print_red,
    print_yellow,
    print_cyan,
    print_purple
)


class UnissexBathroom:

    def __init__(self, num_boxes, num_people):
        self.num_people = num_people
        self.sem_bathroom = threading.Semaphore(value=num_boxes)


    queue = Queue()
    queue_time = Queue()
    count_person = 1
    count_male = 0
    count_female = 0
    count_third_gender = 0
    count_bathroom = 0

    gender_bathroom = 0
    start_male_time = []
    start_female_time = []
    start_third_gender_time = []
    end_male_time = []
    end_female_time = []
    end_third_gender_time = []
    end_time = 0
    total_time = 0
    start_box_time = []
    end_box_time = []
    total_box_time = 0
    start_time = time.time()
    sem_queue = threading.Semaphore()
    sem_mutex = threading.Semaphore()

    TIME_IN_BATHROOM = 10

    def enter_queue(self):
        self.sem_queue.acquire()
        for i in range(0, self.num_people):
            if random.randint(0, 2) == MALE:
                self.start_male_time.append(time.time())

                self.queue.put([MALE, self.count_person])
                self.count_person += 1
                male_enqueue_message = (
                    '|ENQUEUE|> People #{0}: A man has arrived to the queue'.format(
                        self.count_person - 1
                    )
                )
                print_cyan(male_enqueue_message)
                sleep(random.randint(1, 7))

            elif random.randint(0, 2) == FEMALE:
                self.start_female_time.append(time.time())

                self.queue.put([FEMALE, self.count_person])
                self.count_person += 1
                female_enqueue_message = (
                    '|ENQUEUE|> People #{0}: A woman has arrived to the queue'.format(
                        self.count_person - 1
                    )
                )
                print_red(female_enqueue_message)
                sleep(random.randint(1, 7))
            else:
                self.start_third_gender_time.append(time.time())

                self.queue.put([THIRD_GENDER, self.count_person])
                self.count_person += 1
                third_gender_message = (
                    '|ENQUEUE|> People #{0}: A third gender people has arrived to the queue'.format(
                        self.count_person - 1
                    )
                )
                print(third_gender_message)
                sleep(random.randint(1, 7))
        start_timers = {
            'start_female_time': self.start_female_time,
            'start_male_time': self.start_male_time,
            'start_third_gender_time': self.start_third_gender_time
        }
        self.queue_time.put(start_timers)
        self.sem_queue.release()

    def enter_rest_room(self):
        while 1:
            self.sem_queue.acquire()
            if self.queue.qsize() > 0:
                p = self.queue.get()
                self.sem_queue.release()
                self.sem_mutex.acquire()
                if self.gender_bathroom == p[0]:
                    self.sem_mutex.release()
                    self.sem_bathroom.acquire()
                    t1 = threading.Thread(target=self.out_box, args=(p,))
                    t1.start()
                else:
                    print_yellow('|WAIT|>  Waiting for other same-sex person')
                    while self.count_bathroom > 0:
                        self.sem_mutex.release()
                        self.sem_mutex.acquire()
                    self.sem_mutex.release()
                    self.sem_bathroom.acquire()
                    self.gender_bathroom = p[0]
                    if self.queue_time.qsize() > 0:
                        t = self.queue_time.get()
                        t2 = threading.Thread(target=self.out_box, args=(p, t))
                        t2.start()
                    else:
                        t2 = threading.Thread(target=self.out_box, args=(p, ))
                        t2.start()

            else:
                self.sem_queue.release()

    def out_box(self, persons, timer=None):
        self.sem_mutex.acquire()
        if timer:
            self.start_male_time = timer.get('start_male_time')
            self.start_female_time = timer.get('start_female_time')
            self.start_third_gender_time = timer.get('start_third_gender_time')

        if persons[0] == FEMALE:
            self.count_female += 1
            self.end_female_time.append(time.time())

            female_enter_bathroom_message = (
                '|ENTER-BATHROOM|>  People #{0}:a woman just enterred into the bathroom'.format(
                    persons[len(persons) - 1])
            )
            print_green(female_enter_bathroom_message)

        elif persons[0] == MALE:
            self.count_male += 1
            self.end_male_time.append(time.time())
            male_enter_bathroom_message = (
                '|ENTER-BATHROOM|>  People #{0}:a man just enterred into the bathroom'.format(
                    persons[len(persons) - 1])
            )
            print_green(male_enter_bathroom_message)

        else:
            self.count_third_gender += 1
            self.end_third_gender_time.append(time.time())
            print('|ENTER-BATHROOM|>  People #{0}:a third gender people just enterred into the bathroom'.format(
                persons[len(persons) - 1])
            )

        self.start_box_time.append(time.time())
        self.sem_mutex.release()
        self.count_bathroom += 1

        sleep(self.TIME_IN_BATHROOM)
        self.sem_mutex.acquire()
        self.end_box_time.append(time.time())
        self.count_bathroom -= 1

        exit_message = '|EXIT|> People #{0}: left the bathroom'.format(persons[len(persons) - 1])
        print_purple(exit_message)

        if persons[len(persons) - 1] == self.num_people:
            end_time = time.time()
            print(timer)
            print("\n{0}\nStatistics\n{0}\n".format(60 * "*"))
            print("Total people:", self.count_male + self.count_female + self.count_third_gender)
            print("Total men: ", self.count_male)
            print("Total women: ", self.count_female)
            print('Total third gender person', self.count_third_gender)

            print("\n{0}\n".format(60 * "*"))

            total_time_male = (sum(self.end_male_time) - sum(self.start_male_time))
            total_time_female = (sum(self.end_female_time) - sum(self.start_female_time))
            total_time_third_gender = (sum(self.end_third_gender_time) - sum(self.start_third_gender_time))

            average_male = 0 if not self.count_female else total_time_male / self.count_male
            average_female = 0 if not self.count_female else total_time_female / self.count_female
            average_third_gender = 0 if not self.count_third_gender else total_time_third_gender / self.count_third_gender

            print("average time men:", average_male, 'seconds')
            print("average time women:", average_female, 'seconds')
            print("average time third gender", average_third_gender, 'seconds')
            totalTime = end_time - self.start_time
            totalBoxTime = sum(self.end_box_time) - sum(self.start_box_time)
            print("Execution time:", totalTime, 'seconds')
            print("|BOX|> Usage time:", totalBoxTime, 'seconds')
            print("|BOX|> Rate time ocupation:", totalBoxTime / totalTime, 'seconds')
            print("\n{0}\n".format(60 * "*"))
        self.sem_mutex.release()
        self.sem_bathroom.release()

    @classmethod
    def run(cls, num_people, num_boxes):
        obj = cls(num_people=num_people, num_boxes=num_boxes)
        p1 = Process(target=obj.enter_queue)
        p1.start()

        p2 = Process(target=obj.enter_rest_room)
        p2.start()

        p1.join()
        p2.join()

        p1.terminate()
        p2.terminate()
