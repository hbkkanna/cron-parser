import unittest
import util
import cron
import traceback


class TestCron(unittest.TestCase):

    def test_validate_tokens(self):
        # print "start  valid tokens"
        # positive cases
        assert (True, util.TYPE_WILD) == util.validate_tokens("*")
        assert (True, util.TYPE_STEPS) == util.validate_tokens("*/7")
        assert (True, util.TYPE_STEPS) == util.validate_tokens("*/15")
        assert (True, util.TYPE_RANGE) == util.validate_tokens("0-31")
        assert (True, util.TYPE_SPLITS) == util.validate_tokens("0,1,3,4,31")
        assert (True, util.TYPE_NUMBER) == util.validate_tokens("77")

        # negative cases
        assert (False, None) == util.validate_tokens("**")
        assert (False, None) == util.validate_tokens("3-")
        assert (False, None) == util.validate_tokens("*/")
        assert (False, None) == util.validate_tokens("3,")
        # print "end valid tokens"

    def test_is_valid_number(self):
        # print "start is valid number"
        for index, value in util.TIME_VALUES.iteritems():
            assert True == util.is_valid_number(value[1], index)
            assert True == util.is_valid_number(value[1] + 1, index)
            assert True == util.is_valid_number(value[2], index)
            assert True == util.is_valid_number(value[2] - 1, index)

            # negative case
            assert False == util.is_valid_number(value[1] - 1, index)
            assert False == util.is_valid_number(value[2] + 1, index)

        # print "end  valid number"

    def test_cron(self):
        formats = ["*/5", "1,5", "1-4", "5"]
        cron_tokens = ["*", "*", "*", "*", "*"]
        valid_cases = []
        for m in range(5):
            for j in range(len(formats)):
                str = ""
                for k in range(len(cron_tokens)):
                    if m == k:
                        str = str + " " + formats[j]
                    else:
                        str = str + " " + cron_tokens[k]
                str = str + " " + "ls"
                valid_cases.append(str)

        """
        # manual testing
        valid_cases = [
            "*/15 0 1,15 * 1-5 /usr/bin/find come.xt",
            "* * * * *   /usr/bin/find",
            "*/45 1 5 6 7 /usr/bin/find",
            "0 */4 * * * /scripts/script.sh",
            "*/45 */2 */2     */3 */2    ls",
        ]
        """

        valid_cases.append("*/45 */2 */2     */3 */2    ls")

        invalid_cases = [
            "",
            "* * * 34-90 ls",
            "121 * & ms",
        ]

        try:
            for valid_str in valid_cases:
                print "-------------valid case start -------"
                print valid_str
                cron_obj = cron.Cron(valid_str)
                cron_obj.parse()
                # cron_obj.to_string()
                assert True == cron_obj.is_valid
                print "-------------valid case end---------------"
            for invalid_str in invalid_cases:
                print "-------------invalid case start -------"
                print invalid_str
                cron_obj = cron.Cron(invalid_str)
                cron_obj.parse()
                # cron_obj.to_string()
                assert False == cron_obj.is_valid
                print "------------invalid case end----------------"

        except:
            traceback.print_exc()


if __name__ == '__main__':
    unittest.main()
