import re


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


    def print_all(self):
        print(self.TEST_TYPE)
        print(self.FILE)
        print(self.FUNCTION)
        print(self.INPUT)
        print(self.OUTPUT)
        print(self.DESC)
        print(self.CODE)

    def split_keywords(self):
        return re.split(self.keywords, self.CODE)

    def build_import_list(self):
        self.generatedCode += "import " + self.FILE.split(".")[0] + "\n"
        with open(self.FILE) as file_f:
            file = file_f.read()
            self.generatedCode += re.split(r"\n\n", file, maxsplit=1)[0]
        self.generatedCode += "\n\n"

    def build_test_class(self):
        self.generatedCode += "\nclass Test(unittest.TestCase):\n\n"

    def build_main(self):
        self.generatedCode += "\nif __name__ == '__main__':\n"
        ##How can I make sure this isn't always hardcoded?
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
    reqObjects = 0
    with open("requirements.txt") as requirements_f:
        requirements = requirements_f.read()
        requirements = get_req_blocks(requirements)
        autoRequirements = remove_manual_test(requirements)
        reqObjects = classify_reqs(autoRequirements)
    #reqObjects[0].print_all()
    reqObjects[0].build_import_list()
    reqObjects[0].build_test_class()
    reqObjects[0].build_main()
    print(reqObjects[0].generatedCode)
