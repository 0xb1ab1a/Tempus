from datetime import timedelta, datetime
from getopt import getopt
import sys
import os


class Timestats():
    """ Current version: 0.82
    """
    def __init__(self):
        self.days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        self.time_list = []
        self.file = open(os.path.dirname(os.path.abspath(__file__)) + '\worktime', 'r+')
        self.file.seek(0)
        self.daylst = self.file.read().split()
        for half_day in self.daylst:
            self.time_list.append(timedelta(hours=int(half_day.split('.')[0]), minutes=int(half_day.split('.')[1])))

    def oneday(self, day):
        if day not in xrange(1, 6):
            print("Incorrect  day number")
        else:
            result = self.resolve_oneday(day)
            print('At the {} you worked about {} hours'.format(self.days[day - 1], result))

    def resolve_oneday(self, day):
        res = self.time_list[2 * day - 1] - self.time_list[2 * day - 2]
        if res.total_seconds() < 0:
            res = timedelta(0)
        return res

    def week(self):
        count = 1
        for t in self.time_list:
            if count % 2 == 1:
                print('\n' + self.days[count / 2])
            print(t)
            count += 1

    def total(self):
        result = timedelta(0)
        for i in range(1, 6):
            result += self.resolve_oneday(i)
        print('On this week you worked {} hours'.format(result))
        print('Remaining hours to work {}'.format(timedelta(days=1, hours=18, minutes=30) - result))

    def write_day(self, day, ending, time):
        if len(time) != 5:
            print("Error in input format")
        elif day not in xrange(1, 6):
            print("Incorrect  day number")
        else:
            time = time.replace(':', '.')
            time = time.replace(',', '.') + '\n'
            self.file.seek((day + day - 1)*7 - ending)
            self.file.write(time)
            print('Time added')

    def write_current(self, ending):
        day = datetime.today().weekday() + 1
        minutes = str(datetime.today().minute)
        hours = str(datetime.today().hour)
        if len(minutes) < 2:
            minutes = '0' + minutes
        if len(hours) < 2:
            hours = '0' + hours
        time = hours + '.' + minutes
        self.write_day(day, ending, time)

    def reset(self):
        self.file.seek(0)
        for count in xrange(10):
            self.file.write('00.00\n')

    def interface(self):
        opt, args = getopt(sys.argv[1:], 'becv', ['begin', 'end', 'console'])
        for op, val in opt:
            if op in ['-b', '--begin']:
                self.write_current(7)
            elif op in ['-e', '--end']:
                self.write_current(0)
            elif op in ['-c', '--console']:
                self.console()
            elif op in ['-v', '--version']:
                print(Timestats.__doc__)

    def console(self):
        Main = Timestats()
        print('Welcome to Timestats!')
        while True:
            command = raw_input()
            if command == 'exit':
                Main.file.close()
                break
            elif command[:3] == 'day':
                Main.oneday(int(command[-1]))
            elif command == 'week':
                Main.week()
            elif command == 'total':
                Main.total()
            elif command[:5] == 'begin':
                Main.write_day(int(command[-1]), 7, raw_input('Enter time:\n'))
            elif command[:3] == 'end':
                Main.write_day(int(command[-1]), 0, raw_input('Enter time:\n'))
            elif command == 'reset':
                sure = raw_input('All values will be set to null, continue?\n')
                if sure == 'yes' or sure == 'y':
                    Main.reset()
                    print('All timers set to null')
                else:
                    print('Reset aborted')
            elif command == 'reload':
                for i in xrange(2):
                    self.file.close()
                    Main = Timestats()
                print('Reload complete')
            else:
                print('Unknown command, try again')


if __name__ == "__main__":
    Main = Timestats()
    Main.interface()