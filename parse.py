import re
import math

class Requirement:
    """Requirement Variables"""
    TEST_TYPE = ""
    FILE = ""
    FUNCTION = ""
    INPUT = ""
    OUTPUT = ""
    DESC = ""
    CODE = ""

    """Keywords of the requirement language"""
    keywords = r"IF |< |> |= |THEN |-"
    """The auto generated code"""
    generatedCode = ""
    test = ["","",""]

    def print_all(self):
        print(self.TEST_TYPE)
        print(self.FILE)
        print(self.FUNCTION)
        print(self.INPUT)
        print(self.OUTPUT)
        print(self.DESC)
        print(self.CODE)

    def eval_conditions(self):
        conditions = re.findall(r'IF.*', self.CODE)
        length = len(conditions)
        min = 0
        max = 0
        preCond = ""
        minCond = ""
        maxCond = ""
        for i in range(length):
            min = int(re.findall(r'(?<=\()\d*', conditions[i])[0])
            max = int(re.findall(r'\d*(?=\))', conditions[i])[0])
            cond = re.findall(r'[<>]', conditions[i])[0]
            preCond = re.findall(r'[a-zA-Z]+(?=\(\d+-\d+\) [<>])', conditions[i])[0]
            postCond = re.findall(r'(?<=[<>] )\d+', conditions[i])[0]
            if cond == "<":
                minCond = postCond
                self.test[i] += "\tdef test_less_than_" + postCond +"(self):\n"
                for x in range(min, max+1):
                    self.test[i] += "\t\tself.uut." + preCond + str(x) + ".set(" + str(int(postCond)-1) + ")\n"
            elif cond == ">":
                maxCond = postCond
                self.test[i] += "\tdef test_greater_than_" + postCond + "(self):\n"
                for x in range(min, max+1):
                    self.test[i] += "\t\tself.uut." + preCond + str(x) + ".set(" + str(int(postCond)+1) + ")\n"
        self.test[length] += "\tdef test_between_" + minCond + "_" + maxCond + "(self):\n"
        for i in range (min, max+1):
            self.test[length] += "\t\tself.uut." + preCond + str(i) + ".set(" + str(math.trunc((min+max)/2)) + ")\n"

    def run_and_assert(self):
        assertions = re.findall(r'ASSERT.*', self.CODE)
        for i in range(len(self.test)):
            preAssert = re.findall(r'[A-Za-z\d_-]+(?= =)', assertions[0])[0]
            postAssert = re.findall(r'(?<== ).*', assertions[0])[0]
            self.test[i] += "\t\tasyncio.run(self.uut." + self.FUNCTION + "())\n"
            #Any other possibilities for this?
            value = re.findall(r'(?<=.set\()-*\d*', self.test[i])[0]
            value = int(value)
            if value > 255:
                value = 255
            if value < 0:
                value = 0
            value = str(value)
            postAssert = re.sub(r'input\d*', value, postAssert)
            postAssert = re.sub(r',', ', ', postAssert)
            self.test[i] += "\t\tself.assertEqual(self.uut." + preAssert + ", " + postAssert + ")\n\n"


    def generate_tests(self):
        words = re.split("[ \n]", self.CODE)
        print(words)
        if words.count("IF") > 0:
            self.eval_conditions()
        if words.count("ASSERT") > 0:
            self.run_and_assert()
        for tests in self.test:
            self.generatedCode += tests


    def split_keywords(self):
        return re.split(self.keywords, self.CODE)

    def build_import_list(self):
        self.generatedCode += "import unittest\n"
        self.generatedCode += "import " + self.FILE.split(".")[0] + "\n"
        with open(self.FILE) as file_f:
            file = file_f.read()
            self.generatedCode += re.split(r"\n\n", file, maxsplit=1)[0]
        self.generatedCode += "\n\n"

    def build_test_class(self):
        self.generatedCode += "\nclass Test(unittest.TestCase):\n\n"
        self.generatedCode += "\tuut = main_desktop.Desktop()"
        self.generatedCode += "\n\n"

    def build_main(self):
        self.generatedCode += "\nif __name__ == '__main__':\n"
        self.generatedCode += "\tTk()\n"
        self.generatedCode += "\tunittest.main()\n"


def get_req_blocks(reqs):
    results = re.findall(r'(?<=REQ\n)((?:.|\n)*?)(?=REQ)', reqs)
    return results


def remove_manual_test(reqs):
    autoTest = []
    for req in reqs:
        if re.match(r'(TEST_TYPE:(?: )*MANUAL)', req) is None:
            autoTest.append(req)
    return autoTest


def classify_reqs(reqs):
    reqObjects = []
    for req in reqs:
        obj = Requirement()
        obj.TEST_TYPE = re.findall(r'(?<=TEST_TYPE)(?: *: *)(.*)', req)[0]
        obj.FILE = re.findall(r'(?<=FILE)(?: *: *)(.*)', req)[0]
        obj.FUNCTION = re.findall(r'(?<=FUNCTION)(?: *: *)(.*)', req)[0]
        obj.INPUT = re.findall(r'(?<=INPUT)(?: *: *)(.*)', req)[0]
        obj.OUTPUT = re.findall(r'(?<=OUTPUT)(?: *: *)(.*)', req)[0]
        obj.DESC = re.findall(r'(?<=DESC)(?: *: *)(.*)', req)[0]
        obj.CODE = re.findall(r'(?<=CODE)(?: *: *\n)((.|\n)*?(?=CODE))', req)[0][0]
        reqObjects.append(obj)
    return reqObjects


if __name__ == '__main__':
    with open("requirements.txt") as requirements_f:
        requirements = requirements_f.read()
        requirements = get_req_blocks(requirements)
        autoRequirements = remove_manual_test(requirements)
        reqObjects = classify_reqs(autoRequirements)
    #reqObjects[0].print_all()
    #reqObjects[0].pre_compile()
    reqObjects[0].build_import_list()
    reqObjects[0].build_test_class()
    reqObjects[0].generate_tests()
    reqObjects[0].build_main()
    print(reqObjects[0].generatedCode)
