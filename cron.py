import sys
import config
from util import *
import traceback

logger = config.config.get_logger()


class Cron:
    """
      Simple cron parser expecting 5 tokens and a command in the cron expression
      1. Minute
      2. Hour
      3. Day of Month
      4. Month
      5. Day of weeks
      Format : "<Minute> <Hour> <Day of month> <Month> <Day of weeks>"
      Each token validated with allowed formats and then printed in easy to read way.
      Allowed formats : * , */num , num , num,num and num-num.
      This programs run with time complexity of O(number of tokens) and space complexity of 0(1)
    """

    def __init__(self, str):
        self.str = str
        self.parsed_tokens = dict()
        self.is_valid = True

        self.minutes = []
        self.hours = []
        self.day_of_months = []
        self.months = []
        self.day_of_weeks = []
        self.command = []

    def __set_named_values(self, time_index, explanded_values):
        time_period = get_time_name(time_index)
        if time_period == MINUTE:
            self.minutes = explanded_values
        elif time_period == HOUR:
            self.hours = explanded_values
        elif time_period == MONTH:
            self.months = explanded_values
        elif time_period == DAY_OF_MONTH:
            self.day_of_months = explanded_values
        elif time_period == DAY_OF_WEEK:
            self.day_of_weeks = explanded_values
        else:
            self.command = explanded_values

    def parse(self):
        if not self.str or self.str.strip() == "":
            self.is_valid = False
            return
        tokens = self.str.strip().split(" ")
        try:
            time_index = 0;
            for item in range(len(tokens)):
                if tokens[item].strip() == "":
                    continue
                if time_index > 4:
                    self.command.append(tokens[item])
                    continue
                is_valid, format_type = validate_tokens(tokens[item])
                logger.debug("Index : {} Token : {}, Format {}".format(time_index, tokens[item], format_type))
                if not is_valid:
                    logger.error("Invalid {} token : {} ".format(get_time_name(time_index), tokens[item]))
                    self.is_valid = False
                    return
                expanded_values = self.__expand_validate_token(time_index, format_type, tokens[item])
                if not expanded_values:
                    logger.error("Invalid {} , out of range values , token : {} ".format(get_time_name(time_index),
                                                                                         tokens[item]))
                    self.is_valid = False
                    return
                self.parsed_tokens.update({time_index: tokens[item]})
                self.__set_named_values(time_index, expanded_values)
                time_index = time_index + 1;
        except:
            traceback.print_exc()

    def __expand_validate_token(self, time_index, format_type, value):
        try:
            if format_type == TYPE_WILD:
                return self.__expand_token_index(time_index, 1)
            elif format_type == TYPE_STEPS:
                step = int(value.split("/")[1])
                if not is_valid_number(step, time_index):
                    return None
                return self.__expand_token_index(time_index, step)
            elif format_type == TYPE_RANGE:
                start_end = value.split("-")
                for i in start_end:
                    if not is_valid_number(int(i), time_index):
                        return None
                return self.__expand_token(int(start_end[0]), int(start_end[1]), 1)
            elif format_type == TYPE_SPLITS:
                splits = value.split(",")
                expanded_values = []
                for i in splits:
                    i = int(i)
                    if not is_valid_number((i), time_index):
                        return None
                    expanded_values.append(str(i))
                return expanded_values
            elif format_type == TYPE_NUMBER:
                if not is_valid_number(value, time_index):
                    return None
                return [value]
        except:
            traceback.print_exc()

    def __expand_token(self, start, end, step):
        values = []
        for i in range(start, end + 1, step):
            values.append(str(i))  # covert to int
        return values

    def __expand_token_index(self, time_index, step):
        start, end = get_start_end(time_index)
        return self.__expand_token(start, end, step)

    def to_string(self):
        logger.info("Minute        {}".format(" ".join(self.minutes)))
        logger.info("Hour          {}".format(" ".join(self.hours)))
        logger.info("Day of Month  {}".format(" ".join(self.day_of_months)))
        logger.info("Month         {}".format(" ".join(self.months)))
        logger.info("Day of week   {}".format(" ".join(self.day_of_weeks)))
        logger.info("Command       {}".format(" ".join(self.command)))


def howto():
    logger.info("\nExample : {}".format("python cron.py \"*/15 0 1,15 * 1-5 /usr/bin/find\""))


if __name__ == '__main__':
    if sys.argv and len(sys.argv) > 1:
        crons = []
        for i in range(len(sys.argv)):
            if i == 0:
                continue
            cron = Cron(sys.argv[i])
            cron.parse()
            cron.to_string()
            if cron.is_valid:
                crons.append(cron)
            else:
                howto()
    else:
        logger.error("No cron expression input string")
        howto()
